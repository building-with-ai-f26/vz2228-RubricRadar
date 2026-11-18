# AGENTS.md — Coding Agent Operating Manual

> Give this file to your coding agent and check that it is using these instructions. Keep the stack, commands, and ground rules current.

## 1. Project Overview
- **What this repo builds:** Rubric Radar coaches MBA students reviewing written reports/projects against pasted instructions or rubrics. It provides requirement-linked evidence and up to three revision priorities.
- **Primary user & core workflow:** [See the living PRD in `docs/index.html`]
- **Current tech stack:** Python 3.14.4 (verified), Streamlit, OpenRouter API, jsonschema, python-dotenv, certifi; no database.
- **Build 3 plan:** Beginner lane; Streamlit Community Cloud + Supabase Auth/Postgres; private Class → Project → Saved reviews and Continue as guest. See PRD.md section 13 and Plan.md (resume point). Supersedes the local SQLite proposal. Batches 1–3 are implemented locally. November 18 Google sign-in batch is approved: Google Identity Services popup replaces email/password UI and exchanges a nonce-bound ID token through Supabase. Hosted schema installation succeeded November 18; SQL-role and two-account isolation tests remain unexecuted. Cloud sign-in/storage stays gated off until isolation is verified. No public app deployment; batch 4 still requires approval. See tests/README.md for current configuration and evidence.

## 2. Commands
- **Install dependencies:** `python3 -m venv .venv` then `.venv/bin/python -m pip install -r requirements.txt`
- **Run locally:** `.venv/bin/python -m streamlit run app.py` (http://127.0.0.1:8501)
- **Run deterministic tests:** `.venv/bin/python -m unittest discover -s tests -v`
- **Run analytics / Google component tests:** `node --test tests/test_analytics.cjs tests/test_google_signin.cjs` (Node.js required only for this check)
- **Preview Product Page locally:** `python3 -m http.server 8765 --bind 127.0.0.1 --directory docs`
- **Run model evals:** `.venv/bin/python tests/smoke_live.py` (synthetic, two billable API calls; full Build 4 eval not yet implemented)

### Structure and setup
- `app.py`: guest/project review inputs, confirmation, result invalidation and Load demo example. `app_style.css` and `.streamlit/config.toml` own the minimal local presentation/theme; use trusted static CSS only, keep coursework in native widgets. Read DESIGN.md for the established visual system before aesthetic changes; preserve structure, minimal navigation and class identity colors.
- `library_ui.py`: Google account entry, per-session navigation, cloud gate, private library/save/delete UI, unsaved-work and identity clearing.
- `feedback_ui.py`: shared read-only feedback renderer; `sample_library.py`: fixed synthetic read-only walkthrough and demo texts. Sample mode cannot save or call models.
- `radar.py`: OpenRouter requests, structured contracts, input bounds, and evidence checks.
- `supabase_api.py`, `auth.py`, `archive.py`: stateless cloud HTTP, per-session Google/Supabase auth, private archive foundation; `google_signin.py` and `google_signin/` render the official Google popup button with a server nonce. No automatic Google sign-in, browser token storage or app Google client secret; UI calls are gated by RUBRIC_RADAR_ARCHIVE_ENABLED (false by default). Standard library + existing dependencies only.
- `supabase/migrations/`, `supabase/tests_private_archive.sql`: schema/RLS migration (hosted installation succeeded November 18) and unexecuted rollback-only database security checks. Mocks do not prove SQL isolation. See `docs/setup/supabase.md` for setup and pending validation.
- `docs/index.html` and `docs/images/`: Product Page, living PRD summary, build log, and synthetic screenshots; published via GitHub Pages from `main` `/docs`.
- `docs/posthog.js`: Shared browser analytics and masked replay configuration, embedded by `app.py` and loaded by the Product Page. Initialization is guarded against Streamlit reruns.
- `tests/`: Mocked Python checks, analytics checks, synthetic live smoke script, and evidence log in `tests/README.md`.
- `PRD.md`, `Intent.md`, `README.md`, and `journal/`: Product definition, historical discovery, local launch guidance, and build notes.

Use Python 3.14.4 for the verified environment. After installing dependencies, copy `.env.example` to `.env` and set `OPENROUTER_API_KEY` locally. Keep `.env` untracked. Run Streamlit from the repo root and open `http://127.0.0.1:8501`. Model calls are billable; Python and analytics tests use mocks and do not call the model. The browser needs internet access to send analytics to the configured US PostHog project. Product Page edits take effect publicly only after publishing.

## 3. Non-Negotiable Engineering Rules
1. **Plan before coding:** Before touching multiple files, propose a brief plan and wait for approval.
2. **Small batches:** Make small, focused changes that can be reviewed and explained by a human in a single Pull Request.
3. **Explainability:** Avoid unnecessary abstractions or dependencies. Help the human builder understand the main components, what changed, why it matters, what could break, and how it was checked.
4. **Verify changes:** Run relevant checks. For a reproducible logic bug, use a failing test to demonstrate the fix when practical. Record manual checks and known limitations; follow the selected Build 4 evaluation track.
5. **Zero secrets in code:** Never hardcode API keys, tokens, or credentials. Always read from environment variables (`.env`) and update `.env.example` when new variables are needed.
6. **Stop when looping:** If a fix fails twice in a row, stop, summarize what failed, and ask the human before trying a third approach.

7. **Evidence check before every commit:** Review the Build 1 evidence status in `docs/index.html` before staging or committing. Record every automated test run, live evaluation, and builder/user manual test, including failures and recovery, in `tests/README.md`; summarize new evidence and outstanding items in the Build 1 log. Include the date, version/commit under test when known, method, outcome, limitations, and reported cost/time (mark unknown values as unreported). A suite run may be recorded as one entry with counts and failed test names; do not omit failed runs. Keep current evidence summaries in `Intent.md` and `PRD.md` consistent, preserving explicitly labeled historical checkpoints. Never store assignment text or secrets in evidence. Before committing, tell the user what evidence was updated, or explicitly state that no new test evidence exists; do not imply tests were rerun. Keep checking Build 1 status on every commit unless the user changes this instruction.

## 4. Prototype boundaries
- **Implemented boundary:** Guest inputs are session-only. Auth/archive UI is implemented but cloud access remains off until RUBRIC_RADAR_ARCHIVE_ENABLED is explicitly enabled after actual schema/RLS/two-account verification. Sample library is read-only synthetic data; Load demo example only replaces working inputs, resets consent and invalidates stale feedback. No real coursework archive writes before security verification. `radar.py` still owns provider calls/validation.
- Keep secret API keys in `.env`; never log assignment text. The current implementation must not persist coursework. After implementation approval, explicit Save project / Save review actions may persist only selected content in the owner's Supabase archive; guest checks must remain free of coursework archive writes. Disclose cloud storage, enforce ownership in database policies and parent relationships, and implement confirmed deletion and context isolation. Exclude local secrets, database dumps, databases and sidecar files from Git before creating them. The public PostHog browser project token in `docs/posthog.js` is intentionally client-visible; never put a personal API key there. Build 2 explicitly authorizes masked replay: keep all inputs and replay text masked, console/network-body capture off, and click events limited to fixed control names. Never send coursework in analytics.
- Require privacy-compatible provider routing; do not silently relax it if a provider is unavailable.
- Use mocked tests for UI and contracts; model accuracy requires separate live/human evaluation.
- Current limits: 12,000 instruction characters, 30,000 draft characters, 25 requirements, 90-second timeout per request. These are provisional bounds, not measured performance targets.

## 5. Shipping

- Selected lane: Beginner. Target Streamlit Community Cloud for the app; GitHub Pages remains the Product Page. Supabase Auth/Postgres project and schema are provisioned; live ownership proof remains pending. Resume from Plan.md and inspect current status before continuing.
- Before a release, run relevant Python/analytics checks and record every result, failure and recovery per section 3. Security-sensitive storage needs deployed two-account tests as well as mocked checks.
- Never expose coursework tables before grants, RLS and same-owner parent constraints are verified. Use the publishable key plus user token for routine app queries, never a service-role bypass. Keep auth sessions and coursework out of shared caches.
- Keep server credentials in host secrets. Verify runtime compatibility, HTTPS, phone workflow, cost controls, live PostHog events and fully masked replay. Record deployed revision/URL and a known-good code rollback; database migrations require a separate recovery plan.
- Complete SECURITY.md with actual checks, findings, fixes and residual risks. Pending work must not appear as passing. Update PRD v3 and Product Page to distinguish plans from shipped behavior before reporting delivery.

## 6. Ask me first

- Obtain approval for each new multi-file implementation batch; batches 1–3 are approved; batch 4 deployment/audit still needs approval.
- Ask before creating paid resources, choosing a paid plan, raising spending limits, or sending billable evaluation calls without session authorization.
- Ask before public deployment/publishing, remote pushes, destructive migrations or deletion of real saved user data unless that specific action is already authorized. Prepare a concrete reviewable result first. Normal user-confirmed in-app deletion is part of the approved future feature.
- Ask before changing explicit saves into automatic persistence, expanding sharing/retention/analytics, weakening privacy routing/RLS, or using real coursework for agent-run tests. Existing authorization persists; do not ask again for an already authorized action.

## 7. Rule from a real agent mistake

On November 15, an agent's PNG-only documentation check rejected a valid native JPEG screenshot; tests/README.md records the failure and recovery. **Inspect an artifact's actual format before validating or renaming it; never assume all screenshots use one format.** Preserve the original evidence bytes and update references consistently. This was a documentation validation mistake, not an application/model failure.
