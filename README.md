# Rubric Radar

> **Know what's missing. Understand what matters. Submit stronger work.**

An AI-powered pre-submission coach for MBA students reviewing written reports and project submissions against assignment instructions or rubrics.

- **Builder:** `@victor-zu-97` (display name to confirm)
- **Pod:** 12
- **Product Page & Living PRD:** [Local page](./docs/index.html); GitHub Pages deployment has not been verified.
- **Status:** PRD v1 reviewed; local text-only prototype implemented. One live synthetic DeepSeek review passed structural checks; no user tests or public deployment yet.
- **Full PRD:** [PRD.md](./PRD.md)

The MVP uses pasted instructions and draft text, student-confirmed requirements, evidence-backed findings, and up to three prioritized improvements. PDF uploads and saved revision comparisons are deferred.

The app is planned to run locally through Week 4; add a cloud URL in Build 5.

## Start here: Build 1

**Due Monday, November 9 at noon, New York time.** No class November 3; keep building that week.

1. Join the [class organization](https://github.com/building-with-ai-f26), then use this template to create a **public** repo named `<netid>-<project-slug>`. Ask Christian or Hew if the organization is missing from the owner list.
2. Set up Git and one coding agent during the week of October 27. Follow the [Icerynk setup guide](https://www.icerynk.com/c/fa26-tech-gb-2160-dm2-f2/content/pre-class-setup-github-openrouter-your-coding-agent).
3. Publish [`docs/index.html`](./docs/index.html): **Settings → Pages → Deploy from a branch → main → /docs → Save**. When deployment finishes, open `https://building-with-ai-f26.github.io/<your-repo-name>/`.
4. Fill in PRD v1: a reachable user, their painful before/after workflow, one core workflow, and three non-goals.
5. Build a rough local prototype. Add a screenshot or GIF and an honest Build 1 log to the Product Page, including progress, learning, problems, costs, and hours.
6. Push meaningful commits on **at least two separate days each week outside class**, including the November 3 break.
7. Submit your **Product Page URL and repository URL in Icerynk**. Come ready to demo the prototype in two minutes on November 10.

Create your PostHog account in Week 1. Install it on the Product Page and local app in **Build 2**, then verify events. The Product Page is public from Build 1; the app can stay local through Week 4.

## Repository map

| File / folder | Purpose |
| --- | --- |
| [`docs/index.html`](./docs/index.html) | Required public pitch, living PRD, and weekly build log. Update with actual work and evidence. |
| [`PRD.md`](./PRD.md) | Full PRD v1, acceptance criteria, evaluation plan, and proposed architecture. |
| [`Intent.md`](./Intent.md), [`Plan.md`](./Plan.md), [`journal/`](./journal/) | Optional drafting aids. No duplicate submission is required. |
| [`AGENTS.md`](./AGENTS.md) | Local run commands, project context, and agent rules. Build 2 onward. |
| [`tests/`](./tests/) | Verification guidance. Build 4 offers Track A domain evals **or** Track B user replays. |
| [`SPONSOR_MEMO.md`](./SPONSOR_MEMO.md) | One-page recommendation backed by actual usage, full costs, and risks. Due December 14 at noon. |

[Icerynk](https://www.icerynk.com/c/fa26-tech-gb-2160-dm2-f2/content) holds the assignment instructions and submissions.

## Local setup

Verified on Python 3.14.4. From the repository folder:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
```

If `.env` already exists, edit it rather than overwriting it. Set `OPENROUTER_API_KEY` locally; never paste or commit credentials. The default configurable model is `deepseek/deepseek-v4.1-flash` via OpenRouter. Draft reviews default to a 16,000-token output budget; extraction remains at 7,000. Set `OPENROUTER_REVIEW_MAX_TOKENS` (1–32,000) to adjust the review budget. Higher budgets may increase latency and cost; the 90-second request timeout still applies. Restart the app after changing configuration.

```bash
.venv/bin/python -m streamlit run app.py
```

Open **http://127.0.0.1:8501**. The app binds to localhost. Paste instructions and a draft, consent to provider processing, extract and edit requirements, confirm, then review. Blank lines define draft paragraphs. Provisional limits: 12,000 instruction characters, 30,000 draft characters, 25 requirements, and 90 seconds per API request. Inputs are never silently truncated.

## Verification

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

The 12 deterministic tests cover evidence checks, output coverage, input bounds, API failures, privacy request settings, and the Streamlit workflow with mocked responses. They do not establish model accuracy.

For a live synthetic feasibility check (two billable model calls):

```bash
.venv/bin/python tests/smoke_live.py
```

It prints operational metadata and statuses, not assignment text. Review the intentionally absent implementation risks manually. The required Build 4 ten-case evaluation remains outstanding.

## Data handling and limitations

- Assignment text lives in current-session server memory; no database, text logs, caching, or analytics are configured. Use **Clear this session** to reset inputs and results. Do not expose this development server publicly.
- Requests send text to OpenRouter and a model provider. They require `data_collection: deny`, `zdr: true`, and parameter-compatible routing. If no eligible provider exists, the review fails rather than relaxing these controls.
- OpenRouter account logging and data-use settings must still be verified before real coursework. These routing settings are not a blanket guarantee about every intermediary. See [data collection](https://openrouter.ai/docs/guides/privacy/data-collection) and [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection).
- Met/Partially Met evidence is checked against exact paragraph text. Unverified evidence becomes Needs Review and linked recommendations are withheld. Semantic correctness still requires human review.
- No grade predictions, course-material verification, PDF input, saved history, or automatic comparisons.

## Build 1 evidence status

Local implementation and mocked-flow tests are complete. One live synthetic review completed using DeepSeek V4.1 Flash: 3 requirements, 2 Met, 1 Missing, and 1 recommendation. Reported inference cost was $0.003135; API durations totaled 10.84 seconds. This is one small feasibility result, not a quality evaluation or performance guarantee. Browser visual verification, a screenshot/GIF, and classmate feedback remain outstanding. Browser capture was blocked by unavailable browser access and computer-use permission. No prototype screenshot or broad model-quality result is claimed. Actual builder time and coding-agent costs have not been supplied.
