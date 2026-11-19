# Playbook — Orchestrator / Intake (deep reference)

> This document holds the material too long for `SKILL.md`: the scoring rubric, the question bank, the EARS pattern table, and worked routing examples.
> SKILL.md is the law; this file is the field manual you consult while executing it.

## 1. Ambiguity Scoring Rubric — 8 Dimensions

Score each dimension: **0 = Clear** (documented, or answered with certainty), **1 = Vague** (mentioned but interpretable in several ways), **2 = Unknown** (no information at all).

| # | Dimension | 0 — Clear | 1 — Vague | 2 — Unknown |
|---|---|---|---|---|
| 1 | Goal | The problem + desired outcome can be stated in one sentence | "Make it better / prettier / faster" | Only a feature name, no reason given |
| 2 | User | The user groups and their roles can be named | A generic "users" | Nobody knows who uses it or who is affected |
| 3 | Scope | The screens/modules/flows in scope can be listed | Scope stated verbally, boundaries unclear | No idea where it starts or ends |
| 4 | Expected behavior | The system's behavior in the main situations is described | Only the happy path is described | No concrete behavior described at all |
| 5 | Constraints | Stack/brand/deadline/prohibitions are documented | Constraints exist but their current validity is unconfirmed | No known constraints |
| 6 | Success criteria | Measurable, with numbers or a checking method | "Done means it works" | No criteria at all |
| 7 | Reference examples | A link/screenshot/example product + the specific points to learn from | "Make it like app X" without saying which part | No example, no anti-example |
| 8 | Out of scope | Things that definitely will not be done can be named | Partially inferable | Never discussed |

**Reading the result:** 0–3 → ask quickly. 4–9 → ask fully. 10–16 → ask fully + offer concrete options + consider splitting the task.
**Note:** a single dimension scoring 2 in a *blocking* group (Scope, Goal, or a constraint touching money/permissions/data) is handled as if the total were high, regardless of the total.

## 2. Question Bank by 6 Groups

Pick the 0–2 questions per group that best fit the dimensions that are actually vague. Do not mechanically ask every question.

### 2.1 WHY — the real problem (5 Whys technique + JTBD)
- What specific problem is happening, who suffers from it, and how?
- Why does it need solving *now* (what event triggered it)?
- If nothing is done for the next month, what happens?
- What "job" does this help the user get done (job-to-be-done) that they currently do manually or via another product?
- Is this a symptom or a cause? (Repeat "why" up to 5 times; stop when you reach a real decision/policy/limitation.)

### 2.2 WHO / WHERE — users & context
- Who is the primary user? Are there secondary groups (admins, support staff, guests)?
- Do they use it on web / mobile / both? What is their most common device?
- Which screen does the flow start from, and where does it end? Does it change any existing flow?
- Who approves the final result?

### 2.3 WHAT / NOT-WHAT — scope
- Is this a new feature, a modification of an existing feature, or a full replacement?
- List the 3–5 work items that definitely belong to this round.
- What looks related but is *definitely not* part of this round?
- Existing data (if any): keep as-is / migrate / delete?
- Is multi-language, multi-timezone, or multi-level permission support needed — or is that a later phase?

### 2.4 EXAMPLES / ANTI-EXAMPLES
- Is there a product/screen to learn from? Which specific point should be learned (layout, speed, presentation style)?
- Is there a style that must absolutely be avoided (too cluttered, too flashy, too similar to competitor X…)?
- Desired creative freedom: follow the example closely / use it as reference / propose freely?

### 2.5 CONSTRAINTS
- What must stay unchanged (brand, logo, data structures, APIs that others already depend on)?
- Is the deadline real, and what happens if it slips?
- Do end users run low-end devices / slow networks (which decides how much optimization is mandatory)?
- Are there legal/compliance requirements (personal data, payments, record retention)?

### 2.6 SUCCESS
- What does "done" look like when you are satisfied? Name 1–3 observable signs.
- Are there target numbers (load time, flow completion rate, acceptable error count)?
- How will you check it: view a build, click through a prototype, read a test report?
- What happens if the result is technically correct but you "don't like the feel" of it — can that subjective criterion be described in advance?

## 3. EARS Pattern Table (Easy Approach to Requirements Syntax)

| Pattern | Syntax | When to use it | Example (generic) |
|---|---|---|---|
| Ubiquitous | THE SYSTEM SHALL [behavior] | A rule that is always true, independent of events | THE SYSTEM SHALL display prices inclusive of tax on every screen that shows a price |
| Event-driven | WHEN [event] THEN THE SYSTEM SHALL [behavior] | A reaction to an action/event | WHEN the user clicks "Place order" THEN THE SYSTEM SHALL create the order in AWAITING PAYMENT status |
| State-driven | WHILE [state] THE SYSTEM SHALL [behavior] | Behavior that depends on the current state | WHILE an order is in CANCELLED status THE SYSTEM SHALL disable the pay button |
| Unwanted behavior | IF [bad condition] THEN THE SYSTEM SHALL [response] | Errors, refusals, expirations, bad data | IF the login session has expired THEN THE SYSTEM SHALL return to the login screen and preserve the content the user was typing |
| Optional | WHEN [an optional feature is enabled] THEN… | Behavior that exists only when a configuration/feature is on | WHEN the store enables international sales THEN THE SYSTEM SHALL display foreign-currency options |

EARS writing rules: 1 sentence = 1 testable behavior; the subject is THE SYSTEM; avoid unmeasurable words ("fast", "friendly", "reasonable") — replace them with a number or an observable condition; every main flow must have at least one Unwanted-behavior sentence.

## 4. Worked Routing Examples

### Example A — "Redesign the homepage UI"
12-question tree: 1=No (no business-logic change) · 2=Yes (must comply with the existing design system → Frontend Architect goes first and locks the frame) · 3=Yes (UI/UX) · 4=No · 5=No · 6=No (public homepage, no personal data) · 7=No (APIs unchanged) · 8=Yes (QA) · 9=Yes (Release) · 10=No · 11=No · 12=Yes (research + prototype approval before production).
→ **Route:** Frontend Architect → UI/UX → Frontend Dev → QA → Release. BA is condensed into the spec. Security/Integration are skipped with the reasons recorded.

### Example B — "Add social-account login"
12-question tree: 1=Light yes (the account-linking rule when emails collide — BA settles it) · 2=Yes (the auth flow is structural) · 3=Yes · 4=Yes · 5=Yes (identity-linking table) · 6=**Yes — Security mandatory** (auth + personal data) · 7=Yes (third-party identity provider → Integration) · 8=Yes · 9=Yes.
→ **Route:** BA → Architect → Security (in parallel at the end of Architect) → UI/UX → Dev → Integration → QA (including the security tests handed over by Security) → Release.

### Example C — "Fix a bug: clicking Save twice creates two records"
Bugfix branch (question 10): QA reproduces and writes the failing test case first → Dev fixes (idempotency on the save action/behavior) → QA regression. The Architect joins only if the root cause is an API design missing an idempotency key (questions 2/4 = conditionally yes). BA/UI/UX/Security are skipped with reasons recorded.
→ **Route:** QA (reproduction) → Dev → QA (regression) → shortened Release.

### Example D — "Update the pricing table on the marketing page"
Question 11 = Yes (content/data only): **fast lane** — Dev/content update → QA cross-checks every number against the official source the user designates. No BA/Arch/UI/UX. Cross-check evidence is still mandatory, because wrong figures are the hardest errors to spot.

## 5. Edge Cases When Asking Questions

- **The user answers a choice question with one word ("yeah", "ok"):** treat it as agreement with the proposed default you stated, and record exactly that in Clarifications ("agreed to default B via an 'ok' reply on …"). Do not infer anything beyond the published default.
- **The user changes an answer between rounds:** the later answer wins; record both in Clarifications with the earlier one marked "superseded", so it stays traceable why the spec changed.
- **The user is a group (several requesters with differing opinions):** ask who the final decider is; record the minority opinion in the spec's "Recorded disagreements" section instead of deleting it.
- **The request arrives relayed from a third party (the user's customer…):** clarify who the real decision source is; the playback must be confirmed by that source or by their authorized delegate.
- **A task repeats one that was previously STOPPED:** read the old STOP reason first; ask what has changed to make this time different — avoid re-running the exact direction that was stopped.
- **The user asks to "go fast, skip the process" for work touching money/permissions:** the fast lane does not apply to question 6 of the decision tree; state the risk in one sentence and keep Security + QA, shortening the remaining teams instead of those two.

## 6. Long-Input Decomposition — Method and Micro-Example

**Segmentation rules:** one segment = one demand. Split compound sentences at "and/but/also/then" whenever each part could be verified separately. Keep prohibitions ("do not", "never", "only") as their own segments — they are the most commonly dropped items and the most expensive to lose.

**Typing rules:** a segment is a *requirement* if it demands behavior; a *constraint* if it limits how; a *preference* if it guides taste with room to vary; *clarify* if two reasonable readers would implement it differently; *conflict* if it contradicts another segment or the PROJECT-PROFILE.

**Micro-example.** Input: "Add a discount code at checkout. Codes have an expiry date and a max number of uses; expired codes show a clear message. Do NOT stack two codes. Keep the current checkout layout, just add a small input field. Must work on slow phones."
Segments: S-01 discount code at checkout (requirement) · S-02 expiry date (requirement) · S-03 max uses (requirement) · S-04 expired → clear message (requirement) · S-05 no stacking (constraint/prohibition) · S-06 keep layout, small field only (constraint) · S-07 works on slow phones (non-functional requirement).
A summary-style intake would likely keep S-01/S-02 and lose S-05 and S-07 — exactly the failures this protocol exists to prevent. Coverage line in the spec: "Segments: 7 · Mapped: 7 · Unmapped: 0".
