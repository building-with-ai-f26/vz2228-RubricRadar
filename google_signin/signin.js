/* Google credential stays in memory, never in URLs, DOM text, storage or logs. */
(() => {
  'use strict';
  const parentOrigin = new URL(document.referrer || window.location.href).origin;
  let activeNonce = null;
  let submitted = false;
  const send = (type, payload = {}) => window.parent.postMessage({ isStreamlitMessage: true, type, ...payload }, parentOrigin);
  const status = text => { document.getElementById('status').textContent = text; };
  const fail = () => {
    status('Google could not load. Check your connection, then try again.');
    if (!submitted) {
      submitted = true;
      send('streamlit:setComponentValue', { value: { error: 'unavailable', challenge_id: activeNonce }, dataType: 'json' });
    }
  };
  window.addEventListener('message', event => {
    if (event.source !== window.parent || event.origin !== parentOrigin || event.data?.type !== 'streamlit:render') return;
    const args = event.data.args;
    if (!args || !/^[A-Za-z0-9_-]{1,200}\.apps\.googleusercontent\.com$/.test(args.client_id)
        || !/^[a-f0-9]{64}$/.test(args.nonce) || activeNonce === args.nonce) return;
    activeNonce = args.nonce;
    const nonce = activeNonce;
    const render = () => {
      if (nonce !== activeNonce) return;
      google.accounts.id.initialize({
        client_id: args.client_id, nonce, auto_select: false, ux_mode: 'popup',
        callback: response => {
          if (submitted || nonce !== activeNonce) return;
          if (typeof response?.credential !== 'string' || response.credential.length > 16384) { fail(); return; }
          submitted = true;
          status('Finishing sign-in…');
          send('streamlit:setComponentValue', {
            value: { credential: response.credential, challenge_id: nonce }, dataType: 'json',
          });
        },
      });
      google.accounts.id.renderButton(document.getElementById('button'), {
        type: 'standard', theme: 'outline', size: 'large', text: 'continue_with',
        shape: 'rectangular', width: Math.min(320, Math.max(200, window.innerWidth - 4)),
      });
      status('Choose your Google account in the sign-in window.');
    };
    if (window.google?.accounts?.id) render();
    else {
      const script = document.createElement('script');
      script.src = 'https://accounts.google.com/gsi/client';
      script.async = true;
      script.onload = render;
      script.onerror = fail;
      document.head.appendChild(script);
    }
  });
  send('streamlit:componentReady', { apiVersion: 1 });
  send('streamlit:setFrameHeight', { height: 100 });
})();
