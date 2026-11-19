# Build 3 — Beginner lane: private saved reviews

Updated November 19, 2026. Start here when you return.

## Resume here

**Verified.** Both approved Google test accounts signed in and out through a local test page. Hosted Supabase passed the rollback-only SQL checks, four anonymous access checks and authenticated two-account API isolation on revision `9688490`. The test removed its synthetic fixtures. The latest suite rerun on the new Mac passed 61 Python and seven Node tests. [Test log](tests/README.md#november-19--two-account-direct-api-isolation) · [Refused-write screenshot](tests/evidence/supabase-two-account-isolation-2026-11-19.png)

**Current environment.** `RUBRIC_RADAR_ARCHIVE_ENABLED=false`. Google OAuth is External/Testing with the NYU and personal test accounts. The allowed origins are `http://localhost:8501` and `http://127.0.0.1:8501`. The hosted HTTPS origin is pending. The ignored `.env` contains working local configuration. The Streamlit app has no public URL.

### Next session

1. **Restore the local runtime.** Check `.venv/bin/python --version`. The copied environment points to a missing Python framework from the prior Mac. Build a fresh venv from native ARM64 Python 3.14.4 after moving the old venv aside outside the repo. Install `requirements.txt` and preserve the ignored `.env`. The November 19 test used a temporary environment and its servers were stopped.
2. **Finish hosted auth verification.** Check that Supabase refuses a genuinely expired access token. Use a test session and hold the token only in memory until it expires. Keep the archive gate off during this check. Record the actual response.
3. **Verify the full app with synthetic data.** After the auth check and explicit approval to turn on the local archive gate, exercise sign-in → class/project → explicit save → sign-out/in → reopen → confirmed deletion. Verify guest and context isolation and record any approval needed for billable review calls. Keep real coursework out of the test.
4. **Approve Batch 4 before release work.** Finish the audit and request/concurrency/spend controls, settle retention and recovery, and get approval for Streamlit Community Cloud deployment. Configure the deployed Google HTTPS origin, verify the phone workflow and live PostHog event/replay masking, and prepare the submission note and live URL. [Audit register](SECURITY.md)

### What is ready locally

- Guest review and gated Google sign-in, private classes/projects/history, explicit save/delete controls, pagination and context clearing.
- Read-only synthetic sample and Load demo example. Explore both with `.venv/bin/python -m streamlit run app.py` at `http://127.0.0.1:8501`.
- Existing desktop and 400px/768px browser previews. Native form autocomplete warnings, broader accessibility testing and real-device checks remain open.

Suggested resume message: **“Open Plan.md and continue Build 3 from the first pending step.”**

## Decisions

- Public app: Streamlit Community Cloud; keep the Python/Streamlit review UI and OpenRouter backend. GitHub Pages continues to host the separate Product Page, not the Python app.
- Accounts: Google Identity Services → Supabase Auth, approved November 18 in place of email/password/code signup and recovery. No app password or SMTP sender. Keep nonce checks enabled and basic identity only; verify Google browser flow, token refresh, expiry and logout.
- Storage: Supabase Postgres with row-level security (RLS) on every exposed coursework table. This replaces the November 15 local SQLite proposal; do not implement a shared local archive on the public server.
- Organization: each student's private Class → Project → Saved reviews. Project means assignment; there is no extra assignment level. Class name required; professor/semester optional. No shared class roster or collaboration.
- Entry: Continue as guest or Sign in / My classes. Guests use the existing consent/review flow without archive writes. Guest requests still use provider processing and masked analytics.
- Saving: explicit Save project and Save review actions; no automatic coursework persistence. Opening a saved review makes no model call. A fresh review of a revised draft creates a new immutable snapshot.
- Beginner lane does not require preview deployments, automatic test-gated production merges, or separate dev/production databases. Use mocks and local/test infrastructure for development; use only synthetic records for deployed security checks. Never run destructive development checks on real saved coursework.

## Data and access design

| Entity | Proposed fields |
| --- | --- |
| Class | Generated ID, owner user ID, course name, optional professor/semester, creation timestamp |
| Project | Generated ID, owner user ID, class ID, name, explicitly saved instructions/rubric, creation timestamp |
| Saved review | Generated ID, owner user ID, project ID, unique save token, schema version, timestamp, exact instructions/draft snapshot, extracted and confirmed requirements, validated findings/priorities/limitations, available model/prompt/run metadata |

Use database-enforced ownership for reads, inserts, updates, and deletes, based on the verified authenticated user. Enforce same-owner parent relationships so a student cannot attach a project/review to another student's class/project. Do not trust a user ID supplied by a form. Use the publishable client key plus the user's token; do not use a service-role/secret key in routine app data access because it bypasses RLS. No unauthenticated archive privileges.

Keep authenticated clients/tokens isolated to the current session; never put them in a shared/global cache. Logout, account changes, guest transitions, and context switches clear coursework/results/consent before destination content loads. Offer Keep working / Discard for ordinary context switches with unsaved work, without delaying logout. Clear this session clears working data, not saved records.

Save only a successful, current validated result. Enforce duplicate-save prevention in the database as well as the UI. Storage failures preserve working inputs/results without claiming success. Validate stored snapshot structure on load; do not execute saved content. Never save API keys, passwords, auth tokens, raw provider responses, or consent flags in review records.

Confirm deletion of a review/project/class, name the item, show affected counts, and delete descendants transactionally. No undo in this version. Disclose cloud storage, who operates it, and that deletion from active tables does not promise removal from backups/provider systems. Resolve retention and account-deletion handling before release. Class metadata organizes records; it is not extra grading criteria or cross-project AI memory.

## Small implementation batches

1. **Plan and PRD v3 — completed locally November 17.** Save this resume plan; document hosting, accounts, storage, security and guest choices; add Shipping / Ask me first / mistake-derived agent rule; create SECURITY.md as an explicitly pending audit register. Reconcile Product Page and evidence summaries. No application or infrastructure changes.
2. **Authentication and secure storage — approved; foundation completed locally November 17.** Added supabase_api.py (stateless HTTPS, publishable key only), auth.py (per-object email/password/code/recovery/refresh/logout), archive.py (owner-scoped operations and validated snapshots), SQL migration with RLS/composite owner FKs and immutable reviews, rollback-only SQL security script, mocked tests and setup guidance. No new dependencies. No app.py integration, project provisioning or database execution. Local mocked checks do not prove deployed isolation; SQL/Auth/API tests remain pending before real saves.
3. **Library UI — approved; completed locally November 17.** Implemented entry/auth/recovery forms, private classes/projects/history, explicit saves, duplicate-save prevention, fresh revised-draft flow, identity/context clearing, unsaved-work prompts, pagination and confirmed deletion with changed-count reconfirmation. Added read-only SampleArchive (no cloud/model writes) and Load demo example (no model call/save/auto-consent). Cloud feature gate defaults false. 61 mocked Python / four analytics tests passed; local Chrome walkthrough and demo fill verified. Live Supabase wiring/security remains pending before actual saves.
4. **Audit, live deployment and evidence — pending approval.** Hosted two-account database/API proof is saved. Finish the remaining auth and app workflow checks, audit, request and spending controls, deployment, phone and live PostHog verification, and submission. Verify deployed Python and dependency compatibility.

## Acceptance and required security proof

- A student can sign in with Google (Google owns account recovery), create a class/project, run the existing review, explicitly save, sign out/in, and reopen the same snapshot without a new model call.
- Account B cannot list/read/update/delete A's synthetic records or create/reparent descendants under A's records, including direct API requests bypassing the UI. Forged owner IDs, expired tokens, and unauthenticated requests must not grant access. B can manage its own data; A's data remains unchanged after attacks.
- Capture a labeled, refused cross-account write for the required screenshot. Blocked reads can return zero rows; do not invent an HTTP error. Include own-account positive controls, expected/observed results, date and deployed version in the evidence log. Screenshots must contain no tokens/passwords/real coursework.
- Guest checks do not write coursework to the archive. Apply server-enforced request/concurrency and spend controls to public model actions; choose numeric limits before launch. With accounts, the assignment's required proof is the second-account test; the 30-call no-database alternative is not our lane's proof.
- Test ownership/cascade deletion, duplicate saves, storage failure, context switches and logout. Automated mocked tests establish app contracts, not deployed RLS or model quality.
- Inspect live phone layout, links, session expiry, and extraction-to-feedback flow. Verify live PostHog ingestion and replay masking of auth fields, class/project names, rubrics, drafts, feedback and saved history. Only fixed action names; no email, content, titles or record IDs in analytics. Current script labels the app local_app; resolve live labeling during implementation.

## Security audit and launch decisions still open

SECURITY.md tracks checks, actual findings, fixes and residual risks. Audit source/dependencies, Git secrets, auth/session isolation, all table privileges/RLS, parent ownership, guest bypass, injection/rendering, provider routing, analytics/log leakage, API abuse/cost, storage/deletion, hosting/secrets/HTTPS and recovery. A checklist or passing mocks alone does not establish a full audit.

Before launch verify service accounts/plans/quotas, hosting Python support, Google OAuth origin/audience settings, provider logging/retention, database backup/retention/deletion terms, numeric model limits/budget, and the known-good rollback revision. No pricing or availability promise is made here. No service created, paid plan selected, migration applied, or real coursework stored by batch 1.

Official implementation references: [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [Streamlit secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [Supabase Python auth](https://supabase.com/docs/reference/python/auth-api).

## Submission / classroom checklist

- [ ] Working live app URL, usable by a classmate on a phone.
- [ ] Note containing repository URL, Beginner lane, and repository SECURITY.md link.
- [ ] Completed audit: checks, findings, fixes and remaining risks.
- [x] [Refused two-account write screenshot](tests/evidence/supabase-two-account-isolation-2026-11-19.png) linked in the [security record](SECURITY.md#required-two-account-test--november-19).
- [ ] Live PostHog events and full masked session replay verified.
- [ ] PRD v3 and AGENTS.md reflect shipped behavior; unfinished items remain labeled.
- [ ] Bring phone November 24 for pod testing at the live address (user-supplied brief).

Existing journal lists November 23 at noon as the build deadline; this has not been reverified against the new brief. No assignment submission performed. Deferred: collaboration, shared classes, uploads, automatic comparisons, cross-project AI memory, and advanced-lane infrastructure.
