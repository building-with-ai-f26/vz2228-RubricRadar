// Synthetic Google/Streamlit messages only: no Google credentials or network.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');
const source = readFileSync('google_signin/signin.js', 'utf8');

function browser() {
  const sent = [], scripts = [], configurations = [], renders = [], listeners = [];
  const origin = 'http://localhost:8501';
  const parent = { postMessage: (value, target) => sent.push({ value, target }) };
  const elements = { status: { textContent: '' }, button: {} };
  const context = vm.createContext({
    URL,
    window: { parent, location: { href: origin + '/component/google_signin' }, innerWidth: 296,
      addEventListener: (name, handler) => listeners.push(handler) },
    document: { referrer: origin + '/', getElementById: id => elements[id],
      createElement: () => ({}), head: { appendChild: script => scripts.push(script) } },
  });
  const google = { accounts: { id: {
    initialize: options => configurations.push(options),
    renderButton: (target, options) => renders.push(options),
  } } };
  vm.runInContext(source, context);
  const args = { client_id: 'synthetic.apps.googleusercontent.com', nonce: 'a'.repeat(64) };
  const render = (overrides = {}) => listeners[0]({ source: parent, origin,
    data: { type: 'streamlit:render', args }, ...overrides });
  const load = () => { context.google = google; context.window.google = google; scripts[0].onload(); };
  return { sent, scripts, configurations, renders, elements, args, render, load, context };
}

test('button rejects other frames/origins and only loads the official Google library once per challenge', () => {
  const b = browser();
  b.render({ origin: 'https://evil.test' }); b.render({ source: {} });
  assert.equal(b.scripts.length, 0);
  b.render(); b.render();
  assert.equal(b.scripts.length, 1);
  assert.equal(b.scripts[0].src, 'https://accounts.google.com/gsi/client');
  b.load();
  assert.equal(b.configurations[0].nonce, b.args.nonce);
  assert.equal(b.configurations[0].auto_select, false);
  assert.equal(b.renders[0].text, 'continue_with');
  assert.ok(b.renders[0].width < 296);
});

test('credential returns only once to the exact parent and is never rendered', () => {
  const b = browser(); b.render(); b.load();
  b.configurations[0].callback({ credential: 'SYNTHETIC-PRIVATE-TOKEN' });
  b.configurations[0].callback({ credential: 'SYNTHETIC-PRIVATE-TOKEN' });
  const values = b.sent.filter(({ value }) => value.type === 'streamlit:setComponentValue');
  assert.equal(values.length, 1);
  assert.equal(values[0].target, 'http://localhost:8501');
  assert.equal(values[0].value.value.credential, 'SYNTHETIC-PRIVATE-TOKEN');
  assert.equal(values[0].value.value.challenge_id, b.args.nonce);
  assert.ok(!JSON.stringify(b.elements).includes('PRIVATE-TOKEN'));
});

test('Google script failure returns a fixed error, and dismissing the popup returns no credential', () => {
  const b = browser(); b.render(); b.scripts[0].onerror();
  const response = b.sent.find(({ value }) => value.type === 'streamlit:setComponentValue');
  assert.equal(response.value.value.error, 'unavailable');
  assert.equal(response.value.value.credential, undefined);
  const cancelled = browser(); cancelled.render(); cancelled.load();
  assert.equal(cancelled.sent.filter(({ value }) => value.type === 'streamlit:setComponentValue').length, 0);
});
