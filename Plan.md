# Rubric Radar — Resume plan

## Build 4 — Resume November 25, 2026

**Due Monday, November 30 at noon ET.** Track A is selected. Commit `23718b2` is on `main` with prompt v1.3, PRD v4, the rubric, scorecard, and output examples. The same ten synthetic cases scored 36/40 before and 38/40 after. The paired runs used the app’s local review code with live OpenRouter calls. Hosted verification reached the landing page. [Scorecard](docs/index.html#build-4) · [Test evidence](tests/README.md#november-24--build-4-track-a)

1. **Outside-user walkthrough recorded.** The first MBA user testing outside class reported an output-token-limit error, addressed in `5ef1844`. The builder confirmed that the second user navigated the app on the builder’s laptop using the builder’s signed-in account. Their feedback on finding and identifying saved review output led to a project-level dropdown with assignment names and chronological draft numbers. [First report](tests/README.md#november-25--outside-target-user-feedback) · [Walkthrough confirmation](tests/README.md#november-25--build-4-walkthrough-and-builder-time)
2. **Public release verified.** Release `8ddfea7` rolled out on November 25. The Product Page showed the scorecard, the hosted sample reopened Draft 1, and one synthetic guest review completed on v1.3. PostHog received the confirmation event and masked the guest inputs and feedback in replay. Signed-in live saves and replay remain open. Get approval before any additional agent-run billable model calls. [Hosted verification](tests/README.md#november-25--build-4-hosted-release-verification) · [Public Product Page](https://building-with-ai-f26.github.io/vz2228-RubricRadar/#build-4) · [Live app](https://rubricradar.streamlit.app/)
3. **Second-day commit and hours recorded.** Commit `8ddfea7` is dated November 25. The builder reported three total hours across this week’s Build 4 work sessions. Recorded inference totals $0.0428488004 across the scored evaluation and the hosted verification review.
4. **Prepare the submission.** Capture a screenshot of the scorecard. Submit the Product Page URL and include Track A, the live app URL, the GitHub repo link, and two or three sentences about what testing changed. [Build 4 brief](https://www.icerynk.com/content/build-4-test-py-tests-model-evals?course=fa26-tech-gb-2160-dm2-f2)

The rerun’s known defects are a skipped priority in M1 and stray extraction status labels in N4.

## Build 3 — Beginner lane: private saved reviews

Updated November 22, 2026. Start here when you return.

### Build 3 resume notes

**Verified.** The local runtime was restored. Hosted Supabase passed SQL-role, anonymous access and two-account isolation checks. The hosted expired-token check and app workflow with synthetic feedback passed, including guest no-write behavior and fixture cleanup. Batch 4 local checks passed 63 Python and seven Node tests. [Test log](tests/README.md#november-19--batch-4-local-release-audit-and-controls) · [Refused-write screenshot](tests/evidence/supabase-two-account-isolation-2026-11-19.png)

**Current environment.** [Rubric Radar is live on Streamlit Community Cloud](https://rubricradar.streamlit.app/). The hosted archive is enabled and the local archive gate remains off. Google OAuth is External/Testing and authorizes the hosted HTTPS origin plus the two local origins. Host secrets were configured. [Guest review and sign-in evidence](tests/README.md#november-22--public-deployment-and-one-live-guest-review)

### November 22 release checkpoint

**Public startup verified November 22.** The first attempt stopped at the GitHub access check. The retry after the professor approved Streamlit access deployed `app.py` from `main`, which tracked candidate `ac76d6b`. The host log displayed Python 3.14.10, installed dependencies, and startup on `127.0.0.1:8501`. The public HTTPS landing page loaded in an incognito Chrome window. Hosted desktop checks verified guest demo fill with consent off, the unsaved-work discard prompt, and opening a read-only sample review. The host had no model key or archive access during these checks. Inference cost $0. Active builder time and other costs unreported. [First attempt](tests/README.md#november-22--community-cloud-deployment-attempt) · [Audit register](SECURITY.md)

1. **Close the remaining audit requirements.** Search browser-delivered code for secret keys, document the manual Supabase backup and monthly provider cap, and run the requested `pip-audit` or document how the existing OSV audit maps to the brief. The current paid-call limiter is shared per process. The brief asks for per-visitor limits on paid calls and database writes, which remain an implementation gap. Update SECURITY.md with evidence and remaining issues.

   The builder deferred the per-visitor implementation for the submission. The proposed $0.50 budget and separate archive write limit remain future work.
2. **Verify classmate access and analytics.** The desktop guest review and builder's hosted Google sign-in passed. A classmate's account, phone workflow from extraction to feedback, live archive save/reopen, and PostHog `live_app` events and replay masking remain unverified. Use synthetic content. The builder authorized one billable example and it is complete. Obtain approval before additional model calls.
3. **Finish release documentation and submit.** Update PRD v3, the AGENTS.md Shipping section, and the Product Page Build 3 log with shipped behavior, failures, spend and hours. In Icerynk, put the live URL in the Link box, paste the repository, Beginner lane and SECURITY.md in the note, and attach the actual blocked-request screenshot. No assignment has been submitted.

### What is ready locally

- Guest review and gated Google sign-in, private classes/projects/history, explicit save/delete controls, pagination and context clearing.
- Read-only synthetic sample and Load demo example. Explore both with `.venv/bin/python -m streamlit run app.py` at `http://127.0.0.1:8501`.
- Existing desktop and 400px/768px browser previews. Native form autocomplete warnings, broader accessibility testing and real-device checks remain open.

Suggested resume message: **“Open Plan.md and continue the live Build 3 workflow checks on Streamlit.”**

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
4. **Audit, live deployment and evidence — in progress.** The public Streamlit deployment passed startup, guest demo fill, the sample walkthrough, one guest review, and the builder's Google sign-in. Hosted archive save/reopen, phone, and analytics verification remain pending.

## Acceptance and required security proof

- A student can sign in with Google (Google owns account recovery), create a class/project, run the existing review, explicitly save, sign out/in, and reopen the same snapshot without a new model call.
- Account B cannot list/read/update/delete A's synthetic records or create/reparent descendants under A's records, including direct API requests bypassing the UI. Forged owner IDs, expired tokens, and unauthenticated requests must not grant access. B can manage its own data; A's data remains unchanged after attacks.
- Capture a labeled, refused cross-account write for the required screenshot. Blocked reads can return zero rows; do not invent an HTTP error. Include own-account positive controls, expected/observed results, date and deployed version in the evidence log. Screenshots must contain no tokens/passwords/real coursework.
- Guest checks do not write coursework to the archive. Apply server-enforced request/concurrency and spend controls to public model actions; choose numeric limits before launch. With accounts, the assignment's required proof is the second-account test; the 30-call no-database alternative is not our lane's proof.
- Test ownership/cascade deletion, duplicate saves, storage failure, context switches and logout. Automated mocked tests establish app contracts, not deployed RLS or model quality.
- Inspect live phone layout, links, session expiry, and extraction-to-feedback flow. Verify live PostHog ingestion and replay masking of auth fields, class/project names, rubrics, drafts, feedback and saved history. Only fixed action names; no email, content, titles or record IDs in analytics. Streamlit Community Cloud subdomains use the `live_app` label in the local release candidate; verify live ingestion after deploy.

## Security audit and launch decisions still open

SECURITY.md tracks checks, actual findings, fixes and residual risks. Audit source/dependencies, Git secrets, auth/session isolation, all table privileges/RLS, parent ownership, guest bypass, injection/rendering, provider routing, analytics/log leakage, API abuse/cost, storage/deletion, hosting/secrets/HTTPS and recovery. A checklist or passing mocks alone does not establish a full audit.

Before launch verify service accounts/plans/quotas, hosting Python support, Google OAuth origin/audience settings, provider logging/retention, database backup/retention/deletion terms, numeric model limits/budget, and the known-good rollback revision. No pricing or availability promise is made here. No service created, paid plan selected, migration applied, or real coursework stored by batch 1.

Official implementation references: [Streamlit deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [Streamlit secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management), [Supabase RLS](https://supabase.com/docs/guides/database/postgres/row-level-security), [Supabase Python auth](https://supabase.com/docs/reference/python/auth-api).

## Submission / classroom checklist

### Submission draft

> **Rubric Radar · Build 3 · Beginner lane**
>
> [Live app](https://rubricradar.streamlit.app/)
>
> One live synthetic guest review and the builder's Google sign-in passed. The hosted Supabase two-account test verified own-account access and blocked cross-account reads and writes.
>
> [Course repository](https://github.com/building-with-ai-f26/vz2228-RubricRadar) · [Security audit](https://github.com/building-with-ai-f26/vz2228-RubricRadar/blob/main/SECURITY.md) · [Refused cross-account write screenshot](https://github.com/building-with-ai-f26/vz2228-RubricRadar/blob/main/tests/evidence/supabase-two-account-isolation-2026-11-19.png)

- [ ] Working live app URL, usable by a classmate on a phone.
- [x] Draft note containing repository URL, Beginner lane, and repository SECURITY.md link.
- [ ] Completed audit: checks, findings, fixes and remaining risks.
- [x] [Refused two-account write screenshot](tests/evidence/supabase-two-account-isolation-2026-11-19.png) linked in the [security record](SECURITY.md#required-two-account-test--november-19).
- [ ] Live PostHog events and full masked session replay verified.
- [ ] PRD v3 and AGENTS.md reflect shipped behavior; unfinished items remain labeled.
- [ ] Bring phone November 24 for pod testing at the live address (user-supplied brief).

The Icerynk brief was checked November 22. Build 3 is due Monday, November 23 at noon New York time, with phone pod testing on November 24. Deferred: collaboration, shared classes, uploads, automatic comparisons, cross-project AI memory, and advanced-lane infrastructure.
