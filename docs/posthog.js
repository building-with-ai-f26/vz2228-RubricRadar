/* Shared by the Product Page and Streamlit. The project token is public, not a personal API key. */
(() => {
  if (window.__rubricRadarAnalytics) return; // Streamlit reruns must not duplicate listeners/pageviews.
  window.__rubricRadarAnalytics = true;
  const surface = window.RUBRIC_RADAR_SURFACE === 'local_app' ? 'local_app' : 'product_page';
  const sdk = document.createElement('script');
  sdk.src = 'https://us-assets.i.posthog.com/static/array.js';
  sdk.async = true;
  sdk.onerror = () => { window.__rubricRadarAnalytics = false; };
  sdk.onload = () => {
    window.posthog.init('phc_AbQiiT8StyPnpxAZBeHmCjphbZwZopRiXUpub8M9Xa4Q', {
      api_host: 'https://us.i.posthog.com',
      ui_host: 'https://us.posthog.com',
      autocapture: false, // Only the fixed control names below are sent, never DOM text/attributes.
      capture_pageview: false,
      capture_pageleave: false,
      capture_dead_clicks: false,
      capture_exceptions: false,
      capture_heatmaps: false,
      capture_performance: false,
      disable_surveys: true,
      disable_session_recording: false,
      enable_recording_console_log: false,
      person_profiles: 'identified_only',
      session_recording: {
        maskAllInputs: true,
        maskTextSelector: '*',
        recordCrossOriginIframes: false,
        recordHeaders: false,
        recordBody: false,
        maskCapturedNetworkRequestFn: () => null,
      },
      loaded: (posthog) => {
        posthog.register({ surface });
        posthog.capture('$pageview');
      },
    });

    const actions = new Map([
      ['Clear this session', 'clear_session'],
      ['Extract requirements', 'extract_requirements'],
      ['Confirm & review my draft', 'confirm_review'],
      ['Project Status →', 'view_product_status'],
      ['Read the Living PRD', 'view_prd'],
      ['Weekly Build Log', 'view_build_log'],
    ]);
    document.addEventListener('click', (event) => {
      const control = event.target.closest('button, a');
      if (!control || control.disabled) return;
      const action = actions.get(control.textContent.trim());
      if (action) window.posthog.capture('ui_clicked', { action, surface });
    }, true);
  };
  document.head.appendChild(sdk);
})();
