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
- **Run model evals:** `.venv/bin/python tests/smoke_live.py` (synthetic, two billable API calls; full Build 4 eval not yet implemented)

## 3. Non-Negotiable Engineering Rules
1. **Plan before coding:** Before touching multiple files, propose a brief plan and wait for approval.
2. **Small batches:** Make small, focused changes that can be reviewed and explained by a human in a single Pull Request.
3. **Explainability:** Avoid unnecessary abstractions or dependencies. Help the human builder understand the main components, what changed, why it matters, what could break, and how it was checked.
4. **Verify changes:** Run relevant checks. For a reproducible logic bug, use a failing test to demonstrate the fix when practical. Record manual checks and known limitations; follow the selected Build 4 evaluation track.
5. **Zero secrets in code:** Never hardcode API keys, tokens, or credentials. Always read from environment variables (`.env`) and update `.env.example` when new variables are needed.
6. **Stop when looping:** If a fix fails twice in a row, stop, summarize what failed, and ask the human before trying a third approach.

## 4. Prototype boundaries
- `app.py`: session-only UI; `radar.py`: provider requests and output/evidence validation.
- Keep API keys in `.env`; never log or persist assignment text. Do not add analytics text capture or replay recording.
- Require privacy-compatible provider routing; do not silently relax it if a provider is unavailable.
- Use mocked tests for UI and contracts; model accuracy requires separate live/human evaluation.
- Current limits: 12,000 instruction characters, 30,000 draft characters, 25 requirements, 90-second timeout per request. These are provisional bounds, not measured performance targets.
