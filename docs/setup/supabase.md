# Build 3 Supabase foundation — setup and verification

Batch 3 connects the UI behind RUBRIC_RADAR_ARCHIVE_ENABLED=false by default.
Guest mode and the read-only synthetic library work without Supabase. Sign-in and
cloud archive requests remain disabled until actual security verification.
For account creation, start with [builder instructions](./supabase-account.md).
No cloud service is created or database migration applied by these files.

## Configuration

Use a hosted Supabase project and its **publishable** key. `CloudConfig` intentionally
rejects secret keys, legacy JWT keys and custom/self-hosted URLs in this first version.
The transport uses standard-library HTTPS with the existing certifi package; no new
runtime dependencies. Supabase remains responsible for credentials and token verification.

Local: add SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY and GOOGLE_CLIENT_ID to the ignored `.env` using
`.env.example` as the field reference. Do not overwrite an existing `.env`.
`app.py` already loads dotenv; the foundation modules do not load configuration at import.
For future hosting, place these fields and OPENROUTER_API_KEY in Streamlit host secrets.
`CloudConfig.from_settings(st.secrets)` accepts a flat mapping; environment settings use
`CloudConfig.from_settings()`. Never copy real values into docs or terminal output.
`.streamlit/secrets.toml`, archive files/dumps and CLI state are ignored.

## Schema installation and verification

1. Choose a disposable/test Supabase project first. Review
   `supabase/migrations/202611170001_private_archive.sql` before applying it with the
   Supabase SQL editor or migration tooling. Do not paste credentials into source files.
2. The migration is transactional, creates `rr_classes`, `rr_projects`, `rr_reviews`
   and an invoker-rights deletion-count RPC, and explicitly grants authenticated users
   only the required operations. Anonymous access is revoked. All tables have RLS;
   composite foreign keys enforce same-owner parents. Review UPDATE is not granted.
3. It is a one-time migration, not a rerunnable setup script. A failed transaction
   rolls back. A later schema change requires a new migration and recovery plan.
   Do not roll back a deployed database by dropping tables containing saved coursework.
4. Run `supabase/tests_private_archive.sql` against a disposable local Supabase DB
   using `psql -v ON_ERROR_STOP=1 -f supabase/tests_private_archive.sql <local-connection>`.
   The migration must already be installed. Keep connection credentials out of shell
   history; use an appropriate local password file/environment supplied privately.
   The script creates temporary synthetic fixtures in a transaction and rolls back.
   It uses administrator access to seed users, then switches to authenticated/anon
   roles to test actual permissions, RLS, same-owner constraints, duplicate saves,
   immutable reviews, invoker counts and cascade deletion. On November 19 it passed in the hosted test project SQL Editor after the builder approved the rollback-only run.
5. The separate two-account HTTP check passed against hosted Supabase on November 19.
   Live expired-token and full app workflow checks remain pending. [Security evidence](../../SECURITY.md#required-two-account-test--november-19)

## Google sign-in (selected November 18)

Google replaces the earlier email/password/code plan; do not configure SMTP or
email templates for this flow. Follow [Google setup](google-signin.md).
The official Google popup supplies an ID token; Supabase verifies its nonce and
returns the user/session used by RLS. The app has no password/reset forms.
Google is enabled, Email is disabled, and nonce checks are on. Both approved test
accounts completed local Google sign-in and sign-out. The archive flag remains off.

## Batch 3 integration and verification boundary

Create one `Auth(CloudAPI(config))` per Streamlit session and `Archive(auth)` for it.
Only explicit UI save actions call archive writes. Guest mode does not construct an
archive workflow or issue archive requests. Never pass a form-provided owner ID.
Each archive operation checks the current identity with Supabase before its data API
request; the database also checks the supplied user token through RLS.

On logout, account changes or guest entry, immediately clear coursework, old Auth
objects, outputs, consent and password/code widgets. Call `Auth.sign_out()` and handle
failure with a safe message: it clears local tokens even if remote revocation fails.
Supabase access JWTs may remain valid until expiry after logout; no immediate access
JWT revocation claim. Losing a browser/server session requires signing in again;
there is no persistent login cookie in this batch. Confirm ordinary context switches
with unsaved work; logout must not wait for that confirmation.

Archive save tokens are UUIDs: generate once per current validated result in session
state and reuse on reruns; changing inputs/results invalidates the token. The database
uniqueness rule handles concurrent retries. `make_snapshot` takes the current inputs,
original extraction, confirmed requirements and validated result. It checks structure,
source/evidence integrity and whitelists operational metadata. This cannot establish
that the UI supplied a *current* result: the implemented UI gates saves with current-result hashes and invalidates stale state (mocked tests passed).

`list_classes`, `list_projects`, and `list_reviews` return pages of 100 rows with an
offset and stable timestamp/ID ordering; the UI offers previous/next page controls.
Opening a review validates its snapshot and makes no model calls. Invalid historical
records produce a recoverable error, not silent repair or automatic re-evaluation.

Before deleting, use `deletion_counts`, show the selected item and counts, obtain
confirmation, then call `delete(..., confirmed=True)`. Concurrent saves can change counts;
the UI rechecks counts and asks for confirmation again when they change. This does not freeze concurrent writes between the final count and deletion. The foundation's
boolean is a UI contract, not an authorization control. RLS/FKs enforce scope and atomic
cascade deletion; active-table deletion does not erase backups/provider records.

## What is verified versus pending

Mocked tests exercise request construction/redaction, per-object auth, Google nonce binding/reuse/expiry, refresh and
verification failures, save validation/idempotency and safe storage
failures. Hosted SQL-role and direct two-account tests provide the database evidence.
See the [test log](../../tests/README.md#november-19--two-account-direct-api-isolation)
and [security audit](../../SECURITY.md) for results and remaining checks.

Official references: [Auth HTTP API](https://supabase.com/docs/reference/self-hosting-auth/introduction),
[email code templates](https://supabase.com/docs/guides/auth/auth-email-templates),
[OTP types](https://supabase.com/docs/reference/python/auth-verifyotp),
[row-level security](https://supabase.com/docs/guides/database/postgres/row-level-security).
