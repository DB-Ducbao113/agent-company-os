# Domain Modeling Deep Dive — Data, Rules, Processes, States

> Companion to `references/playbook.md` (INVEST, the G/W/T pattern library, state-model basics, MoSCoW).
> This file goes deeper: the four models a BA maintains (data, rules, process, state) and how to keep them
> mutually consistent — plus prioritization beyond MoSCoW and a rubric for acceptance-criteria quality.

## 1. The data dictionary

Stories talk about "the customer" and "the order"; systems store fields. The data dictionary is where the BA pins down every business-significant field **before** the Architect designs tables — it records business meaning, not storage types.

One row per field:

| Column | What to write | Example |
|---|---|---|
| Field | business name, from the glossary | `order.total` |
| Meaning | one sentence, no synonyms | "Amount the customer must pay, including tax, excluding delivery." |
| Type (business) | money / count / text / date-time / enum / flag — not SQL types | money |
| Source of truth | who or what system creates it and may change it | computed by the pricing rule BR-07; never typed by a user |
| Validation | format, range, required-when | > 0; required once the order is PLACED |
| Lifecycle | created when, changes when, retired/archived when | created at checkout; frozen after PAID; kept 7 years |
| Sensitivity | public / internal / personal / financial / secret | financial |

Working rules:
- **One field, one meaning.** If two screens use "status" differently, they are two fields — name them apart (`order.status`, `payment.status`) before the confusion reaches a database.
- **Derived fields name their rule.** Anything computed cites the business rule that computes it; if no rule exists yet, writing the dictionary just exposed a missing rule — log it.
- **"Source of truth" settles arguments.** When two systems disagree about a value, the dictionary already says which one wins; integration defects often trace to a field whose source of truth was never declared.
- Fields nobody can fill in (no source, no owner) are deleted from scope, not carried as decoration.

## 2. Business-rule catalogs and decision tables

Keep rules in one catalog, numbered BR-xx, each with: statement (one sentence, testable), source (who/what document decreed it), applies-to (stories/fields), and exceptions. When a rule's outcome depends on **combinations** of conditions, prose hides gaps — switch to a decision table.

**Worked decision table** — rule: "What discount applies to an order?" Conditions: member tier (Gold / Silver / none), order value (≥ 500 / < 500), coupon present (Y/N). Actions: discount %.

| Rule | Tier | Value ≥ 500 | Coupon | Discount | Note |
|---|---|---|---|---|---|
| R1 | Gold | Y | Y | 15% | coupon does not stack beyond cap |
| R2 | Gold | Y | N | 10% | |
| R3 | Gold | N | Y | 10% | |
| R4 | Gold | N | N | 5% | |
| R5 | Silver | Y | Y | 10% | |
| R6 | Silver | Y | N | 5% | |
| R7 | Silver | N | Y | 5% | |
| R8 | Silver | N | N | 0% | |
| R9 | none | Y | Y | 5% | coupon only |
| R10 | none | Y | N | 0% | |
| R11 | none | N | Y | 5% | coupon only |
| R12 | none | N | N | 0% | |

How the table earns its keep:
- **Completeness is checkable:** 3 conditions → 3×2×2 = 12 combinations; 12 rows present. A missing row is a question nobody asked (what *should* a non-member with a coupon and a small order get? — R11 forced that answer into existence).
- **Contradictions are visible:** two rows with identical conditions but different actions cannot hide in a table the way they hide in paragraphs.
- **QA converts rows to test cases 1:1** — each row is one case with the row's values as test data. If a row cannot be tested, the rule is not finished.
- Collapse rows only when the differing condition provably never changes the action, and note the collapse ("tier Silver/none behave identically when value < 500 and no coupon → merged").

## 3. Process modeling in text

Diagrams are optional; an unambiguous text process is not. Model per process:
- **Trigger** (what starts it), **actors** (roles, from the glossary), **precondition** (what must already be true), **happy path** (numbered steps), **exception flows** (numbered E1, E2… attached to the step they branch from), **end states** (success and each failure end), **postconditions**.

Use swimlane-by-actor notation in plain text — one block per actor, steps in order, handoffs marked:

```
[Customer]  1. Submits checkout → hands order to [System]
[System]    2. Validates stock. E1: item out of stock → notify [Customer], remove item, back to step 1.
[System]    3. Reserves stock (15 min) → requests payment from [Payment provider]
[Provider]  4. Confirms or declines. E2: declined → [System] releases reservation, notifies [Customer]; end: FAILED.
[System]    5. Marks order PLACED → notifies [Warehouse]
[Warehouse] 6. Picks and packs → marks READY; end: FULFILLED-ready.
```

Rules: every exception flow states where it **resumes** or that it **ends** the process; every handoff names the information that crosses (not "sends the data" — which fields, per the data dictionary); any step an actor performs "in their head" (judgment, approval) names its criteria or cites the decision table it uses. A process step nobody owns is a defect in the model, not a detail.

## 4. State machines — advanced

Beyond the basics in the playbook (states, events, allowed transitions), model these four things:
- **Guards** — conditions on a transition beyond the event: `PLACED → PAID [payment confirmed AND amount = order.total]`. A transition without its guard written is an argument waiting to happen between BA, Dev, and QA.
- **Entry/exit actions** — what must happen on entering or leaving a state: entering PAID → "issue invoice, notify warehouse"; leaving RESERVED by timeout → "release stock". Actions belong to the state, not to whichever transition happened to trigger them.
- **Terminal vs. resting states** — mark which states are final (nothing leaves) and which are resting (work pauses but can resume). Reports and timeouts treat them differently.
- **Forbidden transitions as tests** — the playbook's cross-check becomes a test list: for every state pair NOT in the table, QA gets one negative case ("from CANCELLED, event pay → rejected, state unchanged"). The forbidden list is usually longer than the allowed list, and it is where data-corruption bugs live.

Also decide explicitly: can an object be in this lifecycle twice (re-opened orders)? Is history preserved (audit of transitions with actor + timestamp) — if any stakeholder will ever ask "who cancelled this and when", the answer is yes, and it belongs in the requirements now, not as a later patch.

## 5. Prioritization — beyond MoSCoW

**MoSCoW failure modes** (watch for all four):
- *Must inflation:* everything is Must because nobody wants to say no. Counter: cap Must at ~60% of estimated capacity; force-rank within Must — the bottom Must is the first Won't if estimates grow.
- *Won't amnesia:* Won'ts are forgotten and creep back as "quick favors". Counter: Won'ts are listed in the spec's Out of Scope with reasons, and re-adding one requires a new routing decision.
- *Should/Could blur:* the two middle buckets merge into "later, maybe". Counter: every Should names the cost of deferring it; a Should with no deferral cost is a Could.
- *Static buckets:* priorities never revisited after new information. Counter: re-run MoSCoW at every scope change, and record what moved and why.

**Kano basics** — classify each feature by asking how users feel with it vs. without it: **Basic** (absence angers, presence unnoticed — correctness, security), **Performance** (more is linearly better — speed, capacity), **Delighter** (presence pleases, absence unnoticed — the thoughtful extra), **Indifferent**, **Reverse** (some users actively dislike it). Use Kano to protect Basics from being traded away for Delighters in a crunch — the classic prioritization error.

**WSJF (Weighted Shortest Job First)** — for sequencing within a release: `WSJF = Cost of Delay ÷ Job Size`. Cost of Delay ≈ user/business value + time criticality + risk reduction, each scored 1–10 (Fibonacci-ish scales are fine; the discipline matters more than precision).

Worked example (size in rough days):
| Item | Value | Time crit. | Risk red. | CoD | Size | WSJF | Order |
|---|---|---|---|---|---|---|---|
| Fix double-charge bug | 10 | 10 | 8 | 28 | 2 | **14.0** | 1 |
| Add coupon support | 8 | 5 | 2 | 15 | 5 | 3.0 | 3 |
| New onboarding flow | 6 | 3 | 3 | 12 | 3 | 4.0 | 2 |
| Admin export | 4 | 2 | 1 | 7 | 4 | 1.75 | 4 |

The small, urgent, risk-reducing fix wins by a wide margin; the big feature waits despite its higher raw value. Show the arithmetic in the artifact — a ranking without visible scores is an opinion, and stakeholders will treat it as one.

## 6. Acceptance-criteria quality rubric

Score every AC 0–2 on five dimensions (0 = absent/wrong, 1 = partial, 2 = solid). An AC scoring < 8/10 goes back for rework before the gate passes; the pattern library in the playbook supplies the shapes, this rubric supplies the standard.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| **Observable** | describes internals or intentions ("system processes quickly") | partly observable | an outsider can watch it happen or measure it |
| **Unambiguous** | two readers build two different things | one term undefined | every term from the glossary/data dictionary; one reading only |
| **Valued outcome** | checks mechanics only ("button exists") | outcome implied | the Then states the business-visible result |
| **Bounded** | no quantities, limits, or edge stated | some numbers present | thresholds/boundaries explicit (amounts, times, counts) |
| **Independently testable** | needs another AC or production data to check | testable with setup help | QA can execute it as written, with stated data |

**Scored example — bad AC, rewritten step by step.**
Original: *"Given a user checks out, when they pay, then the order is processed fast and correctly."*
Scores: Observable 0 ("processed" is internal), Unambiguous 0 ("fast", "correctly" undefined), Valued outcome 1, Bounded 0, Testable 0 → **1/10**.
Step 1 — make it observable + bounded: *"…then the order reaches status PLACED within 5 seconds of payment confirmation."* (Observable 2, Bounded 2.)
Step 2 — remove ambiguity by citing rules: *"…and the charged amount equals order.total as defined by BR-07."* (Unambiguous 2.)
Step 3 — state the valued outcome + the error sibling AC: *"…the customer sees the confirmation screen with the order number"* plus a paired AC: *"Given payment is declined, when the provider responds, then the order stays CART, stock reservation is released, and the customer sees the decline reason."* Final: **10/10**, and QA can execute both as written.

**Second scored example.** *"Given an admin, when they view the list, then all records are shown."* — Unambiguous 0 ("all" vs. pagination unanswered), Bounded 0. Rewrite forces the missing decision into the open: *"…then the list shows 25 records per page, newest first, with total count and page controls"* — if the stakeholder actually meant "all on one page", the rewrite surfaces the disagreement now, at BA cost, instead of at QA cost.

## 7. Quantities, money, and time — the silent-defect fields

More production defects come from unmodeled quantities than from wrong flows. For every numeric or temporal concept in scope, the dictionary or its rule must state:
- **Unit and currency** — "amount" is not a field; "amount in VND, minor units, tax-inclusive" is. Mixed-unit interfaces are a named integration risk.
- **Rounding rule and where it applies** — per line item or per total; half-up, bankers', or truncate; who decided. Two components rounding differently produce the classic one-cent mismatch that no test with round numbers will catch — QA test data must include a rounding-boundary case (e.g. values ending in .005 of the minor unit).
- **Precision and range** — maximum value the business will ever present; counts that can be zero; quantities that can be negative (refunds, adjustments) vs. those that cannot.
- **Time semantics** — every timestamp names its zone basis (stored UTC, displayed in whose zone?), every duration names its endpoints ("within 4 hours" — from creation, from confirmation, or from payment?), and every "day" states whether it means calendar day, business day, or rolling 24 hours. Deadline rules get a worked example at the boundary: an order placed at 23:30 with a "cancel within 1 day" rule — show the exact last valid moment.
- **Ordering and ties** — any "first", "latest", or "top N" rule states its tie-breaker; unspecified tie-breakers become nondeterministic behavior in production.

## 8. Cross-model consistency checks (run before the gate passes)

The four models (dictionary, rules, process, states) must agree with each other, not just be individually plausible. Run this checklist over `01-ba.md` at gate time; every "no" is a defect in the artifact:

| Check | How |
|---|---|
| Every field used in a rule exists in the dictionary | grep the rule catalog's field names against dictionary rows |
| Every computed field cites its rule; every rule's inputs exist | follow each "computed by BR-xx" both directions |
| Every process step's handoff data exists in the dictionary | check each "hands X to Y" against field rows |
| Every state in the process model matches the state machine | process end states ⊆ machine states; no orphan states either way |
| Every guard references a dictionary field or a rule | guards citing undefined terms are rework |
| Every decision-table combination is reachable in the process | a rule row whose conditions the process can never produce is dead scope — flag it |
| Every AC traces to a story, a rule, or a state transition | orphan ACs are invented scope; missing coverage is a gap |
| Permission matrix agrees with process actors | an actor performing a step they are not permitted to perform is a contradiction, not a detail |

Record the check run (date, result per row) at the end of `01-ba.md`. This table is also the fastest way for the Architect and QA to audit the BA artifact during their handoff acceptance — eight checks, each answerable in minutes.
