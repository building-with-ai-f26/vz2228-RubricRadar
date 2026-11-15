# Rubric Radar — Class archive and guest mode implementation plan

Prepared November 15, 2026 · Planning only; app implementation has not started.

## Product decision

The builder reported classmate feedback requesting a repository organized by MBA class and professor. The user selected an organized archive with rubric checks inside each assignment, and requested an initial **Continue as guest** button. This is reported discovery feedback, not an observed usability test or evidence of demand across students.

The first version is local to one app installation. There are no accounts or separate user libraries, and no user isolation. Anyone using that installation can access its archive; do not use it as a shared or public service. Guest means no archive storage, not anonymous use: existing masked analytics and provider processing still apply.

## Navigation and journeys

Start screen has two visible buttons: **Continue as guest** and **My classes**. Neither path requires sign-up. Guest must work even if archive storage is unavailable and must not create a database merely by opening or running a check.

Guest path: Continue as guest → paste instructions and draft → consent → Extract requirements → edit → Confirm & review my draft → feedback. No assignment, class, draft, or review is written to archive storage. Clear this session clears working data. Saving guest reviews into a class is deferred for this first version.

Archive path: My classes → create/select a class → create/select an assignment → run the existing check → explicitly Save review → revisit that assignment's review history. Show a consistent Class / Assignment location and a Back to home control. Course name is required; professor and semester are optional to keep setup light. Assignment name is required; due date is deferred.

Creating or editing an assignment uses an explicit **Save assignment** action for its instructions/rubric, with a visible local-storage explanation. Assignment instructions and rubric use the existing combined input field. Inside an assignment, preload its current instructions; edits become assignment defaults only through Save assignment. A review always captures the exact instructions actually checked.

Changing class, assignment, mode, or opening a different review must clear working text, confirmation, results, and provider-sharing consent before loading the destination. If unsaved work exists, present Keep working / Discard and continue before switching. Never carry one assignment's draft or feedback into another.

Opening a saved review is read-only and makes no model calls. **Check a revised draft** copies its instructions and draft into a new working check within the same assignment, clears old findings and confirmation, and requires fresh consent and extraction. New saves append a review; they never overwrite the opened record. No automatic comparison or improvement claim.

## Saved data

Use Python's standard-library SQLite support with a small `archive.py` module. Keep model calls and evidence validation in `radar.py`; app.py coordinates navigation and explicit storage actions. No new runtime package is proposed.

| Entity | Stored fields |
| --- | --- |
| Class | Generated ID, course name, optional professor and semester, creation/update timestamps. |
| Assignment | Generated ID, class ID, name, current combined instructions/rubric, creation/update timestamps. |
| Review | Generated ID, assignment ID, save timestamp, snapshot of instructions and draft, extracted and confirmed requirements with sources/IDs, validated findings and priorities, limitations, available extraction/review operational metadata, model and prompt identifiers. |

Snapshots preserve exactly what was reviewed when assignment defaults later change. Store a schema version and use stable generated IDs rather than titles as keys. Store structured fields as JSON where appropriate, validate saved data on load, and never execute saved content as code. Missing historic metadata is displayed as unavailable, not invented. API keys, raw provider response bodies, and consent flags are never saved.

Proposed location: `data/rubric_radar.sqlite3`, relative to the app installation. Add `data/` and SQLite sidecar files to `.gitignore` before the first database creation. No coursework database goes into commits, docs/, screenshots, analytics, or test evidence. Archive storage is ordinary local disk storage, not encrypted by the app; anyone with access to the installation/files can read it. Update in-app disclosure, README, and AGENTS.md when implementing persistence.

Use parameterized SQL, foreign keys, and transactions. Save review is available only for a successful, current validated result. Mark that result as saved in session state and guard repeated clicks/reruns with a unique save token so one result is not inserted twice. Failed model requests and incomplete work are not automatically archived. A storage failure preserves the working review and shows an error without claiming success or overwriting existing records.

## Deletion and session clearing

Provide Delete review, Delete assignment, and Delete class. Require a confirmation naming the selected item and showing affected review/assignment counts. Deleting an assignment deletes its reviews; deleting a class deletes its assignments and reviews in one transaction. Cancel changes nothing. Invalidate any open deleted record and return to its surviving parent or home.

Clear this session resets transient data; it does not delete saved records. Application deletion removes records from the active archive; it does not promise forensic disk erasure, removal from device backups, or deletion of provider/analytics records. Export, backup UI, trash, and undo are deferred; state that deletion cannot be undone in this first version.

## Acceptance and verification

- Guest can complete the mocked two-button workflow without class creation or any storage writes, including with unavailable archive storage.
- Class/assignment organization persists across process restarts; duplicate names do not mix records because IDs are distinct.
- Saving and reopening returns an identical review snapshot without model calls; updated assignment defaults never rewrite history.
- Revised-draft checks create new reviews; stale results cannot be saved; double clicks and reruns cannot duplicate a save.
- Switching context prompts for unsaved work, resets consent, and does not expose another assignment's state.
- Delete cancellation preserves data; confirmed cascade deletion removes exactly the selected descendants and clears affected session state.
- Simulated storage failures preserve an existing archive and the current review; malformed stored content produces a recoverable message, not raw content in logs.
- Tests use synthetic fixtures in temporary databases. Run Python and analytics checks and log every run and failure under tests/README.md; do not use live model calls for archive tests.
- Manually inspect both paths, reopening after restart, deletion, and navigation. Verify archive titles, drafts, rubrics, and feedback stay masked in replay and absent from analytics properties. Only fixed action names may be added; no class/assignment titles or IDs in events. Record builder checks separately from outside-user results.

## Small implementation batches

1. **Storage foundation:** Add archive.py, synthetic storage tests, and ignore rules; implement schema, snapshot saving/loading, transactions, and deletion. Guest creates no storage. No UI integration yet.
2. **Entry and organization:** Add Continue as guest / My classes, class and assignment forms, location display, context reset, and unsaved-work handling. Preserve existing guest review behavior and provider consent.
3. **Review archive:** Integrate explicit Save review, saved-history viewer, revised-draft flow, duplicate-save prevention, and confirmed deletion. Update storage disclosures and AGENTS.md at the point persistence becomes accessible.
4. **Verification and evidence:** Run relevant suites, inspect synthetic workflows and replay masking, reconcile documentation/evidence, and then assess readiness for classmate testing. Paid model checks remain a separate Build 2 evidence task.

Each batch gets a brief implementation plan and approval before changes across files, as required by AGENTS.md. This document authorizes planning only. Review implementation scope with the builder before coding. Account-based private archives and cloud isolation require a later design before hosting saved coursework publicly.

## Boundaries and Build 2 status

This extension brings optional saved history into planned scope. Automatic revision comparisons, professor-style inference, cross-assignment AI memory, cloud sync, sharing, accounts, PDF uploads, and grade prediction remain deferred. Class/professor metadata organizes records and is not sent to the model as extra grading criteria.

It does not complete the pending Build 2 synthetic workflow/cost measurement, full masked feedback replay, published-page analytics verification. The November 13 analytics commits and November 15 documentation checkpoint record two work dates; verify remote publication separately. Historical recorded inference is $0.029571218, a partial total. No additional storage service is proposed for the local version; runtime/model costs depend on actual new reviews. Budget caps, full builder time, subscription allocation, and PostHog billing remain unreported.
