# Google sign-in — Build 3

Google sign-in replaces the earlier email/password/code plan. Students choose
Continue with Google; no app password, verification email or SMTP sender is needed.
Google/Supabase still process identity information. Google is not granted access to
coursework, Gmail or Drive by this sign-in flow.

## Implementation

The local `google_signin/` component renders Google's official Identity Services
button in popup mode. It loads only Google's sign-in SDK, not analytics. One Tap
and automatic sign-in are not requested. Python creates a random nonce per login
attempt, keeps the original in the current Auth object for at most five minutes,
and gives only its SHA-256 hash to the component/Google. The credential is returned
in memory over the existing Streamlit component channel. The server consumes the
nonce once, calls Supabase `/auth/v1/token?grant_type=id_token` with the original
nonce, then verifies the returned identity through `/auth/v1/user`. Supabase checks
Google's signature/audience/expiry/nonce; never disable its nonce check.

No callback query parameters, token URLs, browser token storage, shared auth cache,
Google client secret in Python, new dependencies or database changes are required.
The browser and server temporarily handle credentials in memory; this is not a
secure-erasure guarantee. Sign-out clears app data/tokens and attempts Supabase
session revocation; it does not sign the student out of Google. Supabase JWTs can
remain valid until expiry. Lost Streamlit sessions require signing in again.

## Google configuration

1. Use the builder's chosen Google account. In Google Cloud Console select an owned
   project and open Google Auth Platform. Do not enable billing or paid resources.
2. Configure app name **Rubric Radar**, builder support/developer email and audience.
   External/Testing permits named test accounts without publishing the app. If
   Google requests agreement to its policy, the builder must approve acceptance.
   Add the two intended test accounts when required by the audience configuration.
3. Create a **Web application** OAuth client. Authorized JavaScript origins for
   local development: `http://localhost:8501` and `http://127.0.0.1:8501`. Add the
   exact deployed HTTPS origin only when deployment is approved. The ID-token
   popup implementation does not need an application redirect handler.
4. If configuring the provider's optional redirect flow as well, its Google
   authorized redirect URI is the project's Supabase `/auth/v1/callback` URL.
   Our application does not consume that redirect flow. Do not enable a flow by
   weakening nonce checks or using broad redirect wildcards.
5. Keep requested access limited to basic identity (`openid`, email, profile).
   No Gmail/Drive APIs, offline access or Google access tokens are needed. School
   policy may restrict creating projects, OAuth clients or consenting to apps;
   record actual errors and use a builder-approved account/project instead.

## Supabase and local configuration

1. Authentication → Sign In / Providers → Google: enable Google with the same Web
   client ID. Keep **Skip nonce checks off**. An OAuth client secret, if required
   by the dashboard for enabling the provider, belongs only in Supabase, not chat,
   Git or the Python app. Enter/manage credentials privately.
2. Disable the Email provider once Google is configured and no existing password
   accounts need it. No such user migration is part of this prototype. Leave
   anonymous sign-ins and manual identity linking disabled. Do not disable
   ownership policies or expose tables to unauthenticated clients.
3. In ignored `.env`, configure `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY` and
   `GOOGLE_CLIENT_ID` per `.env.example`. Preserve existing values/secrets. Keep
   `RUBRIC_RADAR_ARCHIVE_ENABLED=false` until real SQL and two-account API checks
   prove ownership isolation. Google configuration alone does not satisfy this gate.
4. When the gate can safely be enabled, restart Streamlit, use the exact authorized
   origin, open My library and choose Continue with Google. Verify both accounts,
   popup cancellation, sign-out/re-entry, expired/reused attempts and Google/NYU
   refusal. Verify phone behavior and live replay separately. No real coursework.

## Validation and pending work

Python mocks cover nonce expiry, reuse, session binding, failure, Supabase-verified
identity and UI state clearing. Node tests use synthetic Google/Streamlit messages
to check origin/source filtering, one credential submission, library failure and
cancelled popup behavior. These do not prove real browser popup compatibility,
Google consent/delivery, hosted session behavior or database isolation. Current
configuration progress and every test run are in `tests/README.md` and Plan.md.

Official references: [Supabase Google sign-in](https://supabase.com/docs/guides/auth/social-sign-in/auth-google),
[Google button](https://developers.google.com/identity/gsi/web/guides/display-button),
[Google JavaScript API](https://developers.google.com/identity/gsi/web/reference/js-reference).
