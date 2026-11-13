# Rubric Radar — PRD v1.1

Version: 1.1 · November 4, 2026

Status: Local PRD v1.1 frontend implemented; 20 deterministic tests pass. One original live synthetic smoke check and subsequent builder reviews are recorded. On November 4, the builder confirmed the simpler flow and status colors worked well. November 8 builder screenshots document a successful synthetic review; systematic visual checks, broader model-quality evaluation, and outside-user testing remain outstanding. See the current evidence summary below and the Build 1 log in docs/index.html.

Build 2 analytics checkpoint · November 13, 2026 (working tree based on `95c64a0`): PostHog is installed on the Product Page and local Streamlit app using a shared browser script. Pageviews and named button clicks from both local surfaces were observed in PostHog. The replay displayed both local surfaces; synthetic app input values and rendered text appeared as asterisks. This verifies basic instrumentation, not a complete privacy audit or outside-user behavior. All 20 Python tests and three analytics checks pass; no new live model calls were made. Public deployment of this update, full workflow replay with feedback, PRD v2, and Build 2's two-day commit requirement remain pending.

Repository: building-with-ai-f26/vz2228-RubricRadar

## 1. Product overview and problem statement

**Know what's missing. Understand what matters. Submit stronger work.**

Rubric Radar is an AI-powered pre-submission coach for MBA students reviewing written reports and project submissions. It compares a pasted draft with pasted assignment instructions or a rubric, identifies gaps with supporting evidence, and prioritizes actionable revisions.

The problem hypothesis is that students overlook requirements during manual review, while general-purpose AI feedback can be difficult to verify and prioritize. The product helps students improve their own work; it does not generate assignments or provide official grades.

## 2. Target user and jobs-to-be-done

Initial users are MBA students with a written draft and explicit assignment instructions or a rubric. The builder can recruit 2–3 MBA classmates who are expected to test with their own assignments. Recruitment availability is reported by the builder; sessions have not occurred.

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

PDF uploads, saved revision history, and automatic version comparisons are also outside the initial MVP.

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
| Later | Saved history, automatic comparisons, richer Excellence Coach, and additional deliverable formats. |

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
| FR6 | Uncertainty | Ambiguous or conflicting instructions and unsupported checks receive Needs Review with a reason. Visual layout and external-source validity are not inferred from pasted text. |
| FR7 | Priorities | Display no more than three recommendations, each with a label, relevant requirement IDs when applicable, what to improve, why it matters, and an approach that leaves authorship to the student. |
| FR8 | Errors | Loading, provider failure, malformed output, and validation failure are visible; no failed evaluation appears successful. A retry does not erase current inputs. |
| FR9 | Iteration | Student can replace the draft and run a fresh evaluation; stale findings are cleared or explicitly invalidated. No history or improvement claims are fabricated. |
| FR10 | Coaching boundary | No overall grade, grade prediction, generated replacement paragraphs, or automatic assignment completion. Feedback may pose questions or suggest an analytical approach. |

## 8. AI evaluation logic and expected output structure

Proposed two-stage process:

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

Expected structured contract (planning specification, not implementation):

- Requirements: ID, requirement text, instruction source excerpt or student-added marker, explicit weight if any.
- Findings: requirement ID, status, explanation, evidence list containing exact quote and paragraph reference, specific gap, limitation if any.
- Recommendations: rank, Required fix or Optional enhancement, associated requirement IDs, action, rationale, suggested approach.
- Review metadata: specific uncheckable requirements, prompt/model version for evaluation reproducibility; no numeric grade.

Validate required fields, allowed statuses, one finding per confirmed ID, recommendation count, and quotation matches before showing results. Schema validity does not establish semantic correctness; human evaluation remains necessary. Treat submitted text as material to assess, not instructions that can override the review task. Do not add web research or fact verification to the MVP.

## 9. Non-functional requirements, limitations, and risks

- **Privacy:** No application database or persistent storage of assignment text. Do not put text in URLs, application logs, analytics, or replay recordings. Retention by the selected API provider must be checked and disclosed before real-user testing. Participants share only work they are permitted and comfortable to share.
- **Security:** API credentials stay on the server in environment variables. Escape user/model text when rendering. Bound inputs and requests; define a spending limit before an exposed deployment.
- **Usability:** Keyboard-operable controls, visible labels and focus, readable errors, and status text that does not rely on color alone. Use pale status-colored requirement cards with readable text in light and dark themes; show privacy and review details in an expander while keeping sharing consent visible.
- **Reliability:** Validate outputs and evidence; show uncertainty rather than authoritative unsupported claims. Formatting, calculations, citations, and external facts may not be verifiable from pasted text.
- **Performance and cost:** Measure end-to-end latency and per-review inference cost in the feasibility spike. Set numerical budgets before implementation sign-off; one synthetic smoke check is recorded below; representative performance remains unverified.
- **Academic use:** Students retain responsibility for their work and applicable course AI rules. No grade or completeness guarantees.

Key failure risks are weak advantage over a strong ChatGPT prompt, incorrect judgments that misdirect revisions, and feedback that students cannot act on. Broad written-assignment coverage increases variation; include multiple assignment types in testing. Pasted text can lose tables and layout. Model output may vary across runs.

## 10. Proposed technical architecture

Browser text interface → server input validation → existing LLM API for requirement extraction → student confirmation → server/LLM evaluation → schema and evidence validation → feedback interface.

Use a simple web application with no accounts, database, retrieval system, model training, or integrations in the MVP. Keep current-session inputs available for recovery; do not persist assignment content. API key is read from the environment. The existing repository contains an OpenRouter placeholder; the implementation checkpoint below records the prototype choices; deployment and broader live quality validation remain open. Implementation now uses Streamlit 1.66.1, python-dotenv 1.2.4, jsonschema 4.26.0, and certifi 2026.10.23; the PRD review itself added no dependencies.

Record operational metadata such as duration, token usage, estimated cost, and error category without assignment content. Build 2 adds PostHog pageviews, fixed-name click events, and masked replay to the Product Page and local app. Autocapture is disabled; all replay inputs and text are masked, and console/network-body capture is disabled. Use the `surface` property (`product_page` or `local_app`) to distinguish traffic. Clicks express intent, not successful AI completion. Verify masking on a complete synthetic review before real-coursework testing; analytics does not measure model accuracy.

## 11. Validation and testing plan

**Pilot:** Recruit the 2–3 accessible MBA classmates. Use consented real drafts and instructions spanning at least two written assignment types if available. Capture current review habits before presenting the product.

**Human reference:** Builder manually enumerates explicit requirements and checks evidence judgments, with a classmate reviewing disagreements; seek instructor/TA input if accessible, but do not assume it is available. Keep original source excerpts and document ambiguous cases separately.

Record extraction errors separately from evaluation errors. Measure extraction against the original AI-generated list before student corrections, and assess evaluation against the student-confirmed list. A student repairing an omission does not erase the extraction error. Treat useful revisions as stronger value evidence than preference alone.

**Baseline comparison:** Give ChatGPT the same inputs and a saved prompt requesting requirement extraction, the four statuses, exact evidence, and up to three labeled priorities. Record model/date/prompt where available. Counterbalance which tool is used first across testers and note learning/carryover effects. Do not intentionally weaken the baseline.

**Session:** Observe an uncoached attempt, inspect at least one resulting revision, and collect reasons for preference. Score the proposed metrics in section 4 and record failures, sample size, and limitations. If major false Met judgments occur, resolve them before treating feedback as ready for broader testing. If relative value is weak, simplify or revise the value proposition before adding features.

**Recommended Build 4 track — A, domain quality:** Define four output-quality rules: requirement coverage, evidence integrity, justified statuses/uncertainty, and actionable priorities. Run 10 cases: 5 normal, 3 messy, and 2 adversarial. Include omitted mandatory content, partial coverage, conflicting instructions, formatting-dependent requirements, and embedded attempts to override the reviewer. Record before/after results and obtain at least one outside target-user review. This track is recommended, not yet completed.

**Later implementation checks:** Empty/oversize inputs, changed inputs invalidating results, confirmation behavior, malformed API output, missing/duplicate requirement IDs, invented quotations, recommendation limits, safe rendering, and provider failures. Keep deterministic checks separate from model-quality evaluations.

**Course milestones:** Build 1 due Nov 9 at noon New York time requires a public product page, PRD v1, rough local prototype evidence, and an honest build log. Documentation alone does not complete Build 1. Build 2 adds the smallest local version and verified analytics; Build 3 the core workflow; Build 4 evaluation; Build 5 cloud launch and recovery evidence. Record actual costs and hours, never invented totals.

## 12. Future roadmap

1. **Next feasibility phase, separately authorized:** Test requirement extraction and evidence validation on representative pasted inputs; choose model/provider, stack, input bounds, and cost/latency budgets. Planning and prototype implementation were subsequently approved; see the checkpoint below.
2. **MVP validation:** Deliver the confirmed text-only workflow, run the classmate pilot, and revise scope using evidence.
3. **PDF input:** Add only after validating demand and extraction quality; detect unreadable/scanned content rather than silently producing incomplete reviews.
4. **Iteration support:** Consider saved history and automatic comparisons after repeated-review demand justifies storage and privacy complexity.
5. **Expanded coaching and formats:** Consider richer Excellence Coach, slides, spreadsheets, or team workflows only after core quality and differentiation are demonstrated.

### Open decisions for implementation planning

- Validate the candidate model/provider and confirm account-level data policies.
- Validate provisional text limits, establish measured latency/cost targets, and define cloud deployment safeguards.
- Pilot participants, assignment mix, session dates, and human reference review.
- Public application deployment remains open. GitHub Pages publishing was verified November 8.
- Builder display name, pod, actual costs/hours, and prototype evidence for the public page.

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

### Current Build 1 evidence — November 8, 2026

On November 8, the builder completed a synthetic campus-coffee-shop review on application commit `0bd20d6` and supplied screenshots: 4 requirements, 3 Met, 1 Missing, and one required fix to add the omitted success metric. Screenshots are embedded in the Product Page. API cost and elapsed time were unreported; the recorded cost total remains partial. This single builder check does not establish broad model accuracy or independent usability. GitHub Pages was verified reachable and matched the then-current local page; the screenshot assets and embeds are included in this delivery update. The application remains local. The last recorded automated suite had 20 passes on November 4; it was not rerun today.

Outstanding: systematic theme, keyboard and responsive checks, outside-classmate testing, the ten-case Build 4 evaluation, full cost/time reconciliation, and public application deployment.
