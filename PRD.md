# Rubric Radar — PRD v4

**Build 4 Track A — November 24.** The same ten synthetic cases scored 36/40 on v1.2 and 38/40 on v1.3 against fixed expectations. Prompt v1.3 tells the reviewer to credit partial explicitly required content, cite what is present, and surface at least one actionable required fix for a demonstrated mandatory gap. The rerun still omitted a priority in one case and returned stray review labels during extraction in another. The checks exercised both app stages against OpenRouter. Outside target-user feedback and hosted verification of the revised workflow remain pending. [Scorecard and examples](docs/index.html#build-4) · [Test evidence](tests/README.md#november-24--build-4-track-a)

**Current checkpoint — November 22.** Rubric Radar is live on Streamlit Community Cloud. Public desktop startup, one synthetic guest review and the builder’s Google sign-in passed. Hosted archive save and reopen, classmate phone use, live replay masking and remaining audit checks are open. [Live app](https://rubricradar.streamlit.app/) · [Resume plan](Plan.md) · [Test evidence](tests/README.md#november-22--public-deployment-and-one-live-guest-review)

**November 24 local follow-up.** A tester reported an output token limit error. The affected stage is unknown. The local extraction budget rose to 10,000 output tokens, and the draft review default and maximum rose to 50,000. All 63 deterministic Python tests passed. Live provider verification and deployment remain pending. [Test evidence](tests/README.md#november-24--draft-review-output-budget)

**Historical checkpoint — November 19.** Hosted Supabase SQL-role, anonymous access, two-account isolation, token expiry and the synthetic app archive workflow passed. The normal archive stays disabled. Batch 4 local controls limit provider requests and concurrency and render untrusted feedback as plain text. The latest local checks passed 63 Python and seven Node tests. Hosted runtime, privacy, phone and live replay checks remain pending. Earlier checkpoints below are historical. [Resume plan](Plan.md) · [Test evidence](tests/README.md#november-19--batch-4-local-release-audit-and-controls)


**Save-and-push checkpoint — November 17:** Builder requested saving all current work to Git. Plan.md contains the consolidated resume point: builder Supabase account/project creation, then real database/Auth security verification before enabling cloud saves. No application/analytics suites rerun for commit preparation; latest recorded results remain 61 Python / four analytics passes. Pre-commit review and limited scan are recorded in tests/README.md. Public Streamlit deployment and schema execution are pending; verify actual Git publication separately.

**Impeccable refinement — November 17:** Installed Impeccable 4.9.2 and applied its polish guidance to the existing local UI: consistent typography/spacing, clearer cards and fields, shared feedback styles and a compact mobile header/summary. Structure, controls and class identity colors remain. Final 61 mocked Python tests passed (5.543 seconds); Chrome desktop, 400px and 768px previews inspected. Native form autocomplete warnings remain; real-phone/dark-theme/full accessibility/live replay checks are pending. No model/cloud calls or deployment. Context helper initially failed executable permission; fallback guidance was applied directly, permission repaired, no context/detector/hooks pass claimed. See DESIGN.md and tests/README.md.


**Class colors — November 17:** Added subtle, stable class color accents, carried into project cards and review context labels. The read-only sample now includes Strategy, Marketing and Finance. No additional navigation controls or database fields. Existing 61 Python tests passed (5.629 seconds); local Chrome verified three colored cards and a matching Marketing project. No analytics-suite rerun, model/cloud calls or deployment. Phone/dark-theme/replay checks and real Supabase security remain pending. Builder accepted the preceding minimal design; acceptance of these colors is not yet recorded.


**Design checkpoint — November 17:** Builder requested a minimal aesthetic and fewer navigation buttons. Local Home/My classes now use a neutral light default, one blue accent, shorter typography/copy, quiet secondary actions, a compact top bar in place of the sidebar and class/project cards. Privacy details remain accessible in a bottom expander; model-sharing consent remains visible in the editor. Existing 61 Python tests passed (5.711 seconds); native Chrome Home/My classes screenshots were visually checked. No new model calls or analytics-suite rerun, phone/dark-mode/keyboard check, cloud changes or deployment. Supabase setup and the full security/live replay work remain pending. Details in tests/README.md. Earlier UI descriptions below reflect historical checkpoints.


**Historical Build 3 checkpoint — November 17, batch 3:** Local UI now has Home, Continue as guest, gated sign-in/recovery, a read-only synthetic sample library, private class/project/history controls, explicit saves and confirmed deletion. The guest editor includes Load demo example (fills both fields, clears stale feedback/save state and resets consent without sending/saving text). Current gate RUBRIC_RADAR_ARCHIVE_ENABLED defaults false. No Supabase account/project is configured, no migration executed, and real sign-in/cloud saves remain unavailable. Builder will create the account/project using docs/setup/supabase-account.md. No app deployment, commit/push or submission. Earlier checkpoints below are historical where they differ.

**November 17 verification:** 61 mocked Python tests and four analytics tests passed. Native Chrome verified local Home → sample class → project → saved review and the demo button filling both fields with consent unchecked. A stale imported-module error during the demo update was recovered by restarting Streamlit and refreshing. No paid model calls; live database/API/email isolation, full audit, phone and live PostHog/replay checks remain pending. See tests/README.md for every run and recovery.

**PostHog events screenshot captured — November 15:** Agent captured PostHog Activity → Events in the sixth Chrome tab on November 15. Last-hour list showed three local-app events at http://127.0.0.1:8501/: one Pageview and two ui_clicked, with recording links on the click rows. This verifies received local-app events; it does not inspect event properties or independently verify public-page traffic. Public-page analytics and complete feedback replay remain builder-confirmed complete. The events screenshot is ready to attach to the Build 2 submission. [Events screenshot](docs/images/posthog-events-2026-11-15.jpg).

**Build 2 completion clarification — November 15:** Builder confirmation, November 15: published Product Page analytics and today’s complete replay through feedback/masking are completed. These are builder-reported checks; the agent did not independently replay today’s session or inspect public-page event properties in this step. The still screenshot remains evidence of session activity and the displayed masked replay.

Current Icerynk Build 2 brief verified November 15: working real AI/API action shown on the Product Page; PostHog pageviews/clicks/replay on page and app; PRD v2 covering biggest risk, test, architecture and cost/run; AGENTS.md setup/structure; two outside-class commit dates and updated progress/lessons/problems/costs/hours. Submission is Product Page link, repo link, and a PostHog screenshot showing events; bring the running laptop app to pod testing. Weekly budgets, account-setting confirmation and pod names/sign-off are optional project follow-ups, not stated Build 2 submission requirements. Learn with AI is explicitly ungraded; a documented synthetic reference test is useful quality work, not an additional stated Build 2 requirement. [Assignment brief](https://www.icerynk.com/content/build-2-plan-md-smallest-version-live?course=fa26-tech-gb-2160-dm2-f2). Submission evidence now includes an agent-captured events screenshot and the builder-supplied replay screenshot. Earlier pending checklists below describe previous checkpoints and are superseded by this clarification.

**Latest Build 2 evidence — November 15, 2026:** November 15 builder review completed: extraction 18.70 seconds / $0.00229428; evaluation 19.69 seconds / $0.00278643; total 38.39 seconds / $0.00508071, model deepseek/deepseek-v4.1-flash, prompt v1.2. Builder confirmed the feedback worked. This is one builder assessment, not independent accuracy validation; reference expectations and findings were not supplied. The supplied PostHog screenshot shows today’s replay entry (11 minutes ago), an older entry (2 days ago), and one recently active recording. The selected older replay visibly masks app text. Today’s recording is present; complete playback through today’s feedback and event properties are not established by this still image. Published-page analytics and full feedback replay are now builder-confirmed complete; see confirmation below.

Updated Build 2 elapsed session time: 76.546 minutes (1.28 hours) through November 15, 12:23:48.017 p.m. America/New_York, across three non-overlapping recorded windows. Includes gaps and agent activity; not verified active builder effort. Excludes the break between the two November 15 sessions and work after the cutoff. Supersedes the earlier 0.67-hour snapshot; the historical approximately two-hour Build 1 estimate is separate. See [screenshot](docs/images/posthog-session-replay-2026-11-15.png) and [detailed evidence](tests/README.md). No application or analytics suites rerun for this update.

Version: 3 · November 17, 2026

Historical batch 2 status (superseded by current batch 3 checkpoint above): Implemented app remains a local, session-only text MVP with the two-button review flow and masked PostHog instrumentation. Build 3 Beginner lane is selected. Batches 1–2 are approved: Streamlit Community Cloud, Supabase Auth/Postgres, and private Class → Project → Saved reviews with a guest path are the selected design. Auth/storage backend modules and SQL scripts now exist locally, with no new dependencies; they are not connected to app.py. No migration, cloud provisioning, sign-in/library UI or deployment has occurred. See section 13 and [Plan.md](./Plan.md) for scope and resume instructions.

November 17 evidence: agent-observed synthetic workflow on local HEAD `1d34206` produced 19 requirements, 11 Met / 3 Partially Met / 5 Missing / 0 Needs Review; the three priorities addressed intended omissions. This was one workflow, not a scored accuracy evaluation or outside-user test; activation of the review button was not observed. Full evidence/replay/metadata/cost/time were not inspected. Batch 2 verification: 44 Python tests passed initially; after a password-reset outcome correction and two regression tests, 46 passed. Three analytics checks passed; pip check found no broken requirements. SQL and real Auth/API tests remain unrun. These mocked checks do not establish deployed security or model quality. November 15 live-review metrics and builder-confirmed public-page analytics/full masked feedback replay remain recorded above. Build 3 deployment and cross-account security proof remain pending. See tests/README.md. Earlier dated checkpoints below are historical and superseded by this current status where they differ.

Repository: building-with-ai-f26/vz2228-RubricRadar

## 1. Product overview and problem statement

**Know what's missing. Understand what matters. Submit stronger work.**

Rubric Radar is an AI-powered pre-submission coach for MBA students reviewing written reports and project submissions. It compares a pasted draft with pasted assignment instructions or a rubric, identifies gaps with supporting evidence, and prioritizes actionable revisions.

The problem hypothesis is that students overlook requirements during manual review, while general-purpose AI feedback can be difficult to verify and prioritize. The product helps students improve their own work; it does not generate assignments or provide official grades.

## 2. Target user and jobs-to-be-done

Initial users are MBA students with a written draft and explicit assignment instructions or a rubric. The builder can recruit 2–3 MBA classmates who are expected to test with their own assignments. Recruitment availability is reported by the builder. On November 15 the builder reported classmate feedback requesting a class/professor archive; no structured observation sessions or usability outcomes have been recorded.

**Job:** Before I submit my draft, help me identify overlooked requirements and prioritize improvements so I can submit stronger work.

**Before, hypothesized:** Manually compare instructions with a draft, or ask a general-purpose assistant for feedback, then decide which suggestions matter.

**After:** Paste both texts, confirm extracted requirements, inspect evidence-backed findings, and act on up to three priorities. Revise externally and repeat as needed.

## 3. Value proposition and differentiation

The proposed advantage is a consistent review workflow with requirement traceability, explicit uncertainty, and a short revision queue. The review focuses on explicit requirement coverage; it does not impose extra depth or professional conventions.

These are differentiation hypotheses, not proven advantages. Compare against ChatGPT using a well-designed, consistent prompt that requests the same statuses, evidence, and priorities. Success must reflect useful revisions and clearer decisions rather than interface preference alone.

## 4. Goals, non-goals, and success metrics

Goals: surface important omissions, make judgments inspectable, and help students prioritize meaningful revisions.

Proposed pilot targets, not measured results:

| Measure | Target and method |
| --- | --- |
| Requirement extraction | At least 90% recall before student corrections across the human-reviewed pilot sample. Recall = correctly captured explicit requirements / human-identified explicit requirements; also record invented and duplicate requirements. |
| Evidence integrity | Every displayed quotation matches draft text; no major unsupported Met judgment found in human review. A major error falsely clears a substantive mandatory requirement. Record counts and denominators. |
| Actionability | At least 2 testers independently identify and make one useful revision, supported by before/after excerpts and the tester's explanation. |
| Relative value | At least 2 testers prefer Rubric Radar over the prompt baseline for a specific reason tied to traceability, prioritization, or a useful revision. Record contrary feedback. |
| Usability | At least 2 testers complete paste → confirmation → feedback without coaching; record completion time and blockers. |

The small sample is directional and cannot establish broad reliability or improved grades.

Explicit non-goals:

1. Writing or automatically rewriting assignments.
2. Predicting official grades or guaranteeing completeness.
3. Supporting slides, spreadsheets, LMS integrations, or collaboration features.

PDF uploads and automatic version comparisons remain outside scope. Saved revision history was excluded from the initial MVP; it is now planned as a private cloud class/project archive (section 13), not yet implemented.

Verification against course readings, lecture content, case exhibits, or other supporting course materials is out of scope. The MVP checks whether explicit rubric requirements are addressed using only the supplied instructions and draft. Depth, rigor, structure, and formatting are assessed only when explicitly requested. It may assess whether a claim has an explanation or supporting evidence in the draft, but does not verify that evidence against course materials. If a rubric judgment requires unavailable course context, mark it Needs Review and explain the limitation; assess any independently reviewable elements separately.

## 5. MVP scope and feature prioritization

| Priority | Capability |
| --- | --- |
| MVP | Paste instructions/rubric and a written draft into separate fields. |
| MVP | Extract requirements and let students correct, add, or remove items before confirming. |
| MVP | Evaluate every confirmed requirement with a status, explanation, and available evidence. |
| MVP | Provide zero to three prioritized recommendations, labeled Required fix or Optional enhancement. |
| MVP | Allow a fresh review after external revision; no saved comparison required. |
| Later | PDF input, after text extraction accuracy and user need are tested. |
| Planned extension | Private Class → Project → Saved reviews via Supabase Auth/Postgres, plus Continue as guest; not implemented. |
| Later | Automatic comparisons, richer Excellence Coach, and additional deliverable formats. |

Excellence Coach is initially optional quality guidance within the same report, not a separate product mode. Do not invent recommendations to fill three slots.

## 6. Primary user journey

1. Student sees what the tool does, its limitations, and how text is processed.
2. Student pastes assignment instructions/rubric and draft into labeled text fields.
3. App checks required inputs and supported length before sending them for analysis.
4. Student clicks **Extract requirements**. AI extracts requirements with source excerpts available in an expander. Student reviews and corrects the list.
5. Student clicks **Confirm & review my draft**, which confirms the edited list and immediately evaluates the draft. There is no separate confirmation button or ready-to-review screen.
6. Student sees a compact summary, up to three priorities, and requirement cards colored by status: green for Met, amber for Partially Met, red for Missing, and blue for Needs Review. Each card retains a written status; evidence and source details remain expandable.
7. Student revises outside the app and starts another review. Previous findings are not automatically compared or saved.

Changes to instructions invalidate requirement confirmation. Changes to the draft invalidate the previous evaluation. Preserve pasted inputs during recoverable failures in the current session.

## 7. Functional requirements and acceptance criteria

| ID | Requirement | Acceptance criteria |
| --- | --- | --- |
| FR1 | Text input | Both fields are labeled and required; empty/whitespace-only inputs are blocked with a useful message. Explain that pasted text cannot preserve visual formatting. |
| FR2 | Input bounds | Publish and enforce text limits before requests; never silently truncate. Prototype limits are 12,000 instruction characters and 30,000 draft characters; reassess during live feasibility testing. |
| FR3 | Confirmation | Show extracted requirements and their instruction excerpts; support correction, addition, removal, and explicit confirmation through a single Confirm & review my draft action that starts evaluation. After consent, reaching feedback requires two primary button clicks: Extract requirements, then Confirm & review my draft. Student additions are identified as such. |
| FR4 | Coverage | Every confirmed requirement has exactly one result with a valid status and explanation; no unconfirmed requirement is presented as mandatory. |
| FR5 | Evidence | Met and Partially Met judgments include exact draft excerpts with paragraph locations where feasible. Missing has no fabricated quote and explains that evidence was not found. Invalid evidence is withheld and flagged Needs Review. |
| FR6 | Uncertainty | Use Needs Review when a specific explicit requirement cannot be checked from the supplied text or its evidence fails verification, with a specific reason. General ambiguity alone does not trigger this status. Visual layout and external-source validity are not inferred from pasted text. |
| FR7 | Priorities | Display no more than three recommendations, each with a label, relevant requirement IDs when applicable, what to improve, why it matters, and an approach that leaves authorship to the student. |
| FR8 | Errors | Loading, provider failure, malformed output, and validation failure are visible; no failed evaluation appears successful. A retry does not erase current inputs. |
| FR9 | Iteration | Student can replace the draft and run a fresh evaluation; stale findings are cleared or explicitly invalidated. No history or improvement claims are fabricated. |
| FR10 | Coaching boundary | No overall grade, grade prediction, generated replacement paragraphs, or automatic assignment completion. Feedback may pose questions or suggest an analytical approach. |

## 8. AI evaluation logic and expected output structure

Implemented two-stage process:

1. Extract atomic, assessable requirements from instructions. Preserve source wording; retain explicit weights only when supplied. Extract only explicit requirements; do not infer additional conventions or deliverables. Student confirms the final list.
2. Evaluate each confirmed requirement against the draft. Check whether each explicit requirement is addressed. A heading alone is not an answer, but a relevant brief response can meet a requirement. Use exact evidence.

Assess depth only when explicitly requested by the rubric. Do not downgrade a response for lacking inferred conventions (for example, an email greeting or sign-off) or additional analysis. Required fixes must identify a demonstrated missing explicit element, rather than conditional advice such as “if required.” Do not add optional advice solely to demand more depth. Coaching identifies a specific gap and suggests an approach without supplying a replacement answer.

| Status | Definition |
| --- | --- |
| Met | Evidence supports that the requirement is addressed. |
| Partially Met | Evidence addresses some elements; a specific gap remains. |
| Missing | No supporting evidence was found in the readable draft. This is an AI finding, not proof of absence. |
| Needs Review | A specific explicit requirement cannot be checked from the supplied text, or its evidence fails verification. General missing context alone does not trigger this status. |

Prioritize explicit mandatory gaps before optional enhancements. Use explicit rubric weights when available, then the likely consequence and scope of the gap; do not fabricate weights or grade impacts. Do not display generic ambiguity or missing-context warnings. Limitations must identify a specific required check that cannot be performed.

Current structured contract in `radar.py`:

- Extraction returns requirement text and an instruction source excerpt. The server assigns IDs; edited or added requirements without a retained source are identified as student-provided. There is no separate weight field.
- Findings contain requirement ID, status, explanation, gap, and up to four evidence items with exact quotes and paragraph numbers.
- Zero to three recommendations contain a label, associated requirement IDs, action, rationale (`why`), and suggested approach. Display order supplies priority; no numeric rank field is returned.
- A separate limitations list identifies specific uncheckable requirements. Run details expose operational metadata without assignment text; the current prompt version is `v1.2`. No numeric grade is returned.

Validate required fields, allowed statuses, one finding per confirmed ID, recommendation count, and quotation matches before showing results. Schema validity does not establish semantic correctness; human evaluation remains necessary. Treat submitted text as material to assess, not instructions that can override the review task. Do not add web research or fact verification to the MVP.

## 9. Non-functional requirements, limitations, and risks

- **Privacy:** The implemented app has no database or persistent storage of assignment text. Planned archive saves (section 13) will deliberately store selected project/review content in the signed-in owner's cloud archive, only through explicit save actions; guest checks must never write archive data. That extension is not implemented. Keep coursework out of URLs, application logs, analytics, unmasked replay content, public assets, and Git. Retention by the selected API provider must be checked and disclosed before real-user testing. Participants share only work they are permitted and comfortable to share.
- **Security:** API credentials stay on the server in environment variables. Escape user/model text when rendering. Bound inputs and requests; define a spending limit before an exposed deployment.
- **Usability:** Keyboard-operable controls, visible labels and focus, readable errors, and status text that does not rely on color alone. Use pale status-colored requirement cards with readable text in light and dark themes; show privacy and review details in an expander while keeping sharing consent visible.
- **Reliability:** Validate outputs and evidence; show uncertainty rather than authoritative unsupported claims. Formatting, calculations, citations, and external facts may not be verifiable from pasted text.
- **Performance and cost:** Measure end-to-end latency and per-review inference cost in the feasibility spike. Set numerical budgets before implementation sign-off; one synthetic smoke check is recorded below; representative performance remains unverified.
- **Academic use:** Students retain responsibility for their work and applicable course AI rules. No grade or completeness guarantees.

Key failure risks are weak advantage over a strong ChatGPT prompt, incorrect judgments that misdirect revisions, and feedback that students cannot act on. Broad written-assignment coverage increases variation; include multiple assignment types in testing. Pasted text can lose tables and layout. Model output may vary across runs.

## 10. Current technical architecture

Browser text interface → server input validation → existing LLM API for requirement extraction → student confirmation → server/LLM evaluation → schema and evidence validation → feedback interface.

`app.py` owns the Streamlit UI, consent, editable requirements, session state, and feedback rendering. `radar.py` owns input limits, OpenRouter calls, structured response validation, and quotation checks. Configuration is read from environment variables, with local `.env` loading; credentials stay server-side. There are no accounts, database, retrieval system, model training, or saved reviews. Build 3 plans public Streamlit Community Cloud deployment; the Product Page is served separately by GitHub Pages. No public app deployment has been verified.

A normal complete review makes two server-side model calls: extraction, then evaluation after student confirmation. The configurable default model is `deepseek/deepseek-v4.1-flash`, a candidate whose broad quality remains unvalidated. Each request has a 90-second timeout. Local extraction allows 10,000 output tokens. The local review default is 50,000, configurable from 1 to 50,000. Requests require `data_collection: deny`, `zdr: true`, and parameter-compatible routing. Requests fail if compatible routing is unavailable. Account logging and provider policies still need verification before real coursework.

The recorded environment uses Python 3.14.4, Streamlit 1.66.1, python-dotenv 1.2.4, jsonschema 4.26.0, and certifi 2026.10.23. The batch 2 cloud foundation uses standard-library HTTP plus existing dependencies and adds no packages. `docs/posthog.js` is loaded by the Product Page and embedded into the Streamlit document, with a browser guard to prevent duplicate initialization across reruns.

Record operational metadata such as duration, token usage, estimated cost, and error category without assignment content. Build 2 adds PostHog pageviews, fixed-name click events, and masked replay to the Product Page and local app. Autocapture is disabled; all replay inputs and text are masked, and console/network-body capture is disabled. Use the `surface` property (`product_page` or `local_app`) to distinguish traffic. Clicks express intent, not successful AI completion. Verify masking on a complete synthetic review before real-coursework testing; analytics does not measure model accuracy.

### Build 2 analytics acceptance criteria

| Criterion | Evidence / remaining check |
| --- | --- |
| Both surfaces send pageviews and fixed-name `ui_clicked` events, distinguished by `surface`. | Observed on local Product Page and local app November 13. Published-page ingestion remains unverified. |
| Click properties contain only fixed control names and surface identifiers, without coursework. | Named controls are mapped in the shared script; inspected local event properties contained no assignment text. This is not a payload-level privacy audit. |
| Replay masks all inputs and text; console and network-body capture stay off. | Configuration and mocked analytics checks cover these controls; initial synthetic app inputs and rendered text appeared masked in replay. Full extraction-to-feedback replay remains pending. |
| Reruns do not duplicate initialization, pageviews, or listeners. | Covered by the November 13 mocked browser checks; these do not validate the PostHog recorder implementation. |
| Analytics claims distinguish clicks from successful reviews and builder sessions from outside users. | No completion event is implemented. Do not infer a successful AI review, conversion rate, or independent adoption from button clicks. |

### Build 2 documentation completion status — November 15

Architecture/data flow, scope boundaries, recorded costs, and recovery are documented. AGENTS.md now distinguishes implemented session-only behavior from the planned explicit-save archive. The builder supplied three architecture reflection answers; original answers and separate agent clarifications are recorded in journal/build-02-plan.md. The third answer conflates clicking, completion, and saving; follow-up on that distinction remains pending. Reported archive feedback is recorded; podmate names, session date/method, and sign-off remain unreported. Proposed weekly API and engineering-time budgets await builder input. At the builder’s request, the earlier frozen session timestamps supported about 40 minutes (0.67 hours) of elapsed Build 2 session time across November 13 and November 15 through 11:26:29.848 a.m. New York time on November 15; this includes gaps and is not verified active hands-on time. See journal/build-02-plan.md for the current delivery worksheet. This documentation work does not complete the outstanding workflow, replay, or published-page analytics evidence. The builder requested committing and pushing this November 15 checkpoint before pausing for a later test session.

### Build 2 risk, cost, and recovery plan

The central risk is that schema-valid feedback still misses an explicit requirement or falsely marks it Met. The smallest local version exposes extracted requirements for correction and shows verified quotes so the student can inspect each judgment. Those safeguards do not establish semantic accuracy. The next synthetic workflow should include a deliberately missing explicit requirement, compare results against a human reference, record API duration/cost, and inspect feedback masking in replay. Broader quality testing remains part of Build 4.

| Item | Recorded basis and open decision |
| --- | --- |
| Inference per full review | Three historical recorded runs cost $0.003135, $0.01418914, and $0.012247078. These are observations, not a forecast or spending cap. November 15 builder measurement: $0.00508071 and 38.39 seconds for extraction plus evaluation. |
| Runtime | The same runs reported 10.84, 77.30, and 55.22 seconds combined API time; these exclude user editing and are not end-to-end completion times. |
| Product runtime spending | Builder-supplied OpenRouter screenshot November 15 shows $0.08 spend over the last 30 days for DeepSeek V4.1 Flash, rounded/account-level. Project attribution remains unreconciled; one November 15 full review is separately measured at $0.00508071. Earlier $0.029571218 is a historical partial subtotal, not an additional charge. |
| Development, analytics, and hosting | Builder confirms Plus. Approximate API-equivalent development estimate: $14.21 for the two session snapshots at supplied $2/M input and $10/M output rates, charging cached input at the full rate. This is not actual spending; a cache discount would lower it. Project subscription allocation and PostHog billing remain unreported. No public app hosting has been deployed. |
| Builder time and budgets | Historical builder session: approximately two hours; November 13 has a separate observed window of at least eight minutes. Earlier frozen session windows totaled 39.964 minutes (0.67 hours) through the November 15 11:26:29.848 a.m. New York cutoff, including gaps; the eight-minute November 13 checkpoint is already included. Active hands-on hours, engineering time budget, and total spending cap remain unreported. |

Session token breakdown, exact cutoffs, formula, and screenshot limitations are in journal/build-02-plan.md. The dashboard’s $0.01 average is not a measured cost per complete review. Keep hypothetical development value separate from actual subscription and product spending.

Recoverable request errors preserve session inputs and expose safe diagnostics. Clear this session resets app state; it does not delete external analytics records. Git commits provide local code recovery; review changes before restoring files. Verify provider spending limits or alerts before exposing the application publicly, and define cloud rollback in Build 5. Do not silently relax routing privacy controls to recover from a provider failure.

## 11. Validation and testing plan

**Pilot:** Recruit the 2–3 accessible MBA classmates. Use consented real drafts and instructions spanning at least two written assignment types if available. Capture current review habits before presenting the product.

**Human reference:** Builder manually enumerates explicit requirements and checks evidence judgments, with a classmate reviewing disagreements; seek instructor/TA input if accessible, but do not assume it is available. Keep original source excerpts and document ambiguous cases separately.

Record extraction errors separately from evaluation errors. Measure extraction against the original AI-generated list before student corrections, and assess evaluation against the student-confirmed list. A student repairing an omission does not erase the extraction error. Treat useful revisions as stronger value evidence than preference alone.

**Baseline comparison:** Give ChatGPT the same inputs and a saved prompt requesting requirement extraction, the four statuses, exact evidence, and up to three labeled priorities. Record model/date/prompt where available. Counterbalance which tool is used first across testers and note learning/carryover effects. Do not intentionally weaken the baseline.

**Session:** Observe an uncoached attempt, inspect at least one resulting revision, and collect reasons for preference. Score the proposed metrics in section 4 and record failures, sample size, and limitations. If major false Met judgments occur, resolve them before treating feedback as ready for broader testing. If relative value is weak, simplify or revise the value proposition before adding features.

**Build 4 Track A — output quality.** The four rules are complete requirement coverage, relevant exact evidence, correct statuses with honest limitations, and specific revision priorities. The ten-case synthetic set covers five normal, three messy and two adversarial inputs. Preserve the original extraction output in the test so missed or invented requirements affect the score. Credit the parts of a requirement that appear in the draft, and direct the student to the highest-priority demonstrated gap. Treat model-generated status labels in extraction and skipped priorities as remaining defects. Obtain at least one outside target-user review before calling the evaluation complete. [Scorecard and examples](docs/index.html#build-4)

**Deterministic verification scope:** Empty/oversize inputs, changed inputs invalidating results, confirmation behavior, malformed API output, missing/duplicate requirement IDs, invented quotations, recommendation limits, safe rendering, and provider failures. Keep deterministic checks separate from model-quality evaluations.

**Course milestones:** Build 1 due Nov 9 at noon New York time requires a public product page, PRD v1, rough local prototype evidence, and an honest build log. Documentation alone does not complete Build 1. Build 2 adds the smallest local version and verified analytics; Build 3 the core workflow; Build 4 evaluation; Build 5 cloud launch and recovery evidence. Record actual costs and hours, never invented totals.

## 12. Future roadmap

1. **Complete Build 2 evidence:** A fresh builder review and cost/time are recorded; still record reference expectations/findings for a synthetic quality check, inspect complete masked replay, verify published-page analytics, and verify remote publication of the November 13/15 checkpoints. Confirm provider policies and builder budgets before real-coursework or exposed deployment.
2. **MVP validation:** Deliver the confirmed text-only workflow, run the classmate pilot, and revise scope using evidence.
3. **PDF input:** Add only after validating demand and extraction quality; detect unreadable/scanned content rather than silently producing incomplete reviews.
4. **Private cloud archive and guest entry (Build 3 planned):** Follow the approved planning decisions and pending implementation batches in Plan.md. Accounts and database ownership protection precede UI saves; preserve Continue as guest. Automatic comparisons remain deferred.
5. **Expanded coaching and formats:** Consider richer Excellence Coach, slides, spreadsheets, or team workflows only after core quality and differentiation are demonstrated.

## 13. Build 3 — Beginner lane: gated private cloud archive UI

The builder selected the Beginner lane and approved the local foundation and UI. Supabase hosted schema installation succeeded November 18. Google sign-in and sign-out, rollback-only SQL assertions, anonymous access and authenticated two-account API isolation passed on November 19. Normal app archive access remains disabled. [Setup](docs/setup/supabase.md) · [Evidence](tests/README.md#november-19--two-account-direct-api-isolation)

**Hosting and accounts (target):** Streamlit Community Cloud will host the Python app; GitHub Pages remains the Product Page. Google Identity Services supplies the sign-in popup and Supabase verifies the nonce-bound identity token and owns archive sessions. Email/password/signup/recovery forms were replaced; no SMTP sender is needed. Verify browser popup behavior, hosting compatibility and live Google/Supabase session handling. Keep secrets server-side and authenticated clients isolated per session. Do not store passwords ourselves or globally cache user tokens.

**Journey (UI implemented locally; normal archive disabled pending release):** Continue as guest → existing consent/extraction/confirmation/review, without coursework archive writes; or sign in → My classes → select/create project → run review → explicitly save → reopen history. Classes are private folders, not shared sections. Project means assignment; no additional assignment level. Class name required; professor/semester optional. Guest still involves masked analytics/provider processing.

**Database.** Supabase Postgres stores owner IDs on classes, projects and review snapshots. Hosted SQL and direct API checks verified RLS and same-owner parent constraints against synthetic fixtures. Routine access uses the publishable key and authenticated user's token. Anonymous requests to the archive endpoints were refused.

**Saves and state (UI implemented; cloud gate defaults off):** Save project deliberately stores instructions/rubric defaults. Save review appends the exact instructions/draft, extracted/confirmed requirements, validated feedback and available model/prompt/run metadata. Opening saved reviews makes no model calls; revised-draft checks start fresh consent/confirmation and create new snapshots. Enforce duplicate-save prevention and schema validation on load. Failures preserve working results. Context changes reset coursework/results/consent after an unsaved-work prompt; logout/account changes clear private state immediately. Class metadata adds no grading rules or AI memory.

**Deletion and privacy.** The UI confirms review/project/class deletion with affected counts. Hosted SQL verified cascades and direct API checks verified the owner's own review deletion and test-fixture cleanup. The hosted synthetic app workflow verified cancel, confirmed deletion and class cascade cleanup. Clear this session leaves saved records intact. Disclose cloud saves, retention and backup limits before real coursework. Account deletion and retention procedures remain release decisions. Keep secrets, tokens and coursework out of logs, URLs, Git, analytics and evidence. Mask auth fields, names, saved history and feedback in replay and keep console/network-body capture off.

**Security acceptance.** The hosted two-account test verified own-account access, zero rows for cross-account operations, blocked forged-owner and cross-owner parent writes, and unchanged A records. Anonymous access was refused. The hosted expiry check received HTTP 403 from Auth and HTTP 401 from the archive after token expiry. [Security audit record](SECURITY.md#required-two-account-test--november-19) · [Refused-write screenshot](tests/evidence/supabase-two-account-isolation-2026-11-19.png)

**Release acceptance:** Saved snapshots survive restart/sign-in and reopen unchanged without calls; guest does not archive coursework; context switches cannot expose another account/project; deletion affects only owned selected descendants; repeated saves do not duplicate records. Verify a live phone review plus live PostHog payloads and complete masked replay. Local controls allow 30 provider requests per rolling hour and two in flight per process. The builder confirmed an OpenRouter key limit. Verify the actual host key and reset policy, hosting quotas, provider account logging and database retention before enabling hosted inference. The required assignment security proof uses two accounts; the no-database 30-call alternative is not this design's proof.

**Authentication.** The official Google button uses popup mode with automatic sign-in off. A per-session nonce expires after five minutes and is consumed on each exchange attempt. Google receives its SHA-256 hash and Supabase verifies the token against the original nonce. The server verifies the resulting user in Supabase. The app requires fresh sign-in after session loss and clears local state on logout. Supabase access JWTs can remain valid until expiry. Both test accounts completed the local browser flow. Hosted app session, phone and replay checks remain pending.

**Sample and demo:** Home offers a read-only, clearly labeled synthetic Class → Project → Saved review walkthrough without an account, cloud writes or model calls. Mutating/model controls are disabled there. Guest/project editors offer Load demo example to explicitly replace working instructions/draft, reset consent and clear old results/save tokens. This never saves or sends text automatically. The existing consent/extract/confirm-review flow remains necessary for a billable live check. No new model-quality claims are made by fixed synthetic feedback.

**Delivery:** Submit live URL, note with repo + Beginner lane + SECURITY.md link, and refused-security-test screenshot. Bring phone November 24 for live pod testing per the user-supplied brief. Advanced-lane previews, automatic test-gated deploys and separate dev/production databases are not required. Development uses mocks/test infrastructure; deployed checks use synthetic records. Shared spaces, collaboration, uploads, automatic comparisons and cross-project AI memory remain deferred.

**Next steps.** Finish the Batch 4 audit by confirming provider account privacy, retention and recovery. Obtain separate approval for a remote push and public deployment. The public app URL, phone/pod checks, and live replay remain pending. [Resume plan](Plan.md)

### Historical Build 1 implementation checkpoint — initial prototype

This records the initial verification only; the current evidence summaries below supersede its current-status statements.

The separately approved prototype uses Python/Streamlit and OpenRouter, with `deepseek/deepseek-v4.1-flash` as a configurable initial candidate, not a quality-validated model choice. It implements pasted input, editable requirement confirmation, schema validation, evidence matching, priorities, fresh reviews, and error recovery. No database, accounts, or analytics are added.

Provisional bounds are 12,000 instruction characters, 30,000 draft characters, 25 requirements, and a 90-second timeout per API call. Each complete review normally requires two calls. Routing requests deny data collection and require ZDR and parameter support; account-level logging settings still require verification. Twelve deterministic tests passed, including a UI flow with synthetic provider responses. A live synthetic smoke-check script is supplied; live quality, cost and latency have not yet been measured because no API key was configured at verification time. Browser visual inspection and screenshot capture were blocked by unavailable browser access and computer-use permission. Do not treat this checkpoint as pilot validation or completed Build 1 submission evidence.

Sources checked for this prototype: [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs), [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [data collection](https://openrouter.ai/docs/guides/privacy/data-collection), [model catalog](https://openrouter.ai/api/v1/models), and [Streamlit session state](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state). Recheck provider/model compatibility before a live run.

### PRD v1.1 — Simpler frontend (November 4, 2026)

Approved change: reduce the three-button extraction → confirmation → evaluation flow to two buttons by combining confirmation and evaluation. Preserve editable requirements, explicit consent, source inspection, input invalidation, evidence validation, and recoverable errors. Move supporting privacy/limitation details into an expander; retain the visible consent checkbox and short grade disclaimer.

Use green / amber / red / blue requirement cards for Met / Partially Met / Missing / Needs Review respectively, with written status labels and expandable evidence. No provider, prompt, storage, or evaluation-contract changes are included. This is a frontend revision within Build 1, not completion of the course's Build 2 milestone. Mocked UI tests verify behavior; visual checks and outside-user evidence are recorded separately and do not establish model accuracy or measured usability improvement.

### Historical Build 1 evidence — November 4, 2026

PRD v1.1 frontend code was committed as `89aabf8`. The recorded automated verification before that commit initially had 19 passes and one failure in `test_combined_action_uses_edits_and_requires_consent`: the mocked report still referenced requirements removed by the test input. Correcting the fixture to preserve the requirement IDs produced 20 passes. This was a test-data correction, not a provider or production-logic fix.

The local server initially failed to bind port 8501 because of sandbox permissions. After execution approval, Streamlit started and its health endpoint returned `ok`. The builder then opened the app and reported that both the simpler flow and card colors worked well. This supports the local frontend behavior; it does not establish model accuracy, independent usability, or measured time savings. No agent-run billable live evaluations were performed for v1.1; usage/cost and elapsed time for the builder's latest test were not supplied.

Earlier recorded API costs remain $0.029571218 across three runs with supplied usage; this is not a full spending total. Screenshot/GIF evidence, systematic light/dark-theme, keyboard and responsive checks, outside-classmate testing, the ten-case Build 4 evaluation, full cost reconciliation, and public deployment verification remain outstanding. Detailed test outcomes are recorded in `tests/README.md`; the public Build 1 summary is in `docs/index.html`.

### Historical Build 1 evidence — November 8, 2026

On November 8, the builder completed a synthetic campus-coffee-shop review on application commit `0bd20d6` and supplied screenshots: 4 requirements, 3 Met, 1 Missing, and one required fix to add the omitted success metric. Screenshots are embedded in the Product Page. API cost and elapsed time were unreported; the recorded cost total remains partial. This single builder check does not establish broad model accuracy or independent usability. GitHub Pages was verified reachable and matched the then-current local page; the screenshot assets and embeds are included in this delivery update. The application remains local. The last recorded automated suite had 20 passes on November 4; it was not rerun today.

Outstanding: systematic theme, keyboard and responsive checks, outside-classmate testing, the ten-case Build 4 evaluation, full cost/time reconciliation, and public application deployment.
