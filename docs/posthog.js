/* Shared by the Product Page and Streamlit. The project token is public, not a personal API key. */
(() => {
  if (window.__rubricRadarAnalytics) return; // Streamlit reruns must not duplicate listeners/pageviews.
  window.__rubricRadarAnalytics = true;
  const surface = window.RUBRIC_RADAR_SURFACE === 'app'
    ? (window.location.hostname.endsWith('.streamlit.app') ? 'live_app' : 'local_app')
    : 'product_page';
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
      ['Home', 'home'],
      ['Continue as guest', 'continue_guest'],
      ['Explore sample library', 'explore_sample'],
      ['Exit sample', 'exit_sample'],
      ['Open my library', 'open_library'],
      ['My classes', 'my_classes'],
      ['Sign in', 'sign_in'],
      ['Sign out', 'sign_out'],
      ['Create account', 'create_account'],
      ['Confirm email', 'confirm_email'],
      ['Send recovery code', 'request_recovery'],
      ['Verify recovery code', 'verify_recovery'],
      ['Set new password', 'set_password'],
      ['Cancel recovery', 'cancel_recovery'],
      ['Create class', 'create_class'],
      ['Open class', 'open_class'],
      ['Create project', 'create_project'],
      ['Open project', 'open_project'],
      ['Save project', 'save_project'],
      ['Save review', 'save_review'],
      ['Open saved review', 'open_review'],
      ['Check a revised draft', 'revise_draft'],
      ['Back to classes', 'back_classes'],
      ['Return to classes', 'return_classes'],
      ['Back to projects', 'back_projects'],
      ['Back to project', 'back_project'],
      ['Previous page', 'previous_page'],
      ['Next page', 'next_page'],
      ['Keep working', 'keep_working'],
      ['Discard and continue', 'discard_continue'],
      ['Delete class', 'delete_class'],
      ['Delete project', 'delete_project'],
      ['Delete review', 'delete_review'],
      ['Cancel deletion', 'cancel_deletion'],
      ['Confirm deletion', 'confirm_deletion'],
      ['Load demo example', 'load_demo'],
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
