**Current checkpoint — November 18:** Google sign-in replaces email/password/code accounts. Google OAuth branding and a Web client are configured under the builder's NYU Google account in the existing My First Project (creation of a new project outside the school organization was refused). Allowed origins are localhost:8501 and 127.0.0.1:8501 only; audience is External/Testing with the builder's NYU account added as one test user. Supabase shows Google enabled and Email disabled; nonce checks were kept on. Hosted schema installation succeeded. Local ignored .env has the project URL, publishable key and Google client ID; existing provider key was preserved. Archive gate stays false. No live Google login, SQL-role/two-account security test, public app deployment or publication was performed. Earlier differing checkpoints below are historical. Setup: docs/setup/google-signin.md; evidence: tests/README.md.

# Rubric Radar

**PostHog events screenshot captured — November 15:** Agent captured PostHog Activity → Events in the sixth Chrome tab on November 15. Last-hour list showed three local-app events at http://127.0.0.1:8501/: one Pageview and two ui_clicked, with recording links on the click rows. This verifies received local-app events; it does not inspect event properties or independently verify public-page traffic. Public-page analytics and complete feedback replay remain builder-confirmed complete. The events screenshot is ready to attach to the Build 2 submission. [Events screenshot](docs/images/posthog-events-2026-11-15.jpg).

**Build 2 completion clarification — November 15:** Builder confirmation, November 15: published Product Page analytics and today’s complete replay through feedback/masking are completed. These are builder-reported checks; the agent did not independently replay today’s session or inspect public-page event properties in this step. The still screenshot remains evidence of session activity and the displayed masked replay.

Current Icerynk Build 2 brief verified November 15: working real AI/API action shown on the Product Page; PostHog pageviews/clicks/replay on page and app; PRD v2 covering biggest risk, test, architecture and cost/run; AGENTS.md setup/structure; two outside-class commit dates and updated progress/lessons/problems/costs/hours. Submission is Product Page link, repo link, and a PostHog screenshot showing events; bring the running laptop app to pod testing. Weekly budgets, account-setting confirmation and pod names/sign-off are optional project follow-ups, not stated Build 2 submission requirements. Learn with AI is explicitly ungraded; a documented synthetic reference test is useful quality work, not an additional stated Build 2 requirement. [Assignment brief](https://www.icerynk.com/content/build-2-plan-md-smallest-version-live?course=fa26-tech-gb-2160-dm2-f2). Submission evidence now includes an agent-captured events screenshot and the builder-supplied replay screenshot. Earlier pending checklists below describe previous checkpoints and are superseded by this clarification.

**Latest Build 2 evidence — November 15, 2026:** November 15 builder review completed: extraction 18.70 seconds / $0.00229428; evaluation 19.69 seconds / $0.00278643; total 38.39 seconds / $0.00508071, model deepseek/deepseek-v4.1-flash, prompt v1.2. Builder confirmed the feedback worked. This is one builder assessment, not independent accuracy validation; reference expectations and findings were not supplied. The supplied PostHog screenshot shows today’s replay entry (11 minutes ago), an older entry (2 days ago), and one recently active recording. The selected older replay visibly masks app text. Today’s recording is present; complete playback through today’s feedback and event properties are not established by this still image. Published-page analytics and full feedback replay are now builder-confirmed complete; see confirmation below.

Updated Build 2 elapsed session time: 76.546 minutes (1.28 hours) through November 15, 12:23:48.017 p.m. America/New_York, across three non-overlapping recorded windows. Includes gaps and agent activity; not verified active builder effort. Excludes the break between the two November 15 sessions and work after the cutoff. Supersedes the earlier 0.67-hour snapshot; the historical approximately two-hour Build 1 estimate is separate. See [screenshot](docs/images/posthog-session-replay-2026-11-15.png) and [detailed evidence](tests/README.md). No application or analytics suites rerun for this update.

> **Know what's missing. Understand what matters. Submit stronger work.**

An AI-powered pre-submission coach for MBA students reviewing written reports and project submissions against assignment instructions or rubrics.

- **Builder:** `@victor-zu-97` (display name to confirm)
- **Pod:** 12
- **Product Page & Living PRD:** [Published Product Page](https://building-with-ai-f26.github.io/vz2228-RubricRadar/) · [Local source](./docs/index.html). GitHub Pages verified November 8.
- **Status:** PRD v3 / Beginner lane. Batch 3 local UI implemented: guest entry, gated auth/recovery and private library screens, read-only sample and Load demo example. Cloud sign-in/saves remain off until actual database verification. Latest checks: 61 mocked Python and four analytics tests passed; local Chrome sample/demo walkthrough verified. Supabase project setup, live security/email, phone/replay and deployment pending.
- **Full PRD:** [PRD.md](./PRD.md)

The MVP uses pasted instructions and draft text, student-confirmed requirements, evidence-backed findings, and up to three prioritized improvements. PDF uploads and saved revision comparisons are deferred.

**Local preview:** The November 17 minimal design pass adds a compact top bar, no sidebar, quiet secondary actions and neutral class/project cards. Existing 61 Python tests passed; Home/My classes checked in Chrome. Open http://127.0.0.1:8501 after launching. Choose **Explore sample library → Open class → Open project → Open saved review** for a read-only synthetic walkthrough. Choose **Continue as guest → Load demo example** to fill a synthetic rubric and draft; consent stays unchecked and no automatic model call/save occurs.

**Cloud access gated:** Sign-in and real saves stay disabled until the database security checks pass. Builder creates the account/project using [Supabase account steps](./docs/setup/supabase-account.md); [technical setup](./docs/setup/supabase.md), [Plan.md](./Plan.md) and [SECURITY.md](./SECURITY.md) cover the next stages. No migration or real cloud saves have occurred.

Build 3 targets Streamlit Community Cloud; the live app URL is pending. GitHub Pages hosts only the separate Product Page.

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
| [`PRD.md`](./PRD.md) | Full PRD v3, acceptance criteria, evaluation plan, current architecture, analytics, and cost evidence. |
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

If `.env` already exists, edit it rather than overwriting it. Set `OPENROUTER_API_KEY` locally; never paste or commit credentials. The default configurable model is `deepseek/deepseek-v4.1-flash` via OpenRouter. Draft reviews default to a 50,000-token output budget. Extraction has a 10,000-token budget. An explicit `OPENROUTER_REVIEW_MAX_TOKENS` setting (1–50,000) overrides the review default. Higher budgets may increase latency and cost. The 90-second request timeout still applies. Restart the app after changing configuration.

```bash
.venv/bin/python -m streamlit run app.py
```

Open **http://127.0.0.1:8501**. The app binds to localhost. Choose Continue as guest, then paste instructions and a draft, consent to provider processing, extract and edit requirements, confirm, then review. Blank lines define draft paragraphs. Provisional limits: 12,000 instruction characters, 30,000 draft characters, 25 requirements, and 90 seconds per API request. Inputs are never silently truncated.

## Verification

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m pip check
```

The 61 deterministic tests cover the original review/evidence contracts, cloud transport/auth/archive, sample/demo, account/navigation/save/history and deletion UI contracts. Provider/cloud responses are mocked. They do not establish model accuracy, deployed RLS, email delivery or live API behavior. The unexecuted SQL security script and setup steps are in docs/setup/supabase.md.

For a live synthetic feasibility check (two billable model calls):

```bash
.venv/bin/python tests/smoke_live.py
```

It prints operational metadata and statuses, not assignment text. Review the intentionally absent implementation risks manually. The required Build 4 ten-case evaluation remains outstanding.

## Data handling and limitations

- Assignment text lives in current-session server memory; no database, text logs, or caching are configured. PostHog tracks pageviews and fixed-name clicks and records masked replay on the Product Page and local app. Inputs and replay text are configured to be masked; console and network-body capture are off. Initial synthetic replay masking was observed November 13; complete feedback replay verification remains pending. Use **Clear this session** to reset inputs and results. Do not expose this development server publicly.
- Requests send text to OpenRouter and a model provider. They require `data_collection: deny`, `zdr: true`, and parameter-compatible routing. If no eligible provider exists, the review fails rather than relaxing these controls.
- OpenRouter account logging and data-use settings must still be verified before real coursework. These routing settings are not a blanket guarantee about every intermediary. See [data collection](https://openrouter.ai/docs/guides/privacy/data-collection) and [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection).
- Met/Partially Met evidence is checked against exact paragraph text. Unverified evidence becomes Needs Review and linked recommendations are withheld. Semantic correctness still requires human review.
- No grade predictions, course-material verification, PDF input, saved history, or automatic comparisons.

## Historical Build 1 evidence — November 8

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
