# Intent.md — Optional PRD Draft (Build 1)

Use this as a scratchpad if helpful. Publish the required PRD and Build 1 log on `docs/index.html`; this file is not a separate hand-in.

**Build 1 due:** Monday, Nov 9, 2026 at noon, New York time  
**Builder:** victor-zu-97 · Pod 12

**Updated:** November 8, 2026 · aligned with PRD v1.1

**Product:** Rubric Radar — Know what's missing. Understand what matters. Submit stronger work.

---

## 1. Who is it for?
*Name a specific person or role you have direct access to (not a broad demographic). Who will actually test and use this before Demo Day?*

- **Target user:** MBA classmates preparing written reports or project submissions who already have a draft and explicit assignment instructions or a rubric.
- **How I will reach them to test it:** Recruit 2–3 MBA classmates I can reach directly. Ask them to try the workflow without coaching, using work they are permitted and comfortable to share, and identify whether the feedback leads to a useful revision. Classmate sessions have not occurred; testing so far has been by the builder.

## 2. What job does it do?
*Describe the concrete recurring problem from work, school, or life, and what "done" looks like for the user.*

- **Current painful workflow (before):** Students manually compare a draft with assignment instructions or ask a general-purpose AI assistant for feedback, then decide which suggestions matter. The working hypothesis is that requirements get overlooked and feedback can be difficult to verify or prioritize; outside-user testing has not yet validated this problem.
- **New workflow with this product (after):** Paste the instructions and draft, review and correct extracted requirements, click Confirm & review my draft, then inspect a finding for each requirement with supporting draft evidence and up to three revision priorities. Revise in an external editor and paste the updated draft for a fresh review. Done means the student can identify a specific gap and decide what to revise while retaining authorship.
- **Why this is useful** *(used weekly / saves real time / worth paying for)*: The intended value is a repeatable pre-submission check that makes omissions easier to find and revision decisions easier to explain. Requirement-linked evidence and a short priority list are the proposed advantages. Time savings, repeat usage, willingness to pay, and an advantage over a strong ChatGPT prompt have not been demonstrated.

## 3. What is in and out of scope?

- **One core workflow:** Pasted instructions + written draft → editable requirement extraction → combined confirmation and review → evidence-backed requirement review → up to three prioritized improvements → external revision and fresh review.
*You have six weeks. List the features, integrations, and polish you are deliberately NOT building.*

- [ ] Not building: Assignment generation, automatic rewriting, official grade predictions, or completeness guarantees.
- [ ] Not building: PDF uploads, slides, spreadsheets, LMS integrations, or collaboration features in the initial MVP.
- [ ] Not building: Saved review history, automatic version comparisons, or verification against course materials, external facts, or source documents. The prototype uses current-session memory with no database.

## 4. Rough Local Prototype
*What did you spike this week to test the core idea, and what did you learn from throwing it at the problem?*

- **Local run command / branch / screenshot:** From the repository folder, run `.venv/bin/python -m streamlit run app.py` and open `http://127.0.0.1:8501`. Follow [README.md](./README.md#local-setup) for environment setup; the OpenRouter key stays in the local `.env`. The prototype uses Python/Streamlit, OpenRouter, JSON Schema validation, and a configurable initial model, `deepseek/deepseek-v4.1-flash`. Builder screenshots are embedded in the Product Page; GitHub Pages publishing was verified November 8. The app remains local.
- **What we created:** A local text-only app with permission-to-share consent, input bounds, editable requirement confirmation, source excerpts, and a result for every confirmed requirement: Met, Partially Met, Missing, or Needs Review. Feedback includes a summary, compact requirement cards, expandable evidence, and up to three revision priorities. Backend checks validate response structure and draft quotations; unverified evidence becomes Needs Review and linked recommendations are withheld. Changed inputs invalidate stale results, and users can clear the session. Requests require privacy-compatible provider routing; account-level logging settings still need verification before real coursework.
- **What worked:** The latest recorded verification reports 20 passing deterministic tests covering contracts, evidence checks, input bounds, provider failures, privacy request settings, and mocked UI flows. The original synthetic live check returned three requirements and one recommendation in 10.84 seconds of combined API time, at a reported cost of $0.003135. Two further builder reviews completed in 77.30 and 55.22 seconds, at reported costs of $0.01418914 and $0.012247078. The builder confirmed that the summary, cards, and expandable details worked, and confirmed a subsequent run after prompt v1.2. On November 4, the builder tested PRD v1.1 and confirmed that the simpler flow and status colors worked well. This is builder feedback, not independent user validation. These checks do not establish broad model accuracy.
- **What surprised us and changed:** Exact instruction-source matching rejected whitespace differences, so matching now tolerates whitespace while retaining original excerpts. Reviews exhausted the initial 7,000-token output budget; the review default is now configurable and set to 16,000, with safe diagnostics for incomplete responses. Live feedback imposed conventions such as email greetings that were not explicitly required. Prompt v1.2 focuses on explicit requirement coverage and removes generic ambiguity notes; depth is assessed only when requested. Backend changes also required restarting the server during testing. On November 4, an inconsistent mocked test fixture caused one failure; correcting the fixture produced 20 passing tests. The first local server launch was blocked by sandbox permissions; after approval, the server started and its health endpoint returned ok, and the builder opened the app successfully.
- **Evidence and limits:** Recorded API costs total $0.029571218 across the three runs with supplied usage; failed requests, the final confirmation run, and other unrecorded usage are excluded. The builder reported approximately two hours for the recorded session. Independent user testing, representative model-quality evaluation, full cost reconciliation, and public application deployment remain outstanding. See [PRD.md](./PRD.md) for the full product definition and [the Product Page](./docs/index.html) for the required Build 1 log.

### November 8 evidence update

On November 8, the builder completed a synthetic campus-coffee-shop review on application commit `0bd20d6` and supplied screenshots: 4 requirements, 3 Met, 1 Missing, and one required fix to add the omitted success metric. Screenshots are embedded in the Product Page. API cost and elapsed time were unreported; the recorded cost total remains partial. This single builder check does not establish broad model accuracy or independent usability. GitHub Pages was verified reachable and matched the then-current local page; the screenshot assets and embeds are included in this delivery update. The application remains local. The last recorded automated suite had 20 passes on November 4; it was not rerun today.
