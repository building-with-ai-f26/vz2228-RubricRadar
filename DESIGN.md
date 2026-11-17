# Rubric Radar — existing visual system

Updated November 17, 2026 after the builder requested Impeccable-guided aesthetic
refinement. This records the current implementation, not an unrelated redesign.
Product scope and evidence live in PRD.md and tests/README.md.

## Direction

Minimal, familiar and quiet. Preserve the builder-approved Home → Class → Project →
Review structure, guest/demo entry, explicit saves and existing button labels.
No sidebar, promotional claims, decorative imagery or added navigation controls.
Keep the main action blue and let typography/spacing carry hierarchy.

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

- Home display: 3.75rem desktop, 2.75rem at <=640px; natural balanced wrapping.
- Page titles: 2rem, reducing to 1.75rem on narrow screens.
- Section headings: 1.125rem; class/project titles: 1.2rem, weight 600.
- Body/editor: 1rem with comfortable leading; captions: .875rem with explicit
  readable foreground rather than opacity. Heading tracking never below -.035em.
- Maximum content width: 960px, with 2.2rem desktop / 1rem mobile side gutters.
- Top padding clears Streamlit's fixed toolbar (4.5rem / 4.25rem mobile).
- Group related information tightly; keep separate sections clearly apart.

## Color and surfaces

- Action/focus blue: #0066cc. Muted text: #606975; rules: #dfe4eb; panels: white.
- Existing stable class palette: blue, mint, violet, peach, rose and sand. Color
  comes from the class UUID, survives renames/order changes, and may repeat.
  Class names remain the primary identifiers. No new database color field.
- Class/project cards retain light tints and a 3px top accent. Use darker
  hue-related metadata on tinted surfaces. Context labels use a thin neutral
  outline with the matching class tint, rather than a heavy side stripe.
- Review status is separate from course identity: green Met, amber Partially Met,
  red Missing, blue Needs Review. Keep written statuses visible. Use light tints,
  thin outlines and readable state-colored text; do not rely on color alone.
- Card radius 14px, controls/expanders 10px. Use borders without stacked shadows.

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

Impeccable 4.9.2 is installed in the user's Codex skills folder. Its polish and
Operate/craft-floor references informed the changes. Context launch initially
failed due to executable permission; the launcher permission was repaired, but
context/detector/hooks were not run afterwards. No automatic detector pass is
claimed. The skill is discoverable on the next turn; its instructions were read
and applied directly in this turn.

Source calculation checked 12 declared text/background pairs (minimum 5.33:1),
not every rendered state. Local Chrome visually checked desktop Home/library/
editor/saved feedback, 400px Home/library/editor/summary, and 768px feedback.
These are emulated layouts, not real-phone tests. Dark override, full keyboard/
screen-reader checks, all long-content cases and complete live replay remain
pending. Browser Issues reported empty autocomplete attributes on native form
fields (3–5 affected fields across pages); this was inspected, not fixed by the
visual pass. Do not claim a full accessibility or security audit.
