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
