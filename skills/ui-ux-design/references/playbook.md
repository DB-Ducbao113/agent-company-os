# UI/UX Playbook — Deep Reference

> Read while working Gate 3. SKILL.md gives the workflow; this file gives the lookup detail.

## 1. The 3-Tier Source System (Detail)

### Tier 1 — Deciding standards (beat every lower tier)
| Source | What it decides |
|---|---|
| The project's design system + brand (PROJECT-PROFILE) | Tokens, components, identity colors, icons, logo — the highest law inside the project |
| WCAG 2.2 (AA level) | Contrast, focus, target size, never conveying information by color alone |
| Nielsen Norman Group — 10 Usability Heuristics | Self-auditing a flow: visibility of system status, match with the real world, user control, consistency, error prevention, recognition over recall, flexibility, minimalism, understandable error messages, help |
| Apple Human Interface Guidelines — Liquid Glass era (iOS 26+, 2025) | iOS/macOS platform patterns: navigation, touch areas, dynamic typography. Glass material belongs to the control/navigation layer only, never the content layer; test with Reduce Transparency on and at both clarity extremes (clear ↔ opaque) |
| Material 3 Expressive (2025+, Android 16 era) | Android/web platform patterns: spring-physics motion, expressive shapes and type scale, dynamic color, 48dp touch targets, adaptive layout |

**AI disclosure:** whenever a feature interacts with users as AI or generates synthetic content, the disclosure UI (see `references/ai-feature-ux.md`) is a design deliverable — users must be told they are interacting with AI at first interaction, not in a terms-and-conditions line.

### Tier 2 — Searchable design data
- **UI/UX Pro Max:** look up by product type (dashboard, e-commerce, SaaS, health app…) and stack.
  Its real value is the *reasoning rules* — why this product type suits that layout/palette —
  not copying a palette wholesale. Always cross-check lookup results against the project's DS before using them.
- **The project's own internal data:** analytics, real user feedback, support tickets — when it exists,
  this data outweighs every external lookup table.

### Tier 3 — Inspiration (never the sole basis for a decision)
| Source | What to learn | Warning |
|---|---|---|
| Mobbin, Page Flows, Refero, Screenlane | Complete flows from real apps: onboarding, checkout, paywall, settings | Learn flow structure; do not copy the brand |
| Behance | Complete case studies: problem → process → result | Presented results are usually polished and omit bad states |
| Awwwards, Godly | Peak web visuals, motion, typography | Many award sites sacrifice performance and accessibility |
| Dribbble | Visual direction, mood, micro-detail | Static concepts: no real data, no edges, no errors — never use as an interaction pattern |

**Citation rule:** every major decision in `03-design.md` records which tier its source belongs to.
A decision based only on Tier 3 must be marked as a judgment call and requires the approver's confirmation.

## 2. The 5-State Spec (Detail per State)

| State | Must include | Common mistake |
|---|---|---|
| Default | Real content in the correct hierarchy; the primary action most prominent; unusually long/short data does not break the layout | Testing only with "just right" data; long text overflowing its cell |
| Loading | A skeleton that keeps the real layout frame; a clear waiting position; actions not yet usable are deliberately disabled/dimmed | A spinner on a blank page; layout jumping when data arrives |
| Empty | Distinguish "no data has ever existed" (getting-started guidance + CTA) from "filter/search found nothing" (say so + a clear-filters button) | A blank page, or a bare "No data" sentence |
| Error | The error in user language; distinguish network errors / permission errors / invalid-input errors; always a recovery path; preserve entered data | Showing technical error codes; forcing re-entry from scratch; an error with no retry button |
| Success | Confirmation of what just happened + its consequence + the next step; the new state reflected immediately in the UI | The user cannot tell whether the action succeeded; having to reload the page to see it |

Quick check: for each screen, ask "what does the user see in the first second when nothing exists yet,
when the network is dead, and right after pressing the most important button?" — you may only pass when
you can answer all three.

## 3. Condensed WCAG 2.2 AA Table (the most-used floor)

| Criterion | Required level |
|---|---|
| Contrast, normal text (< 18pt, or < 14pt bold) | ≥ 4.5:1 |
| Contrast, large text (≥ 18pt, or ≥ 14pt bold) | ≥ 3:1 |
| Contrast, UI components & essential graphics (input borders, functional icons, focus state) | ≥ 3:1 |
| Touch target size (AA 2.2) | ≥ 24×24 CSS px; practical recommendation 44×44 pt (iOS) / 48×48 dp (Android) |
| Visible focus | The focus state must be clearly visible during keyboard navigation; never remove the outline without a replacement |
| Not by color alone | Status/errors/right-wrong must have a second signal: icon, text, position, or pattern |
| Motion | Respect `prefers-reduced-motion`; never flash more than 3 times per second |
| Text resize | No content lost when text is scaled to 200% |
| Form labels & errors | Every input has a visible label; errors are attached to the correct field and readable by a screen reader |
| Heading order & landmarks | Heading structure follows a logical hierarchy; never skip levels for visual effect |

Practical note: many "clean-looking" interfaces achieve the look with pale gray text below AA.
Do not copy that — create the light feeling with hierarchy and whitespace, not with low contrast.

## 4. Method for Researching Real Products

1. **Pick the right samples:** same product type first, same pattern second (another industry's checkout
   flow still teaches you about checkout). Prefer products in production with real users.
2. **Walk the whole flow, do not just admire the pretty screen:** sign up → first use → empty state →
   primary action → hit an error → come back. The most valuable patterns usually live in how they handle
   bad situations.
3. **Record evidence:** screenshots/notes per step, not general impressions ("this app is beautiful").
4. **Separate "learn" from "copy":** learn = the principle (hierarchy, density, grouping);
   copy = lifting their exact colors/brand/signature layout. Only learning is allowed.
5. **Cross-check against your own constraints:** a large product's pattern may depend on infrastructure
   or a team your project does not have (A/B testing, personalization) — record the applicability
   conditions when entering it into the research table.

## 5. Design Audit Checklist (run before submitting the gate)

**Hierarchy & layout**
- [ ] Within 3 seconds it is clear what this screen is for and where the primary action is
- [ ] No two actions both claim to be "primary" on one screen
- [ ] Related information sits close together; whitespace is systematic (follows the spacing scale)

**System consistency**
- [ ] 100% of colors/spacing/radii/font sizes come from tokens; every exception is listed with a reason
- [ ] No two different versions of a same-function component exist
- [ ] UI terminology matches the terminology in the BA/spec (one concept, one name)

**Interaction & states**
- [ ] All 5 states covered; every button gives feedback (state change, loading, or a result)
- [ ] Destructive actions have confirmation or undo
- [ ] No action forces the user to choose something the system already knows automatically

**Accessibility**
- [ ] Contrast meets the section 3 table for every text/background pair, including hover/disabled/color-label states
- [ ] The main flow is fully keyboard-navigable, with focus always visible
- [ ] No information is conveyed by color alone

**Perceived performance**
- [ ] Loading keeps the frame; no layout jumping
- [ ] Images/media have reasonable sizes and formats; a light option exists if the project targets weak devices

## 6. Anti-AI-Slop List (signs of careless AI-made UI)

- The default purple–blue gradient on every surface, unrelated to the brand.
- Cards nested inside cards, many layers deep, with identical corner radii and shadows everywhere.
- The framework's default font used at every type level; no typography scale.
- Every section is "hero + 3 feature columns + CTA button" regardless of content.
- Emoji icons, or icons mixed from several sets; decorative icons that carry no meaning.
- Pale gray text on colored backgrounds "for a refined look" (usually below AA).
- Arbitrary spacing: every screen a different spacing, following no scale.
- Generic stock/placeholder imagery unrelated to the real content.
- Identical motion on every element (the same fade-up in sequence), with no distinction between important and secondary.
- Badge, pill, and status-label overuse: everything has a badge.
- Decorative statistics with no source (fake stats) used to fill empty space.
- Dark mode made by mechanically inverting colors, without re-checking contrast.

If ≥3 of these signs appear in one artifact → treat it as not yet audited, and return to Step 8 of SKILL.md.

## 7. Notes on Forms (the UI type that goes wrong most often)

- Labels are always visible (a placeholder is not a label); format hints go under the label or in a helper field.
- Validate in place when leaving a field; the error states exactly what is wrong + how to fix it, placed
  directly under the field.
- Group related fields under headings; split long forms into steps and show progress.
- The primary button names the exact action ("Create account", "Pay $250.00") instead of "OK"/"Submit".
- Never ask for a field the system can derive itself; mark optional fields clearly under one convention
  (or mark only required fields — pick ONE convention and stay consistent across the whole project).
