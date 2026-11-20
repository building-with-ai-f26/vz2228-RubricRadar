// No network or provider calls. Run: node --test tests/test_analytics.cjs
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');
const source = readFileSync('docs/posthog.js', 'utf8');

function browser(surface, hostname = '127.0.0.1') {
  const sent = [], scripts = [], listeners = [];
  let config;
  const posthog = {
    init: (token, options) => { config = options; options.loaded(posthog); },
    register: properties => sent.push(['register', properties]),
    capture: (...args) => sent.push(args),
  };
  const context = vm.createContext({
    window: { posthog, RUBRIC_RADAR_SURFACE: surface, location: { hostname } },
    document: {
      createElement: () => ({}),
      head: { appendChild: script => scripts.push(script) },
      addEventListener: (name, listener) => listeners.push(listener),
    },
  });
  vm.runInContext(source, context);
  scripts[0].onload();
  return { context, sent, scripts, listeners, config };
}

test('Streamlit reruns keep one SDK, one pageview, and one click listener', () => {
  const b = browser('app');
  vm.runInContext(source, b.context);
  assert.equal(b.scripts.length, 1);
  assert.equal(b.listeners.length, 1);
  assert.equal(b.sent.filter(e => e[0] === '$pageview').length, 1);
  assert.equal(b.sent[0][1].surface, 'local_app');
  assert.equal(browser('app', 'rubric-radar.streamlit.app').sent[0][1].surface, 'live_app');
  assert.equal(browser().sent[0][1].surface, 'product_page');
});

test('privacy config masks inputs and rendered text and rejects network capture', () => {
  const { config } = browser();
  assert.equal(config.autocapture, false);
  assert.equal(config.capture_exceptions, false);
  assert.equal(config.enable_recording_console_log, false);
  assert.equal(config.session_recording.maskAllInputs, true);
  assert.equal(config.session_recording.maskTextSelector, '*');
  assert.equal(config.session_recording.recordBody, false);
  assert.equal(config.session_recording.recordHeaders, false);
  assert.equal(config.session_recording.maskCapturedNetworkRequestFn({ body: 'PRIVATE' }), null);
});

test('clicks emit fixed names only; unknown text and disabled buttons emit nothing', () => {
  const b = browser('app');
  const click = control => b.listeners[0]({ target: { closest: () => control } });
  click({ textContent: 'PRIVATE COURSEWORK' });
  click({ textContent: 'Extract requirements', disabled: true });
  assert.equal(b.sent.length, 2);
  click({ textContent: 'Extract requirements' });
  assert.equal(b.sent[2][0], 'ui_clicked');
  assert.equal(JSON.stringify(b.sent[2][1]), '{"action":"extract_requirements","surface":"local_app"}');
});


test('library controls emit fixed names without record titles or IDs', () => {
  const b = browser('app');
  for (const textContent of ['Explore sample library', 'Load demo example', 'Save review', 'Confirm deletion', 'Synthetic private class']) {
    b.listeners[0]({ target: { closest: () => ({ textContent }) } });
  }
  const clicks = b.sent.filter(e => e[0] === 'ui_clicked');
  assert.deepEqual(clicks.map(e => e[1].action), ['explore_sample', 'load_demo', 'save_review', 'confirm_deletion']);
  for (const [, properties] of clicks) assert.deepEqual(Object.keys(properties).sort(), ['action', 'surface']);
});
