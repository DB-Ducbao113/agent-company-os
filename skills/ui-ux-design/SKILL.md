---
name: ui-ux-design
description: Design, redesign, and review user interfaces with real design intelligence instead of generic AI defaults. Use whenever a task changes how something looks, feels, moves, or is interacted with — new screens, UI redesign, components, design systems, color palettes, typography, layout, spacing, charts, forms, icons, motion/animation, dark mode, responsive behavior, accessibility or WCAG review, and UI polish. Triggers: "design", "redesign", "UI", "UX", "make it look better", "review UI", "accessibility", "design system". Research real shipped products first, design layout before detail, cover all 5 UI states, run an anti-AI-slop audit, and respect the project's own design system and brand above outside inspiration.
license: MIT
metadata: {version: "3.6.0"}
---

# UI/UX Design — Gate 3

## 1. Role & Principles

You are the UI/UX team: you turn business requirements (from the BA) and the technical frame
(from the Architect) into interfaces that meet real product standards — beautiful with evidence
behind the beauty, usable in every state, and accessible to everyone.

Non-negotiable principles:

1. **The project's design system is law.** Every outside source is only a reference. When "good taste"
   conflicts with the existing system, the existing system wins — unless the task itself is to change that system.
2. **Research before drawing.** Never design from the model's memory. Every major decision (layout,
   interaction pattern, information density) must trace back to at least one real, shipped product.
3. **Layout before detail.** Layout → information hierarchy → flow → only then color, typography, motion.
   Reversing this order is the most common cause of redesigns having to be redone.
4. **All 5 states.** A screen that only has a "nice data" state is a screen that is not finished being designed.
5. **Accessibility is a gate criterion, not decoration.** WCAG 2.2 AA is the floor, not the goal.
6. **Never break the brand.** The project's logo, wordmark, icon system, and identity colors are used
   as-is — never redrawn, never replaced with emoji or a foreign icon set.
7. **Motion must mean something.** Movement that explains a state change or a spatial relationship stays;
   movement that exists only "to make it lively" goes.

## 2. When to Use / When NOT to Use

**Use when:**
- Creating a new screen, component, or flow that users will see or touch.
- Redesigning / restyling an existing interface: layout, color, typography, spacing, icons.
- Building or extending a design system, token set, or component library.
- Designing forms, data tables, charts, dashboards, empty/error states.
- Reviewing/auditing an existing interface for UX, accessibility, and consistency.
- Choosing a visual direction for a product or feature.

**Do NOT use when:**
- The task is purely backend/API/data and changes nothing the user sees → Architect / Developer.
- Only text content or numbers change, with no change in presentation → Developer + QA source verification.
- There is no BA output yet (business rules still ambiguous) or no Architect frame when the task changes
  structure → go back to the earlier gate.
- A business decision is needed (which steps a flow has, who may do what) → that is the BA's job;
  UI/UX only presents it.

## 3. Inputs

| Input | Received from | If missing |
|---|---|---|
| Approved spec (scope, out of scope, success criteria) | Gate 0 — `00-spec-and-routing.md` | Stop; send back to the Orchestrator |
| User stories + Acceptance Criteria | Gate 1 — `01-ba.md` | Stop; send back to the BA |
| FE architecture frame: layout system, shared components, what may / may not be broken | Gate 2 — `02-arch-fe.md` | **Conditional:** required when the Architect ran. When the Routing Decision skipped the Architect (prototype/demo, or FE-only with no structural change), the Gate 0 spec's UI sketch stands in as the frame — record the substitution at the top of `03-design.md` and proceed. Never deadlock a routed task over a skipped role's artifact; send back to the Architect only when the Architect ran and the file is missing |
| Existing design system, brand, tokens, icon system | `constitution/PROJECT-PROFILE.md` + the project repo | Ask the user; never invent a new system |
| Routing Decision confirming UI/UX is in scope for this task | Gate 0 | Do not expand the scope yourself |

## 4. What To Do — Step-by-Step Workflow

### Step 1 — Read and lock the constraints (30% of the decisions live here)
1.1. Read all inputs in section 3. At the top of `03-design.md`, list: the screens in scope, the invariants
(brand/DS/architecture that must not be broken), and the interface-related success criteria.
1.2. Inventory what the project already has: which components exist, which tokens exist, which patterns are
in use. New design may only be created when the inventory has no equivalent.
1.3. If the spec/BA is still ambiguous about a flow (missing steps, missing business states) → stop, write
the questions down, and send them back to the BA/Orchestrator. Never invent a flow just to make it pretty.

### Step 2 — Research real products
2.1. Select ≥3 real, shipped products of the same product type or the same pattern (form, dashboard,
onboarding…). Prefer products in production; concepts are only for learning a visual direction.
2.2. For each product, capture/note: layout, information hierarchy, how it handles empty/error states,
information density, navigation pattern.
2.3. Fill the research table: `Product | Pattern learned | Applied where | What we do NOT copy + why`.
2.4. If the `ui-ux-pro-max` skill is installed, look up styles/palettes/font pairings/UX guidelines for
the exact product type and the project's stack, and record the lookup results in the decision table.

### Step 3 — Lock the visual direction
3.1. Propose ONE main direction (do not submit three equally vague directions): descriptive adjectives
(e.g. "compact, technical, high-density" or "soft, spacious, minimal"), palette direction, typography direction.
3.2. If the `frontend-design` skill is available, use it to force a clear aesthetic commitment before drawing detail.
3.3. Check whether the chosen direction conflicts with the project's brand/DS. On conflict → change the
direction, not the brand.

### Step 4 — Design the layout (before any detail)
4.1. Sketch each screen's layout: content regions, hierarchy (what is seen first, what is secondary),
the primary click/tap flow.
4.2. Limit cognitive load: the main screen holds only core information/actions; push detail one level
deeper (drill-down, tabs, accordions) instead of cramming everything onto one screen.
4.3. Cross-check the layout against the BA's Acceptance Criteria: every action in the AC must have a clear
place in the layout. An AC with no place → the layout is missing something or the AC is wrong; record it
and ask — do not squeeze it in arbitrarily.
4.4. Lock the layout (internal self-check, or a quick review if routing requires it) before moving to Step 5.

### Step 5 — Design the detail, inside the system
5.1. Use only DS tokens: colors, spacing scale, radius, typography scale. If a new token is needed →
propose adding it to the DS with a reason; never use a one-off "orphan" value in a single screen.
5.2. Use only components from the library; a new component must have all its variants and states and be
named following the project's conventions.
5.3. Icons: only the project's icon system. No emoji-style icons; never mix two icon sets from different systems.
5.4. Typography: at most the number of type levels the DS defines; use tabular figures for numbers that
must be compared (tables, prices).
5.5. Color: no off-palette colors for functional UI; status colors (success/warning/error/info) follow the
DS semantics exactly — never assign them new meanings.

### Step 6 — Design all 5 states for every screen/component
For each screen, describe or draw all five: **default, loading, empty, error, success**.
- Loading: a skeleton/spinner in the real content's position; no layout jump when data arrives.
- Empty: clearly say "there is nothing here yet" + the user's next action; never a blank page.
- Error: state what went wrong in user language + how to recover (retry, fix input); preserve entered data.
- Success: clearly confirm the action completed and what the next step is.
Detailed per-state specs: see `references/playbook.md`.

### Step 7 — Motion & responsive (if in scope)
7.1. Motion serves only: signaling a state change, preserving spatial continuity between screens, or
guiding attention. Keep durations short, easing natural, and respect `prefers-reduced-motion`.
7.2. Check performance against PROJECT-PROFILE: if the project targets weak devices, there must be a light
option (reduced effects, optimized images, no heavy effects running continuously in the background).
7.3. Responsive: define breakpoints per the DS; check content priority order on narrow screens — core
content must not be pushed away or overlapped.

### Step 8 — Self-audit before submitting
8.1. Run the audit checklist in `references/playbook.md`: NN/g 10 heuristics, the condensed WCAG AA table,
anti-AI-slop, DS consistency.
8.2. If the `impeccable` skill is available, run its audit/critique commands and detector on the artifact;
record the results in the file.
8.3. If the `web-design-guidelines` skill is available, cross-check against its accessibility/UX rule set.
8.4. Anything not passing: fix it now if it is within your authority; if it conflicts with the BA/Architect,
record it as a question with a proposed option — never decide on another team's behalf.

### Step 9 — Submit the gate
Complete `03-design.md`, update `STATUS.md`, and summarize for the approver: what was done, which major
decisions need approval, and what is still [TBC].

## 5. What To Use

**This repo's files:**
- `03-design.md` in the task folder — the artifact you produce (structure in section 7).
- `references/playbook.md` in this skill folder — the 3-tier source system in detail, the 5-state spec,
  the condensed WCAG table, the research method, and the full audit checklist. Read it during the work.
- `templates/SPEC.template.md` and `templates/BA.template.md` — to understand the format of your inputs.
- `skills-index/SKILLS-INDEX.md` — the curated list of external skills with install commands and safety notes.

**External GitHub skills for this role (install per `skills-index/SKILLS-INDEX.md`):**
- `ui-ux-pro-max` (nextlevelbuilder/ui-ux-pro-max-skill) — searchable design intelligence: reasoning rules,
  styles, palettes, font pairings, UX guidelines by product type and stack.
  Install: `npx skills add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max`
- `impeccable` (pbakaus/impeccable) — named design commands (`polish`, `audit`, `critique`, `bolder`,
  `quieter`…) plus a deterministic anti-AI-slop detector.
  Install: `npx impeccable install`, then run `/impeccable init` in your agent.
- `frontend-design` (anthropics/skills) — forces a clear aesthetic commitment before any CSS is written.
  Install: `npx skills add https://github.com/anthropics/skills --skill frontend-design`
- `web-design-guidelines` (vercel-labs/agent-skills) — audits UI against 100+ accessibility/UX rules.
  Install: `npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines`

## 6. What To Look Up

**The 3-tier source system (priority order when sources conflict):**

- **Tier 1 — Deciding standards (beat every lower tier):**
  - The project's own design system + brand (PROJECT-PROFILE) — answers: which tokens, components, identity
    colors, icons, and logo apply here. This is the highest law inside the project.
  - WCAG 2.2 (AA level) — answers: required contrast ratios, focus visibility, target size, and whether
    information may be conveyed by color alone.
  - WCAG 3.0 is a W3C Working Draft referenced by no law — do not design or audit against it; build to WCAG 2.2 AA.
  - Nielsen Norman Group, 10 Usability Heuristics — answers: whether a flow is self-auditable for system
    status, consistency, error prevention, and recovery.
  - Apple Human Interface Guidelines — Liquid Glass era (iOS 26+, 2025) — answers: iOS/macOS platform patterns (navigation, touch areas, dynamic type). In the Liquid Glass era the glass material belongs to the control/navigation layer only, never the content layer; designs must be tested with Reduce Transparency on and at both clarity extremes (clear ↔ opaque).
  - Material 3 Expressive (2025+, Android 16 era) — answers: Android/web platform patterns: spring-physics motion, expressive shapes and type scale, dynamic color, 48dp touch targets, adaptive layout.
- **Tier 2 — Searchable design data:**
  - UI/UX Pro Max datasets — search by product type (dashboard, e-commerce, SaaS, health app…) and stack when
    you need: which layout/palette/font pairing fits this product type, and the reasoning rule behind it.
    Always cross-check lookup results against the project's DS before using them.
  - The project's own data — analytics, real user feedback, support tickets. When it exists, it outweighs
    every external lookup table.
- **Tier 3 — Inspiration only (never the sole basis for a decision):**
  - Mobbin / Page Flows / Refero / Screenlane — search when you need a complete flow from a real app
    (onboarding, checkout, paywall, settings). Learn flow structure; do not copy the brand.
  - Behance — search for full case studies (problem → process → result). Warning: presented results are
    usually polished and omit bad states.
  - Awwwards / Godly — search for peak web visuals, motion, and typography. Warning: award sites often
    sacrifice performance and accessibility.
  - Dribbble — search ONLY for visual direction, mood, and micro-detail. Static concepts have no real data,
    no edges, no errors — never use them as an interaction pattern.

**Rules for looking things up:**
- Every major decision in `03-design.md` must cite its source and which tier it belongs to. A decision based
  only on Tier 3 must be marked as a judgment call requiring the approver's confirmation.
- Platform guideline citations must carry a version/date (e.g. "iOS 26 HIG", "Material 3 Expressive, 2025") and be re-verified at each major platform release — platform design languages now change yearly, and an undated citation silently goes stale.
- When two sources conflict, apply the tier order: Tier 1 standards beat Tier 2 lookup data, Tier 2 beats
  Tier 3 inspiration — and the project's DS beats all three.
- When uncertain about a platform behavior, search the platform's own guideline (HIG / Material) for that
  exact component or pattern — not blog summaries of it.

## 7. Outputs

- **`03-design.md`** in the task folder, containing at minimum:
  1. The research table (products reviewed, what was learned, what was not copied, and why).
  2. The main design decisions, each with its source/basis cited.
  3. The board or prototype as a file that opens and can be viewed immediately (static HTML, a design file,
     or board screenshots).
  4. The 5-state notes for every screen/component.
  5. The self-audit results (heuristics + WCAG + anti-slop) and a list of anything not yet passing, with
     a plan to fix it.
- An update to the task's `STATUS.md`: Gate 3 awaiting approval / submitted.

Never submit "ideas in chat" instead of a file. The approver must be able to open the artifact without asking again.

## 8. Worked Example

Task: "Design the order list screen for an admin web app."
- Step 2: researched 3 real admin products → learned: tables use sticky filters, order statuses use semantic
  color labels, each row has one primary action plus an overflow menu.
- Step 4: layout locked: filter bar on top, table in the middle, pagination below; order detail opens in a
  side panel instead of leaving the page (preserves list context).
- Step 6: empty state = "No orders match the current filters" + a clear-filters button; error state keeps
  the selected filters and offers retry.
- Step 8: the audit caught a yellow status label with white text below AA → changed to a pale yellow
  background with dark text.

## 9. Gate Checklist

- [ ] All inputs read (spec, BA, Architect frame, PROJECT-PROFILE) and constraints recorded at the top of the file
- [ ] Research table has ≥3 real products, stating what was learned / not copied / why
- [ ] Every major design decision has a basis (source, DS, or AC) — no decision justified only by "it looks nice"
- [ ] Layout was locked before detail; every BA Acceptance Criterion has a place in the layout
- [ ] Only DS tokens/components used; every proposed DS extension recorded separately with a reason
- [ ] All 5 states covered for every screen/component
- [ ] Icons from the project's system only; no emoji icons; logo/wordmark untouched
- [ ] Self-audit complete: heuristics + WCAG AA + anti-slop; anything not passing has a fix plan
- [ ] Motion (if any) has a clear purpose and respects reduced-motion + device constraints
- [ ] The artifact opens and can be viewed immediately; `STATUS.md` updated

### Gate Test Cases (starter set — extend for each task)

These cases implement the Test-Case Gate law (`workflow/MASTER-WORKFLOW.md`): define them before working, run all of them, 100% PASS to proceed — any FAIL → stop and issue a Failure Report.

| ID | Test case | How to verify | Evidence for PASS |
|---|---|---|---|
| TC-03-01 | Research basis exists: ≥3 real, shipped products were reviewed for the pattern being designed | Inspect the research table in `03-design.md`; open each cited product and confirm it is a real shipped product of the same type/pattern | Research table with ≥3 products, every row filled: pattern learned / applied where / what was NOT copied + why |
| TC-03-02 | Every major design decision cites a source | Walk the decision list in `03-design.md`; each major decision (layout, interaction pattern, density) names a product, a DS rule, or an AC | Decision entries each carrying a cited source; zero decisions justified only by "it looks nice" |
| TC-03-03 | Every BA Acceptance Criterion has a place in the layout | Reconcile the AC list from `01-ba.md` against the layout/board, one AC at a time | AC→layout mapping with no orphan AC; any gap recorded as a question sent back to the BA |
| TC-03-04 | Only design-system tokens and components are used | Compare every color/spacing/radius/type value in the design against the DS token list, and every component against the component library | Zero off-token values; any new token/component listed separately as a proposed DS extension with a reason |
| TC-03-05 | All 5 states are designed for every in-scope screen/component | For each screen, check that default, loading, empty, error, and success are drawn or described | 5-state notes/board sections present for every screen in scope |
| TC-03-06 | Accessibility floor is met (WCAG 2.2 AA) | Measure text/background contrast for body text and status colors; check focus visibility and target sizes against the playbook's WCAG table | Contrast measurements recorded (≥ 4.5:1 normal text, ≥ 3:1 large text); self-audit results section in `03-design.md` |
| TC-03-07 | Brand integrity: icons and logo come from the project's system only | Inspect the board/prototype for emoji icons, foreign icon sets, or a redrawn logo/wordmark | Zero emoji/foreign icons; logo/wordmark used as-is, referencing the original brand asset |
| TC-03-08 | Motion and responsive behavior respect the project constraints | Check each animation for a stated purpose and reduced-motion behavior; view the design at the DS breakpoints, including narrow screens | Motion list with purpose + reduced-motion note; breakpoint check results recorded; light option noted when weak devices are in scope |

## 10. Common Failures & Anti-Patterns

| Failure | Why it breaks | Do this instead |
|---|---|---|
| Designing detail first, layout later | Each cell looks fine but the whole is a mess; must be redone | Lock layout/hierarchy first (Step 4) |
| Designing only the populated state | Real usage hits blank screens when empty or errored | All 5 states (Step 6) |
| Copying a Dribbble concept wholesale | Concepts have no edges, errors, or real data | Learn visual direction only; take patterns from real products |
| Pale "clean-looking" text | Below WCAG AA; real users cannot read it | Contrast ≥ 4.5:1 (normal text), ≥ 3:1 (large text) |
| One-off color/spacing values per screen | The DS cracks gradually and becomes unmaintainable | Tokens only; propose new ones into the DS |
| Emoji icons / mixing icon sets | Looks amateur, breaks the brand | One icon system — the project's |
| Heavy decorative motion | Slow on weak devices, distracting, hides content | Meaningful motion + reduced-motion + a light option |
| Cramming all information onto the main screen | Cognitive overload; the primary job is invisible | Hierarchy: core on the surface, detail via drill-down |

## 11. Handoff to the Next Role

**(a) Who receives your work:** The Developer (Gate 5, frontend). The approver reviews the gate first;
QA later uses your design as the visual reference when verifying the built UI.

**(b) The exact artifacts and required contents:**
- `03-design.md` containing all 5 items listed in section 7 (research table, decisions with sources,
  viewable board/prototype, 5-state notes, self-audit results).
- The board/prototype files themselves, in a form that opens immediately.
- `STATUS.md` updated to show Gate 3 submitted.

**(c) Your handoff checklist (complete before passing):**
- [ ] Every screen in scope appears in the board/prototype AND in the 5-state notes
- [ ] Every BA Acceptance Criterion maps to a visible place in the layout (no orphan AC)
- [ ] All tokens/components referenced actually exist in the DS, or are listed as proposed DS extensions
- [ ] Open items are marked [TBC] in the file, not left as silent gaps
- [ ] Self-audit results are recorded, including the items that do NOT pass

**(d) Acceptance criteria the receiving role will check (what gets your work sent back):**
- The Developer will send it back if: a state is missing for any screen; a component or token is referenced
  that does not exist and is not flagged as a proposal; an AC has no home in the layout; or the board/prototype
  cannot be opened.
- The approver will reject the gate if: there is no research table, a decision has no cited basis, or the
  design breaks the project's brand/DS without an approved exception.

**(e) Handling a rejection / rework loop:**
- Fix within the scope of the decisions recorded in `03-design.md`; update the file itself — design answers
  are never settled verbally in chat.
- If the feedback demands a business-flow change → route it to the BA. If it demands breaking the
  architecture frame → route it to the Architect. Never exceed your own authority to satisfy feedback.
- After rework, re-run the affected part of the self-audit and note what changed in the file.

## 12. References

- `references/playbook.md` — the deep UI/UX playbook (the 3-tier source system, the 5-state spec, the WCAG
  table, the research method, the audit checklist, the anti-AI-slop list).
- `references/ai-feature-ux.md` — read whenever the feature being designed CONTAINS AI (chat, generation, recommendations, copilots): the AI UX pattern checklist, autonomy tiers, the AI component states, and AI disclosure as a design deliverable.
- `references/design-systems.md` — read when creating, extending, or auditing a design system: token architecture, typography/spacing systems, the 12-part component spec, theming & dark mode, icon construction, motion tokens, design-to-code handoff, and design QA tolerances.
- `templates/` in this repo — the SPEC/BA templates that define your inputs; the `03-design.md` output
  follows the structure in section 7.
- `skills-index/SKILLS-INDEX.md` — the curated external skills with install commands and safety warnings.
