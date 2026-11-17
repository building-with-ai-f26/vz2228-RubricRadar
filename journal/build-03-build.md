# Build 3: Build.exe (The Core, in Small Changes)

Optional working notes. Publish your required build log on `docs/index.html`; no separate journal submission is required.

**Build due:** Monday, Nov 23, 2026 at 12:00 PM (Noon)

---

## 1. What you made
- **PRs / Commits shipped:** 
- **Product Page URL / local demo evidence:** 
- **Summary of what works now:** 

## 2. Metacognition ("Learn with AI"): Branches, Diffs & Agent Guardrails
- **Changes your AI tutor helped you understand: what changed, why it matters, and how you checked it:**
  1. 
  2. 
  3. 
- **New rule you added to `AGENTS.md` after catching your agent making a mistake this week:** 

## 3. What the agent did
- **Agent(s) & Model(s) used:** 
- **How you briefed/directed it (key prompts or `AGENTS.md` updates):** 
- **Where you had to step in, edit by hand, or reset context:** 

## 4. What didn't work
- **Bugs, agent loops, or broken assumptions:** 
- **How you diagnosed and fixed (or rolled back) them:** 

## 5. What it cost
- **Agent / Token spend this week:** `$___`
- **Hosting / API runtime spend this week:** `$___`
- **Your hours spent this week:** `___ hrs`
- **Cumulative project spend to date:** `$___`

## 6. Pod Critique Sign-off
- **Tested by podmate(s):** 
- **Key feedback to address next:**

## November 17 — Batch 1 planning checkpoint

Beginner lane selected. Builder approved saving the plan and advancing batch 1 only. Canonical resume point: [Plan.md](../Plan.md). PRD v3 selects Streamlit Community Cloud + Supabase Auth/Postgres, private Class → Project → Saved reviews, explicit saves and a guest path. Local SQLite proposal is superseded. Added Shipping / Ask me first and the documented screenshot-format mistake rule to AGENTS.md. SECURITY.md is a pending audit register; no security checks/fixes are claimed by creating it.

App remains local/session-only; no auth/archive/guest-entry implementation, service provisioning, database migration, deployment, commit/push or submission. Next: brief batch 2 auth/schema/RLS plan and approval. Required final evidence includes two-account direct API isolation/refused-write screenshot, live phone workflow and live masked PostHog replay. Bring phone November 24 per user-supplied brief; existing November 23 noon deadline above has not been reverified.

No app/analytics suites or agent model calls run for this documentation batch; $0 incremental inference, active time and development spend unreported. Existing November 17 synthetic workflow evidence is preserved and reconciled in PRD/Intent/Product Page, without claiming independent accuracy. Documentation validation is recorded in tests/README.md. Historical November 15 PNG-only screenshot validation failure supplies the real-mistake rule; no new failure is implied.

## November 17 — Batch 2 foundation checkpoint

Builder explicitly approved batch 2. Added standard-library Supabase transport, per-session email/password/code/recovery auth and private archive methods. No dependencies added; app.py unchanged. Added transactional migration (RLS, minimal grants, same-owner composite FKs, unique save tokens, immutable reviews, invoker count RPC), rollback-only SQL security tests, ignored secret/archive artifacts and docs/setup/supabase.md. No migration applied or service provisioned. SQL tooling is absent; SQL and real Auth/API security remain unverified.

Initial 44 Python tests passed. Review found password-update success could be hidden by a subsequent logout failure; corrected outcome handling and added two regression tests. Final 46 tests passed. Three analytics checks and pip check passed. No failing suite runs; Streamlit bare-mode and disabled pip-cache warnings did not fail checks. No browser/model tests, live security evidence, commit/push, deployment or submission. New inference cost $0; development cost/time unreported. Plan.md is updated to resume with disposable database checks and batch 3 UI planning/approval. SECURITY.md documents partial checks and remaining audit work.

## November 17 — Batch 3 UI, sample and demo button

Builder approved batch 3 and then explicitly accepted a read-only sample, requested account creation instructions and requested a button that fills example instructions/draft. Implemented Home/guest, gated email auth/recovery, classes/projects/history, explicit saves, revised-draft flow, context/account clearing, unsaved-work keep/discard, pagination and delete confirmation/reconfirmation. Shared feedback rendering keeps opened snapshots free of model calls. Read-only SampleArchive offers a synthetic walkthrough. Load demo example fills both editor fields, clears old result/save state and unchecks consent; no automatic model request or archive save.

Cloud gate defaults false. No Supabase project configured, migration applied, real save, deployment, commit/push or assignment submission. Builder will create account/project using docs/setup/supabase-account.md. Next: real schema/API/email verification, then batch 4 audit/hosting approval.

Staged Python runs: 46/46, 57/57, 60/60 and finally 61/61 passed. Four analytics checks passed twice (before/after demo mapping); no failing automated runs. Local Chrome confirmed sample class/project/saved feedback plus demo inputs (291/525 characters, consent off). Running server initially retained the pre-demo imported module and displayed ImportError; restart/reload recovered. Browser access host was unavailable, so native Chrome was used. No model calls ($0 incremental inference); active hours/development costs unreported. Full evidence in tests/README.md. Real Supabase isolation, phone usability, live replay/privacy and broad model quality remain unverified.


### November 17 — Minimal design pass

Builder approved a design pass before Supabase setup, then requested an Apple-inspired minimal direction with fewer navigation buttons. Added static app_style.css and a neutral light default theme with a single blue accent; replaced the large repeated masthead/sidebar with a compact top bar, shortened Home copy, made secondary actions quiet links, moved privacy details into a bottom expander (consent remains visible), and arranged class/project cards in two columns that wrap on narrow screens. Coursework remains in native widgets; only trusted static presentation uses HTML/CSS. No auth/storage/model rules changed, no new dependencies, and cloud gate remains false.

Verification: `.venv/bin/python -m unittest discover -s tests -v` passed all 61 tests in 5.711 seconds, no failures; Streamlit bare-mode warnings were non-fatal. No new tests authored for this reversible visual change. Analytics code was unchanged and its suite was not rerun. Restarted the local server to load the theme/import changes; native Chrome refresh showed the new Home and sample My classes layouts without error. Inspected screenshots: readable light default, clear primary/secondary actions, no sidebar, class card with one Open class action. Screenshot observations are visual QA, not an exported screenshot artifact or usability result. Phone sizing, keyboard flow, dark-theme override and live PostHog/replay were not inspected. No model calls ($0 incremental inference), cloud changes, commit/push or deployment; cost/active builder time unreported.

Builder's earlier “nice, it works” confirms their demo-button experience; method, inputs and operational cost/time were not supplied. This is builder feedback on that earlier feature, not acceptance of the new design or independent model accuracy. Supabase account/project creation, real database/API/email checks, full audit, phone/replay proof and public deployment remain outstanding.


### November 17 — Class color accents

Builder accepted the minimal design (“Its nice”) and requested colors to distinguish classes. Added a stable six-color presentation palette derived from class UUIDs, subtle card tints/top borders, and matching project/working-review/saved-review context accents. Class names remain visible; color is supplemental. Palette choices can repeat and are not a unique identifier. No new buttons, schema fields, dependencies or storage behavior. Expanded the read-only synthetic sample to Strategy, Marketing and Finance, each with a project/review, so multiple colors can be previewed. No real coursework or cloud writes.

Verification: `.venv/bin/python -m unittest discover -s tests -v` passed 61 tests in 5.629 seconds, zero failures. Existing tests only; no new tests authored for reversible styling. Analytics code unchanged; analytics tests were not rerun. Restarted Streamlit to load imported sample/UI changes, refreshed local Chrome and visually checked three class cards with sand/blue/mint accents. Opened Marketing and confirmed its blue context label/project card matched. Native screenshots inspected; no repository screenshot saved. This is light-theme desktop visual QA, not phone/dark-theme/keyboard/replay or independent usability verification. No new model calls ($0 inference), provisioning, database changes, commit/push or deployment. Active time/development cost unreported; Supabase setup, real isolation/email tests, full audit and live deployment remain pending.


### November 17 — Impeccable-guided aesthetic refinement

Builder explicitly requested opening impeccable.style, installing its skills and improving aesthetics while keeping the existing structure. Inspected the official site/repository and used the Codex skill-installer helper to install the unified Impeccable 4.9.2 skill/playbooks at ~/.codex/skills/impeccable. First install attempt failed certificate verification; retry with the existing trusted certifi CA bundle succeeded, without disabling TLS checks. The installed context launcher initially failed with permission denied (exit 126); read the skill's required fallback/context references and current PRD/implementation directly. PRODUCT.md/DESIGN.md did not exist then. Repaired the launcher's executable bit; did not rerun context, download/run its engine or enable hooks. Skill instructions are available automatically next turn and were read/applied manually now. No automatic detector or full design-audit result is claimed.

Applied polish/craft-floor/Operate guidance: shared typography/spacing/radius/color tokens, balanced Home wrapping without the redundant eyebrow, native wordmark, clearer class/project title roles, hue-related metadata, quieter context borders, consistent fields/focus/selection/reduced-motion handling, consolidated feedback styles and a two-by-two narrow-screen metric summary. Preserved page structure, button labels/count, class UUID colors, guest/demo/recovery/review/save/delete behavior and privacy gates. Added DESIGN.md to record the incumbent system and limits. No new dependencies/assets/model prompts/database fields or runtime packages.

Automated runs (same `.venv/bin/python -m unittest discover -s tests -v` command): initial polish 61 passed / 0 failed in 5.930 seconds; final native-header/layout revision 61 passed / 0 failed in 5.543 seconds. No new tests authored for this reversible visual pass. Streamlit bare-mode warnings were non-fatal. Analytics code and provider/storage logic unchanged; analytics suites and pip check were not rerun. Source contrast calculation passed 12 declared text/background pairs, minimum 5.33:1; this does not establish contrast of every rendered state. git diff --check passed. Final CSS cleanup only removed an unused token and excluded the title wrapper from card padding; no suite repeat for that styling-only cleanup.

Manual QA: local Streamlit restarted for imported UI changes; Chrome desktop checked Home, class/project cards, sample editor and saved feedback. DevTools responsive preview checked 400px Home/library/editor/summary and 768px feedback. Initial narrow layout exposed excessive metric stacking and a header overlap: a CSS-only column adjustment was unsatisfactory; switched to native nonwrapping columns/native wordmark, then identified the fixed Streamlit toolbar covering the header and restored sufficient top padding. Final 400px screenshot showed wordmark/Home/Exit sample in one row below the toolbar and a two-by-two feedback summary. Native screenshots inspected, no new repository screenshot asset. Device width setValue briefly produced width 1 instead of 768; typing the width through the UI corrected it. DevTools was closed and a normal desktop Home preview restored. No paid extraction/review clicked; fixed sample output is not model-quality evidence.

Browser console showed no messages at the inspected moment; Issues reported empty autocomplete attributes (3–5 affected form fields across pages). Inspected that warning and recorded it as a remaining native-form usability issue, without changing auth/autocomplete behavior in an aesthetic pass. Real hardware/phone, dark override, exhaustive keyboard/screen-reader/long-content, all semantic feedback colors in actual model outputs and live PostHog/replay verification remain pending. No full accessibility/security audit claim.

Working tree remains based on 1d34206; no commit/push, public app deployment, cloud project setup, schema migration or coursework persistence. Incremental inference cost $0; active builder time, development and service costs unreported. Real Supabase ownership/email tests, full audit, spend protection, required refused-access screenshot and live deployment are still outstanding. User asked whether this part was almost finished; agent reported design/checks complete and documentation in progress, not final builder acceptance.

## November 17 — Save-and-push checkpoint

Builder requested committing/pushing all current work. Plan.md now contains the consolidated resume instructions, implemented boundaries, latest recorded checks and next Supabase setup/security steps. Full evidence/pre-commit scan is in tests/README.md. No new application/analytics suites or model calls; no public app deployment or migration. Actual commit/push outcome is verified through Git after this note.
