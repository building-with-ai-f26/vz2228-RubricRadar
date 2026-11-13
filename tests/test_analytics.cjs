// No network or provider calls. Run: node --test tests/test_analytics.cjs
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');
const source = readFileSync('docs/posthog.js', 'utf8');

function browser(surface) {
  const sent = [], scripts = [], listeners = [];
  let config;
  const posthog = {
    init: (token, options) => { config = options; options.loaded(posthog); },
    register: properties => sent.push(['register', properties]),
    capture: (...args) => sent.push(args),
  };
  const context = vm.createContext({
    window: { posthog, RUBRIC_RADAR_SURFACE: surface },
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
  const b = browser('local_app');
  vm.runInContext(source, b.context);
  assert.equal(b.scripts.length, 1);
  assert.equal(b.listeners.length, 1);
  assert.equal(b.sent.filter(e => e[0] === '$pageview').length, 1);
  assert.equal(b.sent[0][1].surface, 'local_app');
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
  const b = browser('local_app');
  const click = control => b.listeners[0]({ target: { closest: () => control } });
  click({ textContent: 'PRIVATE COURSEWORK' });
  click({ textContent: 'Extract requirements', disabled: true });
  assert.equal(b.sent.length, 2);
  click({ textContent: 'Extract requirements' });
  assert.equal(b.sent[2][0], 'ui_clicked');
  assert.equal(JSON.stringify(b.sent[2][1]), '{"action":"extract_requirements","surface":"local_app"}');
});
