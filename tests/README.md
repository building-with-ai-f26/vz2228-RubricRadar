# Verification: Tests, Evals & User Feedback

Review agent changes and verify that the product works throughout the course. Use automated tests for application behavior when useful, model evals for output quality, and manual checks for the user experience. A test shows what it checked; record its limits.

## Build 4: choose one track

**Track A — Domain quality**

Define 3–4 rules for good output. Evaluate 10 cases: 5 normal, 3 messy, and 2 adversarial. Compare results before and after improvements, and ask one outside target user to review the result.

**Track B — User friction**

Watch 3–5 outside users try the product without coaching. Review PostHog replays, identify the top three friction points, and document fixes with before/after evidence. The app can still run locally.

Both tracks update PRD v4 and the build log on `docs/index.html`. Follow [Icerynk Build 4](https://www.icerynk.com/c/fa26-tech-gb-2160-dm2-f2/content/build-4-test-py-tests-model-evals) for the rubric. You do not need to complete both tracks.

## Current local prototype checks

Run `.venv/bin/python -m unittest discover -s tests -v` from the repository root. The 12 tests use synthetic inputs and mocked provider responses; they check contracts, quotation integrity, privacy request flags, and UI state/error behavior, not AI judgment quality.

Run `.venv/bin/python tests/smoke_live.py` with a configured local `.env` for a synthetic live review. It makes two billable provider calls and prints metadata/statuses without draft text. This is a feasibility check, not completion of Track A. No classmate coursework is included in the repository.
