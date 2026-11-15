# Verification: Tests, Evals & User Feedback

Review agent changes and verify that the product works throughout the course. Use automated tests for application behavior when useful, model evals for output quality, and manual checks for the user experience. A test shows what it checked; record its limits.

## Build 4: choose one track

**Track A — Domain quality**

Define 3–4 rules for good output. Evaluate 10 cases: 5 normal, 3 messy, and 2 adversarial. Compare results before and after improvements, and ask one outside target user to review the result.

**Track B — User friction**

Watch 3–5 outside users try the product without coaching. Review PostHog replays, identify the top three friction points, and document fixes with before/after evidence. The app can still run locally.

Both tracks update PRD v4 and the build log on `docs/index.html`. Follow [Icerynk Build 4](https://www.icerynk.com/c/fa26-tech-gb-2160-dm2-f2/content/build-4-test-py-tests-model-evals) for the rubric. You do not need to complete both tracks.

## Current local prototype checks

Run `.venv/bin/python -m unittest discover -s tests -v` from the repository root. The 20 tests use synthetic inputs and mocked provider responses; they check contracts, quotation integrity, privacy request flags, and UI state/error behavior, not AI judgment quality.

Run `.venv/bin/python tests/smoke_live.py` with a configured local `.env` for a synthetic live review. It makes two billable provider calls and prints metadata/statuses without draft text. This is a feasibility check, not completion of Track A. No classmate coursework is included in the repository.

### November 15 pre-commit delivery review

Version: documentation working tree based on `e7237eb`. Reviewed the Build 1 evidence status in docs/index.html before staging, and reviewed the pending eight-file documentation diff and repository destination (`main`, building-with-ai-f26/vz2228-RubricRadar). Builder requested commit/push and deferred the fresh synthetic workflow, cost per complete review, and full masked-replay check until returning. Updated resume notes and checkpoint wording; archive/guest functionality remains planned only. November 13/15 commits establish dated work once recorded, while remote publication and public analytics require separate verification.

`git diff --check` passed during initial pre-commit inspection and final verification. Earlier session static checks (and the one exact-phrase failure/recovery) remain recorded below; no application or analytics suites or live model evaluations were rerun. New product/OpenRouter inference cost $0. Development usage and session-time estimates retain their explicit earlier cutoffs; ongoing commit/push work is excluded, and active hands-on time remains unmeasured. No model-quality or outside-user evidence added. Publication result must be reported from Git, not inferred from this pre-commit note.

### Development-token estimate and OpenRouter screenshot — November 15, 2026

Version: documentation working tree based on `e7237eb`; app/analytics code unchanged. Builder confirmed Plus and requested an approximate statement of what development could have cost, supplying assumed rates of $2/M input and $10/M output. Read response-level token_usage_record entries once per unique response ID in the two local sessions. November 13: 52 records; November 15 frozen cutoff 11:29:07.957 America/New_York: 36 records. Per-response sums matched final cumulative counters for input, cached input, output, reasoning, and total tokens. Token-count event snapshots were not added again. Combined: 6,938,257 input (including 6,710,400 cached), 32,864 output (including 3,132 reasoning), 6,971,121 total. No dollar-charge fields in the inspected token records. This is a snapshot, not the eventual full current-session usage.

At the supplied rates, applying the full input rate to cached tokens yields $14.205154, approximately $14.21 hypothetical API-equivalent development value. Rates were supplied by the builder, not independently verified model pricing. About 96.7% of input was cached; discounted cache pricing would lower the estimate. Actual Plus subscription allocation/purchased-credit charges remain unreported. The screenshot supplied November 15 displays $0.08 spend over 30 days for one model, DeepSeek V4.1 Flash. It is rounded account-level evidence; project attribution and individual extraction/evaluation costs are not established. Its $0.01 average is not a per-complete-review measurement. Do not add the older $0.029571218 historical subtotal or hypothetical $14.21 to the dashboard's actual-spend figure.

Updated PRD.md, Intent.md, the Build 2 worksheet, and Product Page cost snapshot/log. `git diff --check` passed after edits and after recording this entry. Static documentation checks passed four-document cost/estimate labeling, arithmetic, HTML IDs/fragments, image targets and alt text; zero failures in this batch. No app/analytics suites, fresh model evaluations, browser rendering, replay checks, or outside-user sessions were run. New product/OpenRouter inference cost $0. Development agent usage continues after the frozen cutoff; not included in $14.21. Session-time estimate remains the separately labeled 0.67-hour earlier cutoff; active hands-on time unmeasured. No commit or publication performed.

### Builder reflection and session-time evidence — November 15, 2026

Version: documentation working tree based on `e7237eb`; application/analytics code unchanged. Recorded the builder's three original reflection answers, preserving separate agent clarifications. The third answer does not establish understanding of click-versus-completion; follow-up remains pending. At the builder's request, inspected timestamp/event metadata in local sessions `01a1d54b-ce1c-7ea0-9a8a-30d6ead8ffb1` (November 13) and `01a1dff5-140a-7503-836d-cbc472e6df49` (November 15). No session bodies, secrets, or coursework were copied into evidence.

November 13 first-to-last recorded timestamps span 1,196.138 seconds; November 15 first recorded timestamp to the latest builder turn start at 11:26:29.848 America/New_York spans 1,201.701 seconds. Combined elapsed windows: 2,397.839 seconds = 39.964 minutes = 0.6661 hours, rounded to 0.67 hours. Includes gaps; not verified active builder time. Ongoing work after the cutoff and unlogged work are excluded. The prior eight-minute checkpoint is included, not added. Full calculation and local source session IDs are in journal/build-02-plan.md. Historical evidence entries below retain their original pending-input status.

Checks: `git diff --check` passed after updates and again after this evidence entry. Static standard-library documentation checks passed three original answers/separate clarifications, elapsed arithmetic, cutoff consistency across four documents, unique HTML IDs, internal fragment targets, screenshot paths and alt text. Zero failed checks in this batch. These are documentation/timing checks, not application, model, replay, or usability validation. No application/analytics suites or live model calls run; new inference cost $0. Subscription allocation/PostHog billing remain unreported. Current evidence entry work is after the session-time cutoff and is not included in 0.67 hours. No commit or publication performed.

### Build 2 documentation gap closure — November 15, 2026

Version: documentation working tree based on `e7237eb`, including prior uncommitted PRD v2 and archive-plan edits. Reconciled AGENTS.md and PRD.md with the current session-only implementation and planned explicit-save archive. Narrowed FR6 to the implemented prompt's specific uncheckable-requirement/evidence-failure rule. Filled the optional Build 2 worksheet with the request data flow, agent/builder contributions, known failures/recovery, reported costs, and classmate feedback; summarized status on the Product Page and in Intent.md. Presented three reflection questions to the builder; answers, proposed budgets, actual hours, and podmate/session/sign-off details remain pending. No answers or test outcomes were inferred from reported feedback.

- `git diff --check`: passed after documentation edits and again after the evidence record update.
- Standard-library static documentation check: passed current/planned storage boundary wording, future save approval/guest write restrictions, revised uncertainty wording, exactly three pending builder-answer entries, budget/critique status, unique Product Page HTML IDs, valid internal fragments, and screenshot references/alt text. No failed checks in this batch.
- Limits: source-level checks only; no browser rendering, application or analytics suites, storage implementation, replay inspection, live model evaluation, or new observed user session. Latest recorded application/analytics suites remain November 13: 20 Python tests and three analytics checks passed. New inference cost: $0. Builder/agent time, subscription allocation, and PostHog billing: unreported. No commit or publication performed.

### Archive and guest feature planning — November 15, 2026

Version: documentation working tree based on `e7237eb`, including the earlier uncommitted PRD v2 alignment. Prepared Plan.md and aligned PRD.md, Intent.md, README.md, and the Product Page. Recorded classmate archive feedback as reported by the builder, not an observed user session. No application/storage implementation, application or analytics suites, browser tests, or live model calls were made. New inference cost: $0; builder/agent time and subscription allocation: unreported.

- `git diff --check` passed after the planning edits.
- First static planning check failed on an exact phrase assertion, `no user isolation`, in Plan.md. The plan described the shared-installation access boundary using other wording. Added that explicit phrase for clarity; no runtime bug or implementation change was involved. Other preceding guest/status and HTML checks passed before the assertion failed.
- Recovery rerun: static consistency check passed across five planning/product documents for the guest entry and unimplemented status, required plan topics, HTML IDs/fragment targets, and screenshot file/alt references. Final `git diff --check` passed. These checks validate documentation only; archive behavior, deletion, storage isolation, navigation, and replay masking remain unimplemented and untested.

### PRD v2 documentation alignment — November 15, 2026

Version reviewed: documentation working tree based on `e7237eb`; application and analytics code unchanged. Inspected `app.py`, `radar.py`, and `docs/posthog.js` to align PRD v2 with current components, structured contracts, bounds, routing controls, analytics configuration, and recovery. Updated the Product Page, README, and Intent summary. Historical checkpoints remain labeled; fresh workflow/replay evidence, published-page analytics verification, and two actual Build 2 commit dates remain pending.

- `git diff --check`: passed after documentation edits; no whitespace errors.
- Python standard-library static documentation check: passed PRD v2/date consistency across PRD.md, Intent.md, README.md, and docs/index.html; unique HTML IDs; valid internal fragment targets; existing screenshot files and alt text; removal of the outdated README claim that analytics was absent. This checks source structure, not browser appearance, provider behavior, analytics ingestion, masking correctness, or model quality.
- No application or analytics suites, browser workflow tests, or live AI evaluations were run. The latest recorded suite results remain November 13: 20 Python tests and three analytics checks passed. New inference cost: $0. Total builder/agent time, subscription allocation, and PostHog billing: unreported.

### Build 2 PostHog checks — November 13, 2026

Version tested: working tree based on `95c64a0`, subsequently committed as `698d2ee`; Python 3.14.4, Streamlit 1.66.1, Node.js 24.21.0. Scope: analytics installation only; no new model calls or independent user sessions.

| Method | Outcome | Limits / recovery |
| --- | --- | --- |
| `.venv/bin/python -m unittest discover -s tests -v` | 20 passed, zero failures; 1.613 seconds. | Mocked UI/provider behavior; does not execute browser JavaScript or validate model quality. Expected bare-mode Streamlit warnings appeared. |
| `node --check docs/posthog.js` | Passed, no syntax errors. | Syntax only. |
| `node --test tests/test_analytics.cjs` | Three passed, zero failures; 0.145 seconds. | Mock browser verifies one initialization/pageview/listener across reruns, masking settings, rejection of network capture, and fixed-name clicks without arbitrary DOM text. Does not test PostHog's recorder implementation. |
| Start local previews | Streamlit started on `127.0.0.1:8501`. Product Page initially failed with `PermissionError` when binding port 8765 in sandbox; approved rerun started successfully. | Only `docs/` is served by the static preview, not the repository or `.env`. |
| Browser access | Browser extension host unavailable; native Chrome automation worked. | Browser extension failure did not prevent inspection. An unexpected local-device-access permission prompt from the replay viewer was blocked. |
| Pageview/click ingestion | PostHog Activity displayed four initial events: one Pageview and one `ui_clicked` from each of ports 8765 and 8501. Refresh was needed for all four to appear. | Expanded local click properties showed `action=clear_session`, `surface=local_app`; no assignment text in inspected event properties. Product Page interaction was Read the Living PRD. These are agent-generated checks, not outside users or successful AI reviews. |
| Masked app replay | Opened the recorded session and inspected actual replay: both synthetic instruction/draft values and rendered text appeared as asterisks; app navigation/controls remained visible. | Only initial app/input state tested; complete extraction/feedback replay and a payload-level privacy audit remain pending. After refreshing the replay viewer, the Product Page was also visibly rendered with masked text. Both local surfaces are confirmed in replay; public GitHub Pages update has not been deployed or verified. |

New inference cost: $0. PostHog billing and total builder/agent time: unreported. Historical recorded inference cost remains $0.029571218 (partial). PRD v2, fresh AI workflow evidence, public analytics verification, and two genuine Build 2 commit dates remain pending.

### PRD v1.1 frontend check — November 4, 2026

All 20 deterministic tests pass. UI coverage includes the two-button path, edited requirements reaching evaluation, consent gating, empty-requirement rejection, stale-result invalidation, clearing, and recoverable provider errors. No agent-run live model calls were made; usage/cost and elapsed time for the builder’s latest test were not supplied. The builder tested the local app and confirmed that the simpler flow and card colors worked well. Systematic checks for card contrast in light/dark themes, keyboard navigation, and responsive layout remain outstanding; mocked tests do not verify CSS appearance or model quality. Track A remains recommended and incomplete.

### Detailed v1.1 test record — November 4, 2026

These checks occurred before frontend commit `89aabf8`, except the documentation consistency check below. No assignment text is included.

| Check | Method and outcome | Limits / recovery |
| --- | --- | --- |
| First automated run | `.venv/bin/python -m unittest discover -s tests -v`: 19 passed, 1 failed (`test_combined_action_uses_edits_and_requires_consent`). | Mocked report referenced R2 after the test input removed that requirement, causing a lookup error. Corrected the fixture to retain the other requirement IDs; no production logic change was needed. |
| Second automated run | Same command: all 20 passed. | Mocked providers; establishes UI/contract behavior, not model quality or CSS appearance. |
| First local launch | Streamlit failed to bind 127.0.0.1:8501 with a permission error; builder reported the link failed to open. | Sandbox restriction; restarted after execution approval. |
| Local readiness | Streamlit reported startup; an initial sandboxed health request could not connect. An approved request to `/_stcore/health` returned `ok`. | Local readiness only; no public deployment verified. |
| Builder workflow test | After restart, builder opened the app and reported that it worked well. | Simpler flow accepted by builder; test inputs, timing, API usage/cost, and independent quality ratings were not supplied. |
| Builder color test | Builder separately confirmed the colors worked well. | No screenshot/GIF captured; systematic theme, contrast, keyboard, and responsive checks remain open. |
| Documentation reconciliation | `git diff --check` and a scripted consistency check passed for the current 20-test summaries, builder feedback, historical checkpoint labeling, and pre-commit rule. | Documentation-only update; application tests were not rerun. |

Reported historical API costs remain $0.029571218; latest manual-test cost/time is unreported. No new API calls or application test runs were made for this documentation reconciliation.

### Local server readiness — November 8, 2026

Version: `0bd20d6` (unchanged application). Builder reported a browser connection error. Initial listener/health checks found no reachable server; Streamlit was started with `.venv/bin/python -m streamlit run app.py` and reported startup at `127.0.0.1:8501`. A subsequent sandboxed health request failed to connect; repeating the health request outside sandbox network restrictions returned `ok`. This verifies server readiness only; browser workflow and screenshot capture remain unverified. No automated suite or live model evaluation was run. No model calls were made by this check; API cost: $0; elapsed builder/agent time: unreported.

### Builder screenshot review and delivery audit — November 8, 2026

On November 8, the builder completed a synthetic campus-coffee-shop review on application commit `0bd20d6` and supplied screenshots: 4 requirements, 3 Met, 1 Missing, and one required fix to add the omitted success metric. Screenshots are embedded in the Product Page. API cost and elapsed time were unreported; the recorded cost total remains partial. This single builder check does not establish broad model accuracy or independent usability. GitHub Pages was verified reachable and matched the then-current local page; the screenshot assets and embeds are included in this delivery update. The application remains local. The last recorded automated suite had 20 passes on November 4; it was not rerun today.

Manual inspection of the supplied screenshots confirms the displayed counts and priority. No assignment text or credentials are included in this evidence log; screenshots show only the authorized synthetic example. Repository API checks confirmed public visibility, class-template origin, and GitHub Pages configured from main /docs with status built. An HTTP fetch succeeded and matched the pre-update local HTML. Seven remote commits span November 2–4. A common credential-pattern scan across seven local commits found zero matches, and .env was untracked; this is not an exhaustive security audit. Initial sandbox GitHub checks failed because of network restrictions; approved network checks succeeded. Audit cost/time: unreported; no agent-run model calls.

Documentation verification for this screenshot update: `git diff --check` passed. A local HTML-parser/file check passed: exactly two embedded images, both with alt text, existing relative targets, and valid PNG signatures; all four Markdown summaries contain the November 8 update. Application tests were not rerun. Browser rendering of the updated Product Page has not been checked. Cost/time: unreported.

Build 2 documentation verification (November 13): `git diff --check` passed after implementation/evidence updates and again after the final replay evidence reconciliation. This is a whitespace check; no additional application suite rerun.

### PostHog checkpoint publishing preparation — November 13, 2026

Reviewed the Build 1 status and Build 2 log before this documentation commit. Added checkpoint `698d2ee` and the observed 09:35–09:43 a.m. America/New_York verification/checkpoint window (at least 8 minutes / 0.13 hours). This excludes earlier setup and final publishing; total builder hours, PostHog billing, and subscription allocation remain unreported. No new application or analytics suites or live AI calls were run. `git diff --check` passed for this documentation update; inference cost $0. Public Product Page analytics verification remains pending.
### Local app launch — November 15, 2026

Version: `45c388a`, application unchanged; Python 3.14.4. Started Streamlit on `127.0.0.1:8501`. The initial sandboxed health request failed to connect; the approved request outside sandbox network restrictions returned `ok`. Browser extension access was unavailable; native Chrome control opened the app and confirmed the title, empty instruction/draft fields, unchecked sharing consent, and disabled Extract requirements button. One navigation action was interrupted by a browser-state change; refreshing the observed state and retrying navigation succeeded. This verifies launch and initial UI only. No automated suites or model calls were run; extraction, feedback quality, full workflow replay, and user testing remain pending. New inference cost: $0; elapsed builder/agent time: unreported. Build 1 summary reconciliation is deferred to the next approved documentation batch; no commit was made.

### Builder-reported live review metrics — November 15, 2026

Builder follow-up: when asked whether feedback correctly identified what the draft met and what was missing, the builder replied, “Yes, it worked.” This is a positive builder assessment of this run, not an independent accuracy evaluation. Expected requirements and observed findings were not supplied; full replay remains unchecked.

Method: builder supplied extraction and evaluation metadata in chat after the local launch. Local HEAD was `45c388a`; the supplied metadata does not independently identify the running commit. Both stages reported model `deepseek/deepseek-v4.1-flash` and prompt `v1.2`.

| Stage | Reported seconds | Input tokens | Output tokens | Reported cost (USD) |
| --- | ---: | ---: | ---: | ---: |
| Extraction | 18.70 | 356 | 3,371 | $0.00229428 |
| Evaluation | 19.69 | 1,086 | 3,901 | $0.00278643 |
| Total | 38.39 | 1,442 | 7,272 | $0.00508071 |

Outcome: metadata was reported for both stages. Findings, requirement coverage, correctness, usability, and complete masked replay were not inspected for this run. The time total sums the two reported stages and excludes editing/waiting between actions; total builder time is unreported. Input contents and whether they were synthetic are unreported; no coursework is stored in this evidence entry. No agent-run model calls or automated suites were performed. Adding this run to the previously recorded partial $0.029571218 gives a partial recorded inference total of $0.034651928; this is not a complete spending reconciliation. Product Page/PRD/Intent evidence reconciliation remains pending the next approved documentation batch; no commit was made.


### PostHog screenshot review and session-time refresh — November 15, 2026

Version: documentation working tree based on `45c388a`; app/analytics code unchanged. Builder supplied and approved storing `docs/images/posthog-session-replay-2026-11-15.png` as evidence. Visual review shows two replay entries: today’s entry labeled 11 minutes ago (07:34 displayed duration), an older entry labeled 2 days ago (09:43 displayed duration), and a green one-recently-active-recording indicator. The older entry is selected; its local app replay visibly masks text with asterisks. Today’s replay session is present, as the builder correctly clarified. The image establishes recording ingestion/activity and visible masking at the shown older replay state, not event payloads, today’s complete extraction-to-feedback playback, or public Product Page ingestion. No outside-user or broad accuracy claim is made.

Updated Build 2 elapsed session time: 76.546 minutes (1.28 hours) through November 15, 12:23:48.017 p.m. America/New_York, across three non-overlapping recorded windows. Includes gaps and agent activity; not verified active builder effort. Excludes the break between the two November 15 sessions and work after the cutoff. Supersedes the earlier 0.67-hour snapshot; the historical approximately two-hour Build 1 estimate is separate. Log timestamps for session starts/completed sessions and the system clock for the final active-session cutoff produced windows of 1196.138, 1905.584, and 1491.043 seconds, totaling 4592.765 seconds. Full table and source IDs are in journal/build-02-plan.md. No coursework or credentials copied from session logs. Updated README, Intent, PRD, Plan, Build 1/2 Product Page logs, and Build 2 worksheet. Existing historical checkpoints remain labeled. One initial text patch for the prior builder-confirmation entry failed to match a paragraph; the subsequent targeted heading insertion succeeded without changing app code. This was an edit mismatch, not a failed application test. No new AI calls or app/analytics suite runs for this documentation batch. Incremental inference cost $0; the builder’s prior live review is separately recorded above. Documentation validation results will be recorded below. No commit/push or public deployment performed.

Documentation validation: `git diff --check` passed. Static HTML/image checks passed unique IDs, internal fragments, three existing images with alt text, exact SHA-256 screenshot copy, PNG signature (2734 × 1370), and consistent screenshot/cost/time evidence across six current summaries. Zero failures in this validation batch; application and analytics suites were not rerun. Final time refresh uses the system-clock cutoff reported above; later work is excluded.

### Builder completion confirmation and assignment verification — November 15, 2026

Builder confirmation, November 15: published Product Page analytics and today’s complete replay through feedback/masking are completed. These are builder-reported checks; the agent did not independently replay today’s session or inspect public-page event properties in this step. The still screenshot remains evidence of session activity and the displayed masked replay.

Current Icerynk Build 2 brief verified November 15: working real AI/API action shown on the Product Page; PostHog pageviews/clicks/replay on page and app; PRD v2 covering biggest risk, test, architecture and cost/run; AGENTS.md setup/structure; two outside-class commit dates and updated progress/lessons/problems/costs/hours. Submission is Product Page link, repo link, and a PostHog screenshot showing events; bring the running laptop app to pod testing. Weekly budgets, account-setting confirmation and pod names/sign-off are optional project follow-ups, not stated Build 2 submission requirements. Learn with AI is explicitly ungraded; a documented synthetic reference test is useful quality work, not an additional stated Build 2 requirement.

Source: https://www.icerynk.com/content/build-2-plan-md-smallest-version-live?course=fa26-tech-gb-2160-dm2-f2. Method: native Chrome accessibility inspection of authenticated current assignment; no form submitted or settings changed. Updated current summaries, Build 2 log/checklist and Plan with builder-reported completion and corrected requirement scope. No app/analytics suites or model calls performed; new inference cost $0. Prior screenshot remains unchanged. `git diff --check` passed for the preceding final review and this correction batch. Time retains the explicitly frozen 12:23:48.017 cutoff; subsequent requirement-verification work is excluded pending the next final time refresh.

### Agent-captured PostHog Activity/events screenshot — November 15, 2026

Version: documentation working tree based on `45c388a`. Agent captured PostHog Activity → Events in the sixth Chrome tab on November 15. Last-hour list showed three local-app events at http://127.0.0.1:8501/: one Pageview and two ui_clicked, with recording links on the click rows. This verifies received local-app events; it does not inspect event properties or independently verify public-page traffic. Public-page analytics and complete feedback replay remain builder-confirmed complete. The events screenshot is ready to attach to the Build 2 submission. Saved unedited native Chrome window capture to `docs/images/posthog-events-2026-11-15.jpg`. Visually inspected the captured image: event names, local URL, relative times, and all three rows are legible. No event expansion, model call, app change, or assignment submission performed. Incremental inference cost $0. Updated Product Page and current summaries/checklist; application/analytics suites were not rerun.

Documentation validation/recovery: initial update helper failed with an IndentationError before editing files; the corrected helper ran. The initial four-image check failed because that update had not run; after recovery its PNG-only assertion rejected the native screenshot, which is JPEG encoded. Renamed the unchanged screenshot to .jpg and updated references. These were documentation/helper failures, not app test failures. Final format-aware HTML check and git diff --check passed: four existing images with alt text, valid PNG/JPEG signatures, unique HTML IDs, and valid internal fragments. No application or analytics suites rerun.

### Final evidence commit preparation — November 15, 2026

Reviewed Build 1 evidence status before staging; reconciled its current replay status with the builder’s later confirmation while labeling the earlier pre-commit checkpoint historical. Commit scope: documentation, two PostHog screenshots, live-review metadata/positive builder assessment, corrected assignment checklist, and elapsed session-time snapshot. `git diff --check` passed. Prior HTML/image validation and its failed attempts/recovery are recorded above; no application/analytics suites rerun and no new model calls. Incremental inference cost $0; time retains the explicit cutoff, excluding subsequent commit/push work. Remote publication must be verified after pushing.
