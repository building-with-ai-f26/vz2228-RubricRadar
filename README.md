# Rubric Radar

> **Know what's missing. Understand what matters. Submit stronger work.**

An AI-powered pre-submission coach for MBA students reviewing written reports and project submissions against assignment instructions or rubrics.

- **Builder:** `@victor-zu-97` (display name to confirm)
- **Pod:** 12
- **Product Page & Living PRD:** [Published Product Page](https://building-with-ai-f26.github.io/vz2228-RubricRadar/) · [Local source](./docs/index.html). GitHub Pages verified November 8.
- **Status:** PRD v1 reviewed; local text-only prototype implemented. The latest recorded suite passed 20 deterministic tests on November 4. Builder completed live reviews and confirmed the compact interface and revised requirement checks work; outside-user tests and public app deployment remain outstanding.
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

The 20 deterministic tests cover evidence checks, output coverage, input bounds, API failures, privacy request settings, and the Streamlit workflow with mocked responses. They do not establish model accuracy.

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

## Current Build 1 evidence status

On November 8, the builder completed a synthetic campus-coffee-shop review on application commit `0bd20d6` and supplied screenshots: 4 requirements, 3 Met, 1 Missing, and one required fix to add the omitted success metric. Screenshots are embedded in the Product Page. API cost and elapsed time were unreported; the recorded cost total remains partial. This single builder check does not establish broad model accuracy or independent usability. GitHub Pages was verified reachable and matched the then-current local page; the screenshot assets and embeds are included in this delivery update. The application remains local. The last recorded automated suite had 20 passes on November 4; it was not rerun today.

## Historical Build 1 evidence — November 3

Updated November 3, 2026. All 18 deterministic tests pass, including mocked UI flows, whitespace-tolerant source verification, output-budget configuration, and safe failure diagnostics. These tests verify application behavior, not model accuracy.

Live testing includes the original synthetic smoke check (3 requirements, $0.003135, 10.84 seconds combined API time) and two additional successful builder-run reviews with recorded usage:

| Run | Combined API time | Reported API cost | Evidence |
| --- | --- | --- | --- |
| Technology trends | 77.30 seconds | $0.01418914 | Builder confirmed review and priorities displayed. Feedback informed stricter rules against inferred requirements. |
| Project-update email | 55.22 seconds | $0.012247078 | 6 findings: 5 Met, 1 Partially Met. Builder confirmed summary, cards, and expandable details worked. |

The builder also confirmed a subsequent live run worked after prompt v1.2 removed ambiguity notes and focused judgments on explicit requirements; usage for that run was not supplied. These are builder checks, not independent target-user evaluation or evidence of broad model accuracy. Assignment text is not retained in this log.

Failures and changes: exact source matching rejected formatting differences; matching now tolerates whitespace while retaining original excerpts. Draft reviews exhausted the initial 7,000-token budget; a configurable 16,000-token default allowed the recorded reviews to complete. Incomplete responses now show safe diagnostics. Manual feedback prompted compact cards, a summary, expandable evidence, and removal of inferred conventions such as mandatory email greetings. Provider reasoning-token consumption remains unconfirmed.

Builder time: approximately 2 hours for this session, self-reported. Coding agent: Codex through a ChatGPT Plus subscription; no project-specific subscription cost allocation or separate agent charge was reported. Recorded API costs total $0.029571218 across the original smoke check and the two tabulated runs; today's two tabulated runs total $0.026436218. These are partial totals, excluding failed attempts, the final confirmation run, and any other unrecorded requests. Full project spending is not yet reconciled.

The builder visually checked the interface in the browser; agent browser access remained unavailable. Screenshot/GIF evidence, outside-classmate feedback, the ten-case Build 4 evaluation, and public deployment verification remain outstanding.
