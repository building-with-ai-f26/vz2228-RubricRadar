# Build 3 — Beginner lane: private saved reviews

Updated November 17, 2026. This is the resume point for the next session.

## Resume here

November 17 checkpoint: the builder requested committing and pushing all current project work to origin/main. This plan, code, setup guides, design rules, audit register and test evidence are included in that checkpoint. Actual commit/push success must be verified from Git; this text was prepared before the commit.

### What is ready

- Beginner lane selected; batches 1–3 approved and implemented locally: guest entry, gated email auth/recovery, private Class → Project → Saved reviews UI, explicit saves/deletion, history, pagination and context isolation.
- Read-only synthetic sample: three classes, each with a project/review. Load demo example fills both editor fields, clears stale feedback/save state and unchecks consent; loading never calls the model or saves coursework.
- Minimal aesthetics and class accents refined using Impeccable 4.9.2 guidance. Preserve the current structure and minimal navigation; read DESIGN.md before changing aesthetics.
- Backend auth/archive modules and SQL migration/rollback-only security script are prepared. No database migration has run and no Supabase project is configured. RUBRIC_RADAR_ARCHIVE_ENABLED remains false.
- Latest recorded Python suite: 61 passed in 5.543 seconds. Latest analytics suite: four passed in 215.334 ms, before styling-only edits. No application/analytics suite rerun for this commit preparation. Desktop, 400px and 768px Chrome previews were inspected; real-phone and full live replay checks remain pending.

### Next session

1. Read AGENTS.md, this resume point, DESIGN.md and SECURITY.md; inspect Git status so new user edits are preserved.
2. Builder creates their Supabase account/project using [account setup](docs/setup/supabase-account.md), then confirms it is ready. Credentials go only in ignored local/host settings, not chat or Git.
3. Follow [technical setup](docs/setup/supabase.md): review/apply the schema in the intended disposable/test environment, execute the SQL tests and real two-account direct API isolation checks, configure email confirmation/recovery, and document observed failures/results. Keep real coursework saves disabled until ownership isolation is verified.
4. Batch 4 full audit/public deployment needs a brief plan and approval. Complete request/spend protection, live PostHog/replay checks, phone test and refused-security-test screenshot before submission. SECURITY.md remains an incomplete audit.

Known follow-ups: native form fields produce empty-autocomplete warnings; dark override, exhaustive keyboard/screen-reader/long-content and real-device checks are not complete. SQL and real Auth/API/email behavior remain unverified. No automatic Impeccable detector/hooks were run. The skill is installed globally at ~/.codex/skills/impeccable on this Mac (launcher permission repaired); it is not vendored in this repository. New machines can install it from the official [Impeccable site](https://impeccable.style/).

### Reopen locally

Run `.venv/bin/python -m streamlit run app.py`, then open http://127.0.0.1:8501. A server was left running at the last checkpoint, but it may need restarting after logging back in. Explore sample library → Open class → Open project → Open saved review; or Continue as guest → Load demo example. Consent and the two review actions are still required for a billable live review. Restart after imported-module changes if hot reload retains an old module.

Suggested resume message: **“Open Plan.md and continue Rubric Radar Build 3 from the next pending step.”** GitHub Pages hosts the separate Product Page; the Streamlit app has no public URL yet. Pushing this checkpoint does not deploy the Python app or apply database migrations.

## Decisions

- Public app: Streamlit Community Cloud; keep the Python/Streamlit review UI and OpenRouter backend. GitHub Pages continues to host the separate Product Page, not the Python app.
- Accounts: Supabase Auth, initially email/password with email verification and password recovery. Supabase handles credentials; never store passwords in app tables or logs. Verify email delivery, redirects, token refresh, expiry, and logout before release.
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
4. **Audit, live deployment and evidence — pending approval.** Run and record the security audit, address findings, deploy, verify on phone and with two accounts, inspect live PostHog event payloads and masked replay, reconcile SECURITY.md/PRD/evidence and prepare submission. Verify deployed Python/dependency compatibility. No claim of completion until observed.

## Acceptance and required security proof

- A student can register/verify/sign in, recover access, create a class/project, run the existing review, explicitly save, sign out/in, and reopen the same snapshot without a new model call.
- Account B cannot list/read/update/delete A's synthetic records or create/reparent descendants under A's records, including direct API requests bypassing the UI. Forged owner IDs, expired tokens, and unauthenticated requests must not grant access. B can manage its own data; A's data remains unchanged after attacks.
- Capture a labeled, refused cross-account write for the required screenshot. Blocked reads can return zero rows; do not invent an HTTP error. Include own-account positive controls, expected/observed results, date and deployed version in the evidence log. Screenshots must contain no tokens/passwords/real coursework.
- Guest checks do not write coursework to the archive. Apply server-enforced request/concurrency and spend controls to public model actions; choose numeric limits before launch. With accounts, the assignment's required proof is the second-account test; the 30-call no-database alternative is not our lane's proof.
- Test ownership/cascade deletion, duplicate saves, storage failure, context switches and logout. Automated mocked tests establish app contracts, not deployed RLS or model quality.
- Inspect live phone layout, links, session expiry, and extraction-to-feedback flow. Verify live PostHog ingestion and replay masking of auth fields, class/project names, rubrics, drafts, feedback and saved history. Only fixed action names; no email, content, titles or record IDs in analytics. Current script labels the app local_app; resolve live labeling during implementation.

## Security audit and launch decisions still open

SECURITY.md tracks checks, actual findings, fixes and residual risks. Audit source/dependencies, Git secrets, auth/session isolation, all table privileges/RLS, parent ownership, guest bypass, injection/rendering, provider routing, analytics/log leakage, API abuse/cost, storage/deletion, hosting/secrets/HTTPS and recovery. A checklist or passing mocks alone does not establish a full audit.

Before launch verify service accounts/plans/quotas, hosting Python support, Supabase email delivery/redirects, provider logging/retention, database backup/retention/deletion terms, numeric model limits/budget, and the known-good rollback revision. No pricing or availability promise is made here. No service created, paid plan selected, migration applied, or real coursework stored by batch 1.

Official implementation references: [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [Streamlit secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [Supabase Python auth](https://supabase.com/docs/reference/python/auth-api).

## Submission / classroom checklist

- [ ] Working live app URL, usable by a classmate on a phone.
- [ ] Note containing repository URL, Beginner lane, and repository SECURITY.md link.
- [ ] Completed audit: checks, findings, fixes and remaining risks.
- [ ] Screenshot of the refused two-account security test, linked to its evidence record.
- [ ] Live PostHog events and full masked session replay verified.
- [ ] PRD v3 and AGENTS.md reflect shipped behavior; unfinished items remain labeled.
- [ ] Bring phone November 24 for pod testing at the live address (user-supplied brief).

Existing journal lists November 23 at noon as the build deadline; this has not been reverified against the new brief. No assignment submission performed. Deferred: collaboration, shared classes, uploads, automatic comparisons, cross-project AI memory, and advanced-lane infrastructure.
