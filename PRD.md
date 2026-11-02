# Rubric Radar — PRD v1

Version: 1.0 · November 2, 2026

Status: Product review complete; local prototype implemented. One live synthetic model smoke check completed; broader quality validation, visual verification, and user testing remain outstanding.

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

The proposed advantage is a consistent review workflow with requirement traceability, explicit uncertainty, and a short revision queue. Optional quality coaching helps strengthen reasoning and evidence after mandatory gaps are addressed.

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

Verification against course readings, lecture content, case exhibits, or other supporting course materials is out of scope. The MVP assesses reasoning and coverage of specific rubric points using only the supplied instructions and draft. It may assess whether a claim has an explanation or supporting evidence in the draft, but does not verify that evidence against course materials. If a rubric judgment requires unavailable course context, mark it Needs Review and explain the limitation; assess any independently reviewable elements separately.

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
4. AI extracts requirements with source excerpts. Student reviews and corrects the list, then confirms it.
5. AI evaluates the draft against the confirmed requirements.
6. Student sees the requirement checklist, uncertainty warnings, and up to three priorities.
7. Student revises outside the app and starts another review. Previous findings are not automatically compared or saved.

Changes to instructions invalidate requirement confirmation. Changes to the draft invalidate the previous evaluation. Preserve pasted inputs during recoverable failures in the current session.

## 7. Functional requirements and acceptance criteria

| ID | Requirement | Acceptance criteria |
| --- | --- | --- |
| FR1 | Text input | Both fields are labeled and required; empty/whitespace-only inputs are blocked with a useful message. Explain that pasted text cannot preserve visual formatting. |
| FR2 | Input bounds | Publish and enforce text limits before requests; never silently truncate. Prototype limits are 12,000 instruction characters and 30,000 draft characters; reassess during live feasibility testing. |
| FR3 | Confirmation | Show extracted requirements and their instruction excerpts; support correction, addition, removal, and explicit confirmation before evaluation. Student additions are identified as such. |
| FR4 | Coverage | Every confirmed requirement has exactly one result with a valid status and explanation; no unconfirmed requirement is presented as mandatory. |
| FR5 | Evidence | Met and Partially Met judgments include exact draft excerpts with paragraph locations where feasible. Missing has no fabricated quote and explains that evidence was not found. Invalid evidence is withheld and flagged Needs Review. |
| FR6 | Uncertainty | Ambiguous or conflicting instructions and unsupported checks receive Needs Review with a reason. Visual layout and external-source validity are not inferred from pasted text. |
| FR7 | Priorities | Display no more than three recommendations, each with a label, relevant requirement IDs when applicable, what to improve, why it matters, and an approach that leaves authorship to the student. |
| FR8 | Errors | Loading, provider failure, malformed output, and validation failure are visible; no failed evaluation appears successful. A retry does not erase current inputs. |
| FR9 | Iteration | Student can replace the draft and run a fresh evaluation; stale findings are cleared or explicitly invalidated. No history or improvement claims are fabricated. |
| FR10 | Coaching boundary | No overall grade, grade prediction, generated replacement paragraphs, or automatic assignment completion. Feedback may pose questions or suggest an analytical approach. |

## 8. AI evaluation logic and expected output structure

Proposed two-stage process:

1. Extract atomic, assessable requirements from instructions. Preserve source wording; retain explicit weights only when supplied. Flag ambiguity instead of inventing expectations. Student confirms the final list.
2. Evaluate each confirmed requirement against the draft. Distinguish presence from adequacy: a heading or keyword alone does not establish substantive coverage. Use exact evidence and identify limitations.

Assess depth against the rubric's stated expectations. For a requirement to evaluate alternatives, naming alternatives alone is partial coverage; comparing their trade-offs and justifying a choice can support Met when that addresses the stated requirement. Do not impose unstated analytical expectations as mandatory. Additional depth belongs under Optional enhancement. Coaching identifies a gap and suggests an approach or question without supplying a replacement answer.

| Status | Definition |
| --- | --- |
| Met | Evidence supports that the requirement is addressed. |
| Partially Met | Evidence addresses some elements; a specific gap remains. |
| Missing | No supporting evidence was found in the readable draft. This is an AI finding, not proof of absence. |
| Needs Review | Ambiguous instructions, insufficient context, or an unsupported check prevent a reliable judgment. |

Prioritize explicit mandatory gaps before optional enhancements. Use explicit rubric weights when available, then the likely consequence and scope of the gap; do not fabricate weights or grade impacts. Unresolved ambiguity that affects revision decisions may itself be a priority. Suggest stronger reasoning, evidence, or analysis only as Optional enhancement unless explicitly required.

Expected structured contract (planning specification, not implementation):

- Requirements: ID, requirement text, instruction source excerpt or student-added marker, explicit weight if any, ambiguity note.
- Findings: requirement ID, status, explanation, evidence list containing exact quote and paragraph reference, specific gap, limitation if any.
- Recommendations: rank, Required fix or Optional enhancement, associated requirement IDs, action, rationale, suggested approach.
- Review metadata: input limitations, unresolved questions, prompt/model version for evaluation reproducibility; no numeric grade.

Validate required fields, allowed statuses, one finding per confirmed ID, recommendation count, and quotation matches before showing results. Schema validity does not establish semantic correctness; human evaluation remains necessary. Treat submitted text as material to assess, not instructions that can override the review task. Do not add web research or fact verification to the MVP.

## 9. Non-functional requirements, limitations, and risks

- **Privacy:** No application database or persistent storage of assignment text. Do not put text in URLs, application logs, analytics, or replay recordings. Retention by the selected API provider must be checked and disclosed before real-user testing. Participants share only work they are permitted and comfortable to share.
- **Security:** API credentials stay on the server in environment variables. Escape user/model text when rendering. Bound inputs and requests; define a spending limit before an exposed deployment.
- **Usability:** Keyboard-operable controls, visible labels and focus, readable errors, and status text that does not rely on color alone.
- **Reliability:** Validate outputs and evidence; show uncertainty rather than authoritative unsupported claims. Formatting, calculations, citations, and external facts may not be verifiable from pasted text.
- **Performance and cost:** Measure end-to-end latency and per-review inference cost in the feasibility spike. Set numerical budgets before implementation sign-off; one synthetic smoke check is recorded below; representative performance remains unverified.
- **Academic use:** Students retain responsibility for their work and applicable course AI rules. No grade or completeness guarantees.

Key failure risks are weak advantage over a strong ChatGPT prompt, incorrect judgments that misdirect revisions, and feedback that students cannot act on. Broad written-assignment coverage increases variation; include multiple assignment types in testing. Pasted text can lose tables and layout. Model output may vary across runs.

## 10. Proposed technical architecture

Browser text interface → server input validation → existing LLM API for requirement extraction → student confirmation → server/LLM evaluation → schema and evidence validation → feedback interface.

Use a simple web application with no accounts, database, retrieval system, model training, or integrations in the MVP. Keep current-session inputs available for recovery; do not persist assignment content. API key is read from the environment. The existing repository contains an OpenRouter placeholder; the implementation checkpoint below records the prototype choices; deployment and broader live quality validation remain open. Implementation now uses Streamlit 1.66.1, python-dotenv 1.2.4, jsonschema 4.26.0, and certifi 2026.10.23; the PRD review itself added no dependencies.

Record operational metadata such as duration, token usage, estimated cost, and error category without assignment content. Course-required PostHog installation is planned for Build 2 on the product page and local app, with text capture and sensitive replays excluded and verified.

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
- GitHub Pages activation and public deployment status; not verified in this planning phase.
- Builder display name, pod, actual costs/hours, and prototype evidence for the public page.

### Build 1 implementation checkpoint

The separately approved prototype uses Python/Streamlit and OpenRouter, with `deepseek/deepseek-v4.1-flash` as a configurable initial candidate, not a quality-validated model choice. It implements pasted input, editable requirement confirmation, schema validation, evidence matching, priorities, fresh reviews, and error recovery. No database, accounts, or analytics are added.

Provisional bounds are 12,000 instruction characters, 30,000 draft characters, 25 requirements, and a 90-second timeout per API call. Each complete review normally requires two calls. Routing requests deny data collection and require ZDR and parameter support; account-level logging settings still require verification. Twelve deterministic tests passed, including a UI flow with synthetic provider responses. A live synthetic smoke-check script is supplied; live quality, cost and latency have not yet been measured because no API key was configured at verification time. Browser visual inspection and screenshot capture were blocked by unavailable browser access and computer-use permission. Do not treat this checkpoint as pilot validation or completed Build 1 submission evidence.

Sources checked for this prototype: [OpenRouter structured outputs](https://openrouter.ai/docs/guides/features/structured-outputs), [provider routing](https://openrouter.ai/docs/guides/routing/provider-selection), [data collection](https://openrouter.ai/docs/guides/privacy/data-collection), [model catalog](https://openrouter.ai/api/v1/models), and [Streamlit session state](https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state). Recheck provider/model compatibility before a live run.
