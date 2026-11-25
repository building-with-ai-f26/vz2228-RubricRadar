# Rubric Radar — existing visual system

Updated November 25, 2026 after a full Streamlit polish pass using the upstream
Impeccable polish, Operate and craft-floor guidance.
Product scope and evidence live in PRD.md and tests/README.md.

## Direction

Minimal, familiar and quiet. Preserve the builder-approved Home → Class → Project →
Review structure, guest/demo entry, explicit saves and existing button labels.
No sidebar, promotional claims or decorative imagery. Use warm-white surfaces
and slate actions. Reserve class and feedback colors for identity and status.

## Implementation

- app_style.css owns shared presentation; .streamlit/config.toml supplies the light
  default. Keep coursework and model text in native escaped Streamlit widgets.
- library_ui.py contains the native wordmark, navigation, class/project title
  wrappers and read-only snapshot presentation. feedback_ui.py contains keyed
  feedback sections; status styles belong in the shared stylesheet.
- No remote fonts, image assets or added runtime packages. Preserve native controls
  and their keyboard semantics. CSS uses a system sans stack with Streamlit's
  native sans fallback; metadata, titles and controls have explicit roles.

## Type and spacing

- Home display: 3.65rem desktop, 3rem at <=800px, 2.75rem at <=640px. The
  introduction and entry actions sit side by side on desktop and stack on mobile.
- Page titles: 2rem, reducing to 1.75rem on narrow screens.
- Section headings: 1.125rem; class/project titles: 1.2rem, weight 600.
- Body/editor: 1rem with comfortable leading; captions: .875rem with explicit
  readable foreground rather than opacity. Heading tracking never below -.035em.
- Maximum content width: 960px, with 2.2rem desktop / 1rem mobile side gutters.
- Top padding clears Streamlit's fixed toolbar (3.9rem / 3.75rem mobile).
- Group related information tightly; keep separate sections clearly apart.

## Color and surfaces

- Primary actions use slate `#26364a`, and focus rings use `#526d88`. Main
  background is `#f7f7f4`, with white panels and recessed surfaces in `#eceeea`.
- Muted text uses `#4e5a67`. Rules and panel borders use `#c8cfd2`.
- Existing stable class palette: blue, mint, violet, peach, rose and sand. Color
  comes from the class UUID, survives renames/order changes, and may repeat.
  Class names remain the primary identifiers. No new database color field.
- Class/project cards use light tints and a thin class-colored border. Use darker
  hue-related metadata on tinted surfaces. Context labels use a thin neutral
  outline with the matching class tint.
- Review status is separate from course identity: green Met, amber Partially Met,
  red Missing, blue Needs Review. Keep written statuses visible. Use light tints,
  thin outlines and readable state-colored text; do not rely on color alone.
- Card radius 12px, controls and expanders 10px. Primary buttons use a single
  soft shadow. Secondary buttons use an outline. Tertiary actions use text.

## Interaction and responsive behavior

- Buttons retain primary/secondary/tertiary roles; target minimum height 44px.
  Explicit focus rings, caret and selection colors. Hover transitions are 160ms;
  reduced-motion preference disables them. No page entrance choreography.
- Native top-bar columns do not wrap; space the wordmark and existing account
  actions so they remain visible on a 400px viewport.
- Class/project columns wrap on small screens. The feedback metrics become two
  columns at <=640px rather than one very tall four-item stack.
- Keep text inputs labeled, error/recovery messages intact and disabled sample
  controls disabled. Preserve consent, masking, routing and archive gates.

## Verification and limits

November 25 used the upstream Impeccable 4.11.0 guidance directly. The local
launcher was unavailable, so the pass used this file and the existing UI as
context. See the test log for Chrome walkthroughs, automated checks and limits.

On November 17, source calculation checked 12 declared text/background pairs (minimum 5.33:1),
not every rendered state. Local Chrome visually checked desktop Home/library/
editor/saved feedback, 400px Home/library/editor/summary, and 768px feedback.
These are emulated layouts, not real-phone tests. Dark override, full keyboard/
screen-reader checks, all long-content cases and complete live replay remain
pending. Browser Issues reported empty autocomplete attributes on native form
fields (3–5 affected fields across pages); this was inspected, not fixed by the
visual pass. Do not claim a full accessibility or security audit.
