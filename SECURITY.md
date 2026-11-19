# Security audit — Build 3 (pending)

**Current checkpoint — November 19.** Google sign-in worked for both approved test accounts. Hosted SQL-role, anonymous access and authenticated two-account isolation checks passed. The archive stays disabled. Expired-token verification, full app testing and the release audit are pending. Earlier checkpoints below are historical. [Test evidence](tests/README.md#november-19--two-account-direct-api-isolation)

**November 18 configuration.** Google sign-in replaced email/password/code accounts. The Google Web client was configured in the builder's existing My First Project after project creation outside the school organization was refused. OAuth origins were limited to localhost:8501 and 127.0.0.1:8501. Supabase Google was enabled with nonce checks on, and Email was disabled. Hosted schema installation succeeded. The ignored local `.env` retained the provider key and was configured for the Supabase project and Google client. [Google setup](docs/setup/google-signin.md)


Updated November 17, 2026. **Full audit incomplete; no production readiness is claimed.** Batch 2 adds local auth/archive contracts and unexecuted SQL schema/security tests. The app has local guest/sample and gated library UI; Supabase Auth/Postgres are provisioned and schema installation succeeded November 18, but no live isolation proof exists. Earlier batch 2/3 auth findings below are historical; the Google batch supersedes email/password/recovery. See Plan.md and PRD.md section 13.

## Batch 3 local UI checkpoint — November 17

Account/guest/library UI is implemented, with cloud access gated off by default. The builder will create the account/project; no actual migration/security proof has run. Fixed synthetic sample data is read-only and cannot call models or archive writes. Load demo example replaces working inputs, resets consent and invalidates feedback/save tokens without sending/saving text. Current account identity is checked before private pages; failed verification, logout or identity change clears working coursework and credential widgets. Unsaved navigation offers keep/discard; current-result fingerprints gate saves; duplicates are disabled after success. Revised saved drafts require fresh extraction and consent. Deletion cancellation and changed-count reconfirmation are tested; a race between final count and cascade deletion is still possible.

Local tests: staged runs passed 46, 57, 60 and finally 61 mocked Python tests as coverage was added. Four analytics tests passed before and after the demo action mapping. No failing automated run. A manual hot-reload ImportError occurred when the running server retained the old sample module; restarting Streamlit and reloading restored the app. Native Chrome verified sample navigation and demo fill with consent off; no model called. These do not prove actual Supabase access controls, phone usability or live PostHog ingestion/masking. Full audit remains incomplete; details in tests/README.md.

## Scope and evidence

Audit the app, dependencies, repository/history, hosting/secrets, Supabase auth and every coursework table/API path, OpenRouter privacy/cost controls, logs, analytics and replay. Use synthetic data and redact credentials. For each completed check record date, revision/deployed environment, method, expected/observed result, finding, fix/retest and residual risk. Link tests/README.md entries and safe screenshots. An unchecked item is not a finding of safety.

| Area | Planned checks | Status / actual findings / fixes |
| --- | --- | --- |
| Secrets | Working tree + history; ignored local secrets; host secrets; no tokens/keys in UI/logs | Pending; no finding/fix recorded |
| Dependencies | Installed versions, advisories, supported hosting runtime | pip check passed; advisory/runtime audit pending |
| Authentication | Google identity, expiry/refresh, logout and per-session clients | Live sign-in and sign-out verified in the local test pages. Live expired-token and full app session checks pending |
| Authorization | Grants and RLS, forged owner IDs, same-owner parents and direct API verification | Hosted SQL-role, anonymous access and two-account direct API checks passed on November 19. See evidence below |
| Guest and account state | No guest coursework saves; logout/account/context changes clear private working state | Pending; no finding/fix recorded |
| Input/output | Parameterized operations, bounds, escaped rendering, untrusted model/stored content, safe errors | Pending; no finding/fix recorded |
| API and cost | Server-held provider key, privacy-compatible routing, request/concurrency controls and budget | Pending; numeric limits undecided |
| Privacy/analytics | No coursework/credentials in logs/events/URLs; masked auth, names, drafts and history; console/network-body capture off | Pending live audit; earlier local checks are not Build 3 verification |
| Storage/deletion | Immutable snapshots, duplicate-save guard, owned transactional deletion, retention/backup/account deletion disclosures | Hosted SQL assertions passed for uniqueness, cascading deletion and immutability. Direct API checks verified own review deletion and fixture cleanup. Full app workflow and retention decisions pending |
| Hosting/recovery | HTTPS, secrets, phone usability, deployed revision, code rollback + migration recovery | Pending; no live app deployed |

## Local checks, finding and fix — November 17

Working tree based on `1d34206`; no deployment. Initial run: 44 mocked Python tests passed. Source review then identified an outcome-reporting bug: a successful password update followed by a failed logout could raise a generic failure and hide the successful change. Fixed reset handling to discard local recovery state immediately, report password-change success separately from unconfirmed remote sign-out, and preserve the original error when password update fails. Two regression tests added; final suite: 46 passed. No failing automated run occurred for this issue; it was found by source review. Three analytics checks and pip check passed. Details: tests/README.md.

Other local checks cover HTTPS origin/publishable-key restrictions, redirect refusal, bounded requests, safe errors, identity verification, recovery isolation, snapshot validation and duplicate-save contracts. These are mocked/source checks, not a full security audit. No secrets/history/advisory scan, live Auth/email test, real SQL/RLS execution, phone test or new replay inspection has been completed in this batch.

The migration and rollback-only SQL role tests are under supabase/; setup and limitations are in docs/setup/supabase.md. No psql, Docker or Supabase CLI is available in the inspected environment, so both scripts remain unrun. Future live tests must use real user tokens and bypass the UI; SQL-role simulation alone is insufficient. Access tokens can remain valid until JWT expiry after logout. UI state clearing, stale-save gating and pagination are now implemented and covered by mocked tests; real-service validation is pending. Guest model abuse/spend protection remains a pre-release gate.

## Required two-account test — November 19

1. A creates synthetic class/project/review records. Record fixture IDs privately during execution, never tokens or coursework in public evidence.
2. B demonstrates successful operations on B's own fixtures (positive control).
3. Using B's token and the publishable key, attempt direct API reads/updates/deletes of A's records, forged-owner inserts, and cross-owner parent attachment/reparenting. Test anonymous and expired-token access too.
4. Verify no A records are disclosed/changed and no unauthorized children are created. A can still read its unchanged fixtures. A denied read may return an empty result; do not label it a 403 unless observed.
5. Capture a labeled refused write showing expected/observed outcome and deployed version without credentials. Link the screenshot and full evidence entry here, including failures and retests.

**Result.** Hosted Supabase authorized each user's own synthetic operations. Cross-account access returned zero rows, the forged-owner insert was refused with HTTP 403, and cross-owner parent writes were refused with HTTP 409. A's records remained unchanged until fixture cleanup. Anonymous requests returned HTTP 401. Live expired-token behavior remains pending. The test ran from a localhost harness on revision `9688490` on November 19, 2026. Public app deployment remains pending. [Refused-write screenshot](tests/evidence/supabase-two-account-isolation-2026-11-19.png) · [Full record](tests/README.md#november-19--two-account-direct-api-isolation)

## Remaining risks and release gates

Complete expired-token and full app session verification, rate/concurrency/spending limits, provider account privacy settings, cloud retention/backups/account deletion and runtime compatibility. Verify live PostHog ingestion and complete masking before real coursework. Document any remaining limitations after fixes.

## November 18 Google configuration checkpoint

Hosted configuration: Google Web client created after explicit builder approval; Google provider saved without client secret for the ID-token flow, nonce checks on, no-email identities disallowed. Email provider disabled after approval. Anonymous sign-ins/manual linking remain off. Only local origins are authorized and one chosen NYU test user is configured. No service-role key used. Local .env stores only the intended project URL, publishable key and Google client ID alongside existing provider configuration; gate false. Client secret was not saved/downloaded or placed in app settings.

Auth source now uses a five-minute, one-use server nonce and server-verified Supabase identity. Python recovery suite: 61 passed; one earlier AppTest timeout and recovery recorded. Four analytics plus three Google component Node tests passed. These mocks do not prove Google popup compatibility, live nonce enforcement, hosted JWT/session isolation or database policies. No new tests after the builder requested finishing configuration without testing; full audit remains incomplete. See tests/README.md for exact results and limitations.
