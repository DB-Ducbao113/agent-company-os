# Design Systems — Deep Dive

> Read when: the task creates, extends, or audits a design system, or a design decision needs a rule instead of an opinion.
> Companion: `playbook.md` covers research, states, and audits; this file covers the system itself — tokens, type, space, components, theming, motion, and handoff.

## 1. Token Architecture — Three Layers, No Exceptions

Design tokens are the single source of truth for visual decisions. Raw values (hex, px) may exist in exactly ONE layer.

| Layer | Holds | Example names | Who may use it |
|---|---|---|---|
| 1. Primitive (global) | Raw values, no meaning | `color.blue.500`, `space.4`, `radius.md` | Only Layer 2 |
| 2. Semantic (alias) | Meaning, mapped to primitives | `color.action.primary`, `color.surface.raised`, `text.body.size` | Components, screens |
| 3. Component | Per-component decisions, mapped to semantic | `button.primary.bg`, `card.padding`, `input.border.focus` | That component only |

Rules:
- **Never style a screen from Layer 1.** A screen full of `blue.500` cannot be rethemed, rebranded, or dark-moded.
- **Semantic names describe role, not appearance.** `color.text.muted` survives a palette change; `color.text.gray` does not.
- **Naming pattern:** `category.property.variant.state` — lowercase, dot-separated, no abbreviations that need a glossary (`bg` and `fg` are acceptable only if the whole team uses them consistently).
- One token, one job. If `color.action.primary` is also used for links, charts, and selection, it is three tokens pretending to be one — split them before the first rebrand forces you to.

Sample token table (excerpt):

| Token | Layer | Light value | Dark value |
|---|---|---|---|
| `color.blue.500` | Primitive | `#2563EB` | `#2563EB` |
| `color.action.primary` | Semantic | `color.blue.500` | `color.blue.400` |
| `color.surface.base` | Semantic | `color.neutral.0` | `color.neutral.950` |
| `color.text.primary` | Semantic | `color.neutral.900` | `color.neutral.50` |
| `button.primary.bg` | Component | `color.action.primary` | `color.action.primary` |
| `space.inset.card` | Component | `space.4` (16px) | same |

Worked micro-example — one component token set (Button, primary variant):

| Component token | Maps to | Notes |
|---|---|---|
| `button.primary.bg` | `color.action.primary` | Hover uses `color.action.primary.hover`, a separate semantic token — never a manually darkened value |
| `button.primary.fg` | `color.text.on-action` | Guaranteed-contrast foreground for action surfaces, checked as a pair in both themes |
| `button.primary.radius` | `radius.md` | Shared with inputs so adjacent controls align visually |
| `button.primary.padding-inline` | `space.4` | Size variants override this one token, nothing else |
| `button.primary.font` | `text.body` + weight 600 | Buttons do not get their own typeface rules |

Decision rules when naming gets argued:

| Situation | Rule |
|---|---|
| Two screens need "almost the same" color | Same semantic token if the ROLE is the same; new token only if the role differs |
| A value is used in exactly one place | It still gets a token if it expresses a role (error, success); one-off decoration is a smell |
| Marketing wants a one-off campaign color | Primitive token + a campaign-scoped semantic token with an expiry review date (Section 10) |
| A platform forces a different value (iOS vs. Android) | Same semantic token, per-platform primitive mapping — the meaning stays unified |

## 2. Typography System

- **One scale ratio, applied mechanically.** Pick a ratio (1.25 major third for dense product UI, 1.333–1.5 for marketing/editorial) and derive every size from a base of 16px. Hand-picked sizes are how systems rot.
- **Line-height by role:** headings 1.1–1.25, body 1.45–1.6, captions/labels 1.3–1.4. Line-height is unitless in code (multiplier), never a fixed px.
- **Measure (line length):** 45–75 characters for body text. Wider text gets multi-column or a max-width container — never full-bleed paragraphs.
- **Tabular numbers** (`font-variant-numeric: tabular-nums`) are mandatory anywhere numbers align vertically or update live: tables, prices, timers, stats. Proportional figures in a price column are a defect.
- **Weights:** ship at most 3 (regular, medium/semibold, bold). A fourth weight is a new token decision, not a local choice.
- **Never set type in px in product code** — rem/em so user font-size settings work; that is an accessibility requirement, not a preference.

Sample type scale (ratio 1.25, base 16):

| Role token | Size | Line-height | Weight | Use |
|---|---|---|---|---|
| `text.display` | 39px | 1.15 | 700 | Hero headline only |
| `text.h1` | 31px | 1.2 | 700 | Page title |
| `text.h2` | 25px | 1.25 | 600 | Section title |
| `text.h3` | 20px | 1.3 | 600 | Card/group title |
| `text.body` | 16px | 1.55 | 400 | Default reading text |
| `text.body-sm` | 14px | 1.5 | 400 | Secondary text, dense lists |
| `text.caption` | 12.8px | 1.4 | 500 | Labels, meta, timestamps |

## 3. Spacing & Layout Grid

- **Base unit 4px; rhythm on 8.** All spacing tokens are multiples of 4: `space.1`=4, `space.2`=8, `space.3`=12, `space.4`=16, `space.6`=24, `space.8`=32, `space.12`=48, `space.16`=64. Values like 13px or 22px in a spec mean the layout was eyeballed — send it back.
- **Inset vs. stack vs. inline:** name spacing by relationship (padding inside a container = inset; vertical gap between blocks = stack; horizontal gap = inline). Same numbers, clearer intent.
- **Containers:** define max content widths per content type (reading ~720px, app shell ~1280px, data-dense ~1440px or fluid with a cap) — "full width" is not a layout decision.
- **Grid:** 12 columns on desktop, 4 on mobile, gutters = `space.6` desktop / `space.4` mobile, margins = gutter. Components span columns; they never invent their own widths.
- **Breakpoint strategy:** content-driven, not device-driven. Add a breakpoint where the layout actually breaks. Name them by range (`compact`, `medium`, `expanded`), never by device (`iphone`, `ipad`) — devices change, ranges don't.

## 4. Component Specification Anatomy — The 12 Required Parts

A component is not specified until all 12 exist. A spec missing any row is incomplete and Dev will (correctly) improvise the missing parts.

| # | Part | Must state |
|---|---|---|
| 1 | Purpose & non-purpose | What it is for, and what it must NOT be used for |
| 2 | Anatomy | Named parts (container, label, icon slot, helper text…) with a diagram or labelled list |
| 3 | Variants | Each variant and the rule for choosing it (primary vs. secondary is a decision rule, not taste) |
| 4 | States | Default, hover, focus-visible, active, disabled, loading, error — every state the variant can be in |
| 5 | Sizes | Size tokens and when each applies |
| 6 | Props/API | Name, type, default, required? — written so a developer can build the interface without asking |
| 7 | Content rules | Max label length, truncation behavior, empty/missing content behavior, localization expansion allowance (+30% length) |
| 8 | Accessibility | Role/element semantics, focus order, keyboard interaction, target size (≥44px touch, ≥24px pointer minimum), contrast of every state |
| 9 | Motion | Which transitions, which motion tokens (Section 7), what happens under reduced-motion |
| 10 | Responsive behavior | What changes at each range: stack, hide, truncate, scroll — explicitly, per range |
| 11 | Do / Don't | At least 2 of each, with visuals or concrete examples |
| 12 | Tokens used | The Layer 2/3 tokens it consumes — no raw values anywhere in the spec |

## 5. Theming & Dark Mode

- **Dark mode is a token remap, not a redesign** — but only if Sections 1–2 were obeyed. Semantic tokens get new primitive mappings; components and screens change zero code.
- **Dark surfaces are not inverted light surfaces.** Dark base is rarely pure black (use a very dark neutral, e.g. `#0B0E14`-family) except for OLED-true-black themes, which are a deliberate product choice.
- **Elevation in dark mode = lighter surface**, not shadow (shadows are invisible on dark). Encode elevation in surface tokens per theme.
- **Contrast is checked per theme, per pair.** A pair that passes in light can fail in dark (mid-gray text is the classic casualty).

Contrast pair table (minimums, WCAG 2.2 AA):

| Pair | Minimum | Common failure |
|---|---|---|
| Body text on its surface | 4.5:1 | "Muted" text at 3.8:1 shipped as decoration |
| Large text (≥24px, or 19px bold) | 3:1 | Display type over photography with no scrim |
| Interactive component boundary vs. adjacent | 3:1 | Ghost button border invisible in dark mode |
| Focus indicator vs. adjacent colors | 3:1 | Focus ring that only differs by hue |
| Icon conveying meaning (not decorative) | 3:1 | Status icons failing on tinted backgrounds |
| Disabled state | Exempt from WCAG, but must stay legible as "present but unavailable" | Disabled text so faint it reads as missing |

- **Theme QA rule:** every new semantic token ships with both theme values in the same change. A token with only a light value is an unfinished token.

## 6. Icon System Construction

- **Derive icons from the product's own brand mark and visual language** — its geometry, angles, and metaphors. Generic emoji-style or mixed-stock icons break identity and are never acceptable as a system.
- **One construction grid:** 24×24 viewBox, 2px keylines/padding safe area, all icons drawn on the same grid at the same optical size.
- **One stroke rule:** single stroke weight across the set (1.5px or 2px at 24px grid — pick one), same corner radius on strokes and shapes, same cap/join style. Mixing filled and outline styles is allowed only as a deliberate active/inactive pair.
- **Optical correction beats mathematical sameness:** circles and triangles are drawn slightly larger than squares to *look* the same size.
- **Icons are components, not images:** they consume `color.icon.*` tokens, scale by token sizes (16/20/24), and every meaning-bearing icon has a text label or accessible name — icon-only controls get an `aria-label` in the spec.
- **Test at 16px.** If the metaphor dies at the smallest shipped size, simplify the drawing; never ship a detailed icon that only works large.

## 7. Motion System

Motion is tokenized like color. Durations and easings are chosen by distance and purpose, never per-screen.

| Token | Duration | Easing character | Use |
|---|---|---|---|
| `motion.duration.instant` | 80–120ms | ease-out | Hover/press feedback, toggles |
| `motion.duration.short` | 150–200ms | ease-out | Tooltips, small reveals, chip changes |
| `motion.duration.medium` | 250–350ms | ease-in-out | Panels, modals, tab content, layout shifts |
| `motion.duration.long` | 400–600ms | ease-in-out | Page-level transitions, large surface changes |
| `motion.duration.emphasis` | 600ms+ | spring/custom | Rare, brand moments only — needs explicit justification |

Rules:
- **Exits are shorter than entrances** (roughly 70–80%): leaving should never feel slower than arriving.
- **Animate transform and opacity only** in product UI; animating layout properties (width, top, margins) causes jank and layout thrash.
- **Reduced motion is a spec item, not a dev afterthought:** under `prefers-reduced-motion`, replace slides/springs with fades or instant changes; remove parallax and auto-playing motion entirely.
- **Data-driven motion exception:** motion that visualizes real data changing (a value counting, a live position moving) is functional, and follows the data's own timing — but still respects reduced-motion by simplifying, not by faking data.

## 8. Design-to-Code Handoff Protocol

What the designer owes the developer — the handoff is incomplete without all of it:

- [ ] Every screen/flow in the agreed state set (default, loading, empty, error, success — per the playbook's 5-state rule), not just the happy path
- [ ] Token names, not raw values, annotated on components and spacing ("redlines" reference `space.4`, `color.text.muted`)
- [ ] Component specs per Section 4 for anything new or changed
- [ ] File/frame naming convention: `Flow / Screen / State` (e.g. `Checkout / Payment / Error-card-declined`) — no "final_v2_REAL" frames
- [ ] Assets exported in the agreed formats with the agreed naming (`icon/<name>`, `img/<name>@2x`), illustrations as SVG where possible
- [ ] Interaction notes for anything a static frame cannot show: what triggers it, duration/easing tokens, what interrupts it
- [ ] A changelog note in the design file: what changed since the last handoff, so Dev diffs instead of re-reading everything

Developer's side of the contract: build from tokens and specs; where the spec is silent, ask — a guessed value that ships becomes an untracked design decision.

## 9. Design QA — Comparing Build vs. Design

- **Compare at the same viewport, same data, same state.** Most "design bugs" reported are state mismatches (comparing an empty build against a full-data mock).
- **Tolerance rules:** spacing/size deviation ≤2px = pass (rendering noise); 3–4px = log as minor; ≥5px or any wrong token (color, type size, radius) = defect. Color is exact — a near-miss hex is the wrong token, full stop.
- **Check in this order:** layout/spacing → typography (size, weight, tabular numbers where required) → color tokens → states (force hover/focus/disabled/error, don't wait to stumble on them) → motion (duration feel + reduced-motion) → responsive at each range boundary ±1px.
- **Evidence:** side-by-side screenshots with the deviation annotated; "looks off" without a marked screenshot is not a QA finding.
- Findings route back by ownership: wrong token/value in code → Developer; wrong value in the spec → UI/UX fixes the spec first, then Dev re-implements. Never patch the build to differ from the spec silently.

## 10. Maintaining the System

- **Components are versioned like APIs.** A breaking change (removed variant, renamed prop, changed default) is a major bump with a migration note; additive changes are minor.
- **Deprecation protocol:** mark deprecated → announce replacement + reason → keep working for an agreed window → remove only when usage is zero (search the codebase; don't trust memory).
- **One owner per component.** Unowned components drift; the owner approves changes to spec and tokens for that component.
- **Adoption is measured:** periodically count screens built from system components vs. one-off styles. A falling ratio means the system is missing something teams need — find out what before enforcing harder.
- **Change requests follow the same gate discipline as features:** a new token/variant enters through a spec (why existing ones fail), not through a single screen's local need. One-off exceptions are recorded as exceptions with an expiry review date.
- **Design debt is tracked like tech debt:** every known deviation (hardcoded value, missing state, forked component) is logged with an owner and a reason. A short, honest debt list is healthy; discovering deviations in QA, sprint after sprint, means the system process — not the designers — is failing.
- **System documentation lives where builders work:** each component's spec (Section 4), tokens table, and do/don't examples are published in the same place the team already looks (design tool + repo), versioned together. A beautiful system site nobody opens loses to an ugly page everybody uses.
