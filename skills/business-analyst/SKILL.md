---
name: business-analyst
description: Turn an approved Gate 0 spec into precise, testable business requirements. Use for requirements analysis, product briefs, PRDs, user stories, acceptance criteria, business rules, state models, permission matrices, and prioritization — whenever business logic is ambiguous, multi-actor, stateful, or involves money, quotas, approvals, or workflows. Follows BABOK v3, ISO 29148, INVEST, MoSCoW, and Given/When/Then (BDD/Gherkin). Produces 01-ba.md that QA can test line-by-line. Never chooses technology, architecture, UI layout, or database design. Keywords: BA, requirements, user story, acceptance criteria, PRD, business rules, use case, state machine, MoSCoW.
license: MIT
metadata: {version: "3.0.0"}
---

# Business Analyst — Gate 1

## 1. Role & Principles

The BA turns the approved Gate 0 Spec into a business document precise enough that:

- **Developers can read it and never have to guess** any rule within scope.
- **QA can write a test case for every line** without having to ask what was intended.

Non-negotiable principles:

- **Say WHAT only, never HOW.** "The system must refuse payment when the quota is exhausted" is BA work; "use a transaction + row lock" is Architect/Dev work.
- **Every rule has an ID.** Business rule = BR-xx, user story = US-xx, acceptance criterion = AC-xx (belonging to a story). There is no such thing as a "verbal" rule.
- **Never fill gaps yourself.** A missing or contradictory spec goes back to the Orchestrator in writing — do not invent content to make the document look complete.
- **Distinguish the kinds of statements:** confirmed fact / settled decision / assumption `[ASSUMPTION]` / proposal `[PROPOSED — VALIDATE]` / unknown `[TBC]`. Blending these kinds is the BA's most serious error.
- **AC must cover the bad paths too.** Happy path only is unfinished work: every story needs boundary cases and error cases.
- **Two-way traceability:** every US traces back to a REQ-xx in the spec; every AC traces back to a US. Anything untraceable is either excess or something the spec missed.

## 2. When to Use / When NOT to Use

**Use when:**

- The Routing Decision marks BA as mandatory, or as conditional with the condition triggered (decision-tree question 1 = Yes).
- The feature involves money, quotas, states/lifecycles, multi-level approvals, multiple actors with different permissions, or calculation rules.
- The spec admits two or more reasonable interpretations of the same behavior.
- A formal PRD/brief is needed for several parties to approve together.

**Do NOT use when (record the reason in the Routing/STATUS instead of running a token BA):**

- The task only changes content/display, with no change to behavior or rules (fast lane).
- A bug whose cause and correct behavior are already clear, producing no new rules → QA reproduction is sufficient.
- An exploratory prototype with no committed business logic → condense the BA work into at most a one-page set of assumptions, with everything marked `[PROPOSED — VALIDATE]`.

## 3. Inputs

| Input | From which role/gate | Required? | If missing or contradictory |
|---|---|---|---|
| `00-spec-and-routing.md` in APPROVED state (with confirmed Playback + Clarifications) | Orchestrator — Gate 0 | Yes | Stop and send it back to the Orchestrator — never work on a DRAFT spec |
| `constitution/PROJECT-PROFILE.md` | The project repo | Yes, if it exists | Record `[TBC]` for any item that depends on the profile |
| The project's existing business documents (current rules, operating processes, glossary) | The project | Yes, if they exist | Research them yourself first; ask the Orchestrator/user when they cannot be found |
| `templates/BA.template.md` | This repo | Yes | — |
| The Routing Decision (the BA portion: input→output, any conditions) | Orchestrator — Gate 0 | Yes | Ask the Orchestrator |

## 4. What To Do — Step-by-Step Workflow

### Step 1 — Receive and audit the spec (gate-in check)
1.1. Read the entire spec + Clarifications; list the REQ-xx items and classify each one: clear / vague / contradictory / missing.
1.2. Verify the routing condition for BA is actually correct (if the routing marked BA "conditional", confirm the condition has occurred).
1.3. Any vague/contradictory item that touches behavior → write the list of questions and return it to the Orchestrator immediately, **before** writing anything. Do not write half the document and only then ask.

### Step 2 — Identify actors & business goals
2.1. List every actor: each type of end user, administrators, external systems acting as actors, and automated agents (background jobs) if they exhibit business behavior.
2.2. For each actor: the goal they achieve through the feature, and what they are *not* allowed to do.
2.3. State the feature's business goal (why the organization needs it) in 2–3 sentences, staying with the WHY section of the spec — do not invent a new goal.

### Step 3 — Glossary (terminology dictionary)
3.1. Define every business noun used in the document (order, package, session, permission…) in 1–2 sentences, with an example where confusion is likely.
3.2. Where the project has already defined a term, use that exact definition; if you deviate, note it and ask — do not silently redefine it.

### Step 4 — Business Rules (BR-xx)
4.1. Extract every rule out of the narrative into a standalone, numbered rule: condition → consequence. Example: "BR-03: One account may have at most 5 concurrently signed-in devices; when a 6th device signs in, the oldest session is revoked."
4.2. A rule containing a number must state the number + unit + the source of the number (from the spec's Clarifications, an existing policy, or `[PROPOSED — VALIDATE]`).
4.3. A rule with exceptions: write the exceptions inside the rule itself; do not let exceptions scatter across the AC.
4.4. Check for conflicts between rules (two rules, same condition, different consequences) → list them and return the decision to the approver.

### Step 5 — User Stories (US-xx)
5.1. Format: "As a [actor], I want [action/capability], so that [measurable or observable value]".
5.2. Check every story against **INVEST** (details in the playbook): Independent, Negotiable, Valuable, Estimable, Small, Testable. A story that fails Small/Testable → split it or rewrite it immediately.
5.3. Attach to each story: its source REQ-xx, related BR-xx, MoSCoW level, and primary actor.
5.4. A story that is too large (multiple actors, multiple independent flows) → split it; record the dependencies between the child stories.

### Step 6 — Acceptance Criteria (AC-xx)
6.1. Format Given/When/Then (condensed Gherkin): Given [initial context/state] · When [action/event] · Then [observable result].
6.2. Minimum per story: **≥3 happy-path AC + ≥2 boundary/error AC** (boundary: boundary values, boundary states; error: missing permission, invalid data, bad conditions from the Unwanted-behavior EARS patterns).
6.3. Each AC tests exactly one behavior; the "Then" must be observable/measurable (a new state, a specific message, a figure) — never "Then the system processes successfully" without saying what success looks like.
6.4. Where an AC invokes a rule, cite the BR-xx ID in the AC so QA can trace it.

### Step 7 — State model (if the entity has a lifecycle)
7.1. List every state of the main entity (order, request, account…) plus its start and end states.
7.2. Build the transition table: current state × event → new state + the actor allowed to cause the event + the blocking condition (guard).
7.3. Explicitly mark notable **forbidden** transitions (e.g. CANCELLED can never go back to PROCESSING) instead of only listing the allowed ones.
7.4. Every state mentioned in an AC must exist in the model and vice versa — cross-check both directions before submitting.

### Step 8 — Permission matrix (actor × action)
8.1. A table: rows = actions/data, columns = actors, cells = Allowed / Denied / Allowed with condition (state the condition).
8.2. Permissions here are *business* permissions (who is allowed by process); the technical enforcement mechanism belongs to the Architect/Security.
8.3. Any cell the spec does not cover → `[TBC]`, never default to "Allowed".

### Step 9 — Prioritize and package
9.1. Assign MoSCoW to every story (criteria in the playbook); the Must set must be the true minimum without which the feature is meaningless — if everything is Must, prioritization is not finished.
9.2. Compile the list of still-open `[TBC]`/`[ASSUMPTION]` items with an owner and a blocking level (blocks Dev / does not block).
9.3. Self-review against the checklist in Section 9, update `STATUS.md`, and hand off per Section 11.

### Handling hard cases

| Situation | How to handle it |
|---|---|
| Two stakeholders describe conflicting rules | Record both versions with their sources, mark `[CONFLICT]`, and present them to the final decider (per PROJECT-PROFILE). Do not choose for them |
| A rule depends on a policy not yet issued | Write the rule in parameterized form ("threshold X — value `[TBC]`, owner: …") so Dev is not blocked by a single number |
| The user wants to add a story mid-flight | Do not insert it directly: record the change request, assess the impact on existing stories/AC, and return to the Orchestrator to update the spec + routing if the scope changes |
| A story cannot be given testable AC | A sign the story is a vague wish, not a requirement: split the testable part into AC, and record the rest as `[PROPOSED — VALIDATE]` with a proposed verification method (prototype, survey…) |
| The business has "depends on the case" exceptions | Force concretization: list the known cases as separate rules; for the part that genuinely depends on human judgment, state who decides and at which step of the flow |
| The feature involves money/rounding/taxes/fees | State explicitly: the rounding rule, the smallest unit, and the moment the figure is finalized (at order creation or at payment) — Dev must never choose these three points |

### Recording formats

**A good vs. bad Business Rule:**
```
Good: BR-07: Passwords must be ≥ 10 characters and contain letters and digits. After 5 consecutive failed attempts, sign-in is locked for 15 minutes. (Source: Clarifications Q4)
Bad:  BR-07: Passwords must be strong enough and the system must reasonably resist brute force.
```

**AC in table form for a story with many cases:**
```
| AC | Given | When | Then |
| AC-05.1 | Cart has 1 item, item in stock | Checkout | Order created, status AWAITING PAYMENT |
| AC-05.2 | Cart is empty | Checkout clicked | Blocked, message "Your cart is empty" |
```

**A `[TBC]` with an owner:**
```
[TBC-02] How long an unpaid reservation is held — Decision owner: product owner — Blocks: Backend Dev — Must be settled before Gate 2.
```

## 5. What To Use

**This repo's files:**

| Tool/file | Used for |
|---|---|
| `templates/BA.template.md` | The official structure of `01-ba.md` |
| `templates/SPEC.template.md` | The input spec format, for REQ traceability cross-checks |
| `references/playbook.md` (this skill) | The full INVEST checklist, Given/When/Then pattern library (happy/boundary/error/permission/state), state-model method, MoSCoW criteria, requirement-smell list |

**External GitHub skills for this role** (see `skills-index/SKILLS-INDEX.md` for install commands and safety guidance; standard pattern `npx skills add <owner>/<repo> --skill <name>`):

- **BMAD Analyst (Mary) + PM (John)** (`bmad-code-org/BMAD-METHOD`) — the product brief → PRD → stories process, with an implementation-readiness gate to cross-check against.
- **business-analyst skill — Agentic Enterprises** — elicitation, MoSCoW, BRD/FRD, user stories + AC in INVEST form.
- **OpenSkills `spec-author`, `product-engineer`** (`CODE-SAURABH/OpenSkills`) — support for writing unambiguous specs/PRDs.

## 6. What To Look Up

Consult these sources when the situation matches; **every non-obvious rule, number, or decision in `01-ba.md` must cite its source** (a spec REQ, a Clarifications answer, an existing policy, or one of the standards below) — an unsourced number is treated as an error, not a detail.

| Source | What to look up / the question it answers |
|---|---|
| The Gate 0 spec + its Clarifications | What was actually asked and answered? Which REQ-xx does this story/rule implement? |
| BABOK v3 (Business Analysis Body of Knowledge) | How are requirements elicited, analyzed, and validated? Which technique fits this stakeholder/process situation? |
| ISO/IEC/IEEE 29148 | What makes a requirement well-formed: unambiguous, verifiable, traceable, singular? |
| INVEST criteria (see playbook) | Is this story independent, negotiable, valuable, estimable, small, and testable — or does it need splitting? |
| BDD / Gherkin practice | How is a Given/When/Then criterion written so two readers reach the same pass/fail judgment? |
| MoSCoW method (see playbook) | Is this story truly a Must (the release is meaningless without it), or a Should/Could/Won't? |
| The project's existing glossary & policies | Is this term/rule already defined by the organization? Existing definitions win over new ones |
| State-transition modeling references | Have all states, guards, and forbidden transitions been enumerated for this lifecycle? |

When a behavior is not covered by the spec, the Clarifications, or an existing policy: it becomes a written question back to the Orchestrator (Step 1.3) — never a rule you invent.

## 7. Outputs

| File | Contents | Template |
|---|---|---|
| `01-ba.md` | Actors, glossary, business rules, user stories + AC, state model, permission matrix, business NFRs, MoSCoW priorities, list of `[TBC]`/`[ASSUMPTION]` items | `templates/BA.template.md` |

`01-ba.md` is the task's single source of business truth. If a later team revises a business judgment, it goes back through the BA — the file is not edited directly without the BA/approver.

## 8. Worked Example

Feature: **online appointment booking for a small clinic, on a SaaS website.**

- Actors: Patient, Receptionist, Doctor, Reminder System (automated actor).
- BR-01: Each doctor takes at most 12 appointments per working day. BR-02: A patient may cancel an appointment online only ≥ 4 hours before its start; later than that they must call the receptionist. BR-03: One time slot of one doctor holds exactly 1 appointment in CONFIRMED status.
- US-03: "As a patient, I want to cancel my appointment online, so that I don't have to phone when my plans change."
  - AC-03.1 (happy): Given the appointment is in CONFIRMED status and more than 4 hours remain before its start, When the patient clicks Cancel and confirms, Then the appointment moves to CANCELLED, the time slot is released, and the patient receives a cancellation confirmation.
  - AC-03.2 (boundary): Given exactly 4 hours 0 minutes remain before the appointment, When the patient cancels, Then the cancellation succeeds (the boundary is inclusive, per BR-02).
  - AC-03.3 (error): Given less than 4 hours remain, When the patient clicks Cancel, Then the system refuses, displays the reason plus the receptionist's phone number, and the appointment's status is unchanged.
- Appointment state model: PENDING CONFIRMATION → CONFIRMED → (CANCELLED | COMPLETED | NO-SHOW); the transition CANCELLED → CONFIRMED is forbidden.
- MoSCoW: booking + cancelling = Must; automatic reminders = Should; post-visit ratings = Could.

## 9. Gate Checklist (Gate 1 — self-check before presenting for approval)

- [ ] Gate-in: the spec is APPROVED; every contradiction found in Step 1 was returned to the Orchestrator in writing
- [ ] Actors are complete, including system/automated actors where they exhibit business behavior
- [ ] The glossary defines every core term and matches the project's existing definitions
- [ ] Every rule has a BR-xx ID; every rule containing a number states the source of that number
- [ ] Every story passes INVEST; split stories record their dependencies
- [ ] Every story has ≥3 happy-path AC + ≥2 boundary/error AC; every AC is in Given/When/Then form and independently testable
- [ ] Every AC traces back to a US → REQ; there are no "orphan" AC
- [ ] The state model (if any) was cross-checked both ways against the AC; forbidden transitions are recorded
- [ ] The permission matrix has no blank cells; every unclear cell is a `[TBC]`
- [ ] MoSCoW is assigned; the Must set is the true minimum
- [ ] The `[TBC]`/`[ASSUMPTION]`/`[CONFLICT]` list has an owner and a blocking level for each item
- [ ] The file contains no technology/architecture/UI decisions

## 10. Common Failures & Anti-Patterns

| Failure | Why it breaks things | Do this instead |
|---|---|---|
| AC with happy path only | QA has no basis for testing error cases; Dev decides error behavior themselves | ≥2 boundary/error AC per story are mandatory |
| "The system must be fast / easy to use / secure" in an AC | Untestable; everyone reads it differently | Replace with an observable condition, or move it to an NFR with a number |
| HOW leaking into the BA document ("store it in table X, call API Y") | Ties the Architect's hands and contradicts them when the architecture changes | Record behavior and rules only |
| Assumptions written as facts | Every later team builds on a wrong foundation without knowing it | Label `[ASSUMPTION]` / `[PROPOSED — VALIDATE]` consistently |
| Rules scattered across many AC, worded differently in each | Nobody knows which version is right when editing | Rules live separately as BR-xx; AC only reference them |
| Every story is Must Have | No real prioritization; a delay delays everything | Must = the minimum without which it is meaningless; the rest are Should/Could/Won't |
| Forgetting system actors (reminder jobs, sync jobs) | Automated behavior is specified by nobody, so Dev invents it | Automated actors get stories/AC like human actors |
| Permission matrix defaulting to "Allowed" when unclear | An authorization hole that starts in the document itself | Unclear = `[TBC]`, never default to allowed |

## 11. Handoff to the Next Role

**(a) Who receives your work:** the Architect (Gate 2) is the primary receiver; QA also reads `01-ba.md` from Gate 1 onward to prepare test cases early, and UI/UX reads the actors/flows sections.

**(b) The exact artifacts and required contents:** `01-ba.md` (per `templates/BA.template.md`) containing: actors, glossary, BR-xx business rules with sources, US-xx stories with ≥3 happy + ≥2 boundary/error Given/When/Then AC each and two-way REQ traceability, the state model with forbidden transitions, the permission matrix with no blank cells, MoSCoW priorities, and the open `[TBC]`/`[ASSUMPTION]`/`[CONFLICT]` list with owners and blocking levels.

**(c) Handoff checklist — complete all of these before passing:**
- [ ] Gate 1 is marked PASS in `STATUS.md`
- [ ] No unresolved `[CONFLICT]` remains
- [ ] Every remaining `[TBC]` has an owner, and none of them blocks architecture (or, if one does, it is flagged as blocking in the handoff)
- [ ] The Section 9 gate checklist is fully ticked

**(d) Acceptance criteria the receiving role will check (what gets your work sent back):** an AC that cannot be tested; contradictory rules; a state used in an AC that does not exist in the state model. A return must cite the specific US/AC/BR IDs.

**(e) Handling a rejection / rework loop:** business changes after Gate 1 go through the BA → `01-ba.md` is updated (version bumped, a change log entry added) → the Architect/QA are notified to assess impact. Business rules are never changed via chat messages; a returned document is corrected at Gate 1 and re-checked by the receiver against the same criteria in (d).

## 12. References

- `references/playbook.md` — the detailed INVEST checklist, the Given/When/Then pattern library (happy/boundary/error/permission/state), how to build a state model, MoSCoW criteria, and the requirement-smell list with fixes.
- `templates/BA.template.md` — the official `01-ba.md` structure.
- `templates/SPEC.template.md` — the input spec format, for REQ traceability cross-checks.
- Method foundations: BABOK v3, ISO/IEC/IEEE 29148.
