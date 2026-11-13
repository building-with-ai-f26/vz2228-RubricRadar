# AGENTS.md — Coding Agent Operating Manual

> Give this file to your coding agent and check that it is using these instructions. Keep the stack, commands, and ground rules current.

## 1. Project Overview
- **What this repo builds:** Rubric Radar coaches MBA students reviewing written reports/projects against pasted instructions or rubrics. It provides requirement-linked evidence and up to three revision priorities.
- **Primary user & core workflow:** [See the living PRD in `docs/index.html`]
- **Tech stack:** Python 3.14.4 (verified), Streamlit, OpenRouter API, jsonschema, python-dotenv, certifi; no database.

## 2. Commands
- **Install dependencies:** `python3 -m venv .venv` then `.venv/bin/python -m pip install -r requirements.txt`
- **Run locally:** `.venv/bin/python -m streamlit run app.py` (http://127.0.0.1:8501)
- **Run deterministic tests:** `.venv/bin/python -m unittest discover -s tests -v`
- **Run analytics tests:** `node --test tests/test_analytics.cjs` (Node.js required only for this check)
- **Preview Product Page locally:** `python3 -m http.server 8765 --bind 127.0.0.1 --directory docs`
- **Run model evals:** `.venv/bin/python tests/smoke_live.py` (synthetic, two billable API calls; full Build 4 eval not yet implemented)

### Structure and setup
- `app.py`: Streamlit inputs, session state, requirement confirmation, and feedback UI.
- `radar.py`: OpenRouter requests, structured contracts, input bounds, and evidence checks.
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
- `app.py`: session-only UI; `radar.py`: provider requests and output/evidence validation.
- Keep secret API keys in `.env`; never log or persist assignment text. The public PostHog browser project token in `docs/posthog.js` is intentionally client-visible; never put a personal API key there. Build 2 explicitly authorizes masked replay: keep all inputs and replay text masked, console/network-body capture off, and click events limited to fixed control names. Never send coursework in analytics.
- Require privacy-compatible provider routing; do not silently relax it if a provider is unavailable.
- Use mocked tests for UI and contracts; model accuracy requires separate live/human evaluation.
- Current limits: 12,000 instruction characters, 30,000 draft characters, 25 requirements, 90-second timeout per request. These are provisional bounds, not measured performance targets.
