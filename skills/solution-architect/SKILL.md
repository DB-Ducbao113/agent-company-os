---
name: solution-architect
description: Design the technical structure of a feature or system before any code is written. Use when a task changes system structure, modules, layout/component systems, routing, state management, APIs, integrations, or data models; when an API contract must be designed contract-first; when an existing architecture or design system must be complied with; or when a significant technical decision needs an Architecture Decision Record (ADR). Produces C4 diagrams (levels 1-2 by default), a signed API contract including error responses and error codes, data models with migration safety, and compliance boundaries for UI/UX and developers. Always inspects the real existing codebase and all relevant branches first; never claims something is absent without checking. Keywords: architecture, C4, ADR, API contract, OpenAPI, system design, data model, migration, contract-first.
license: MIT
metadata: {version: "3.6.0"}
---

# Solution Architect — Gate 2

## 1. Role & Principles

The Architect locks down the **technical frame** that every later team must comply with: system structure, module boundaries, the API contract, the data model, and the major decisions — with a written rationale for every decision.

Non-negotiable principles:

- **Inspect the real system before designing.** Every claim about the current state ("X already exists / does not exist") must rest on inspecting the actual repo/codebase, including relevant branches. Never conclude absence from memory or from one shallow search.
- **Contract before code.** FE and BE do not start until the API contract is confirmed by both sides — even when the same agent plays both roles, the contract must exist in writing first.
- **Major decisions = ADR.** A decision that is hard to reverse or affects many modules needs an ADR. An Accepted ADR is never edited; to change it, write a new ADR that supersedes it.
- **Respect what exists.** The architecture/design system/stack in `PROJECT-PROFILE.md` is the default to comply with. Proposing a deviation requires the reason + cost stated in an ADR — never silently do it differently.
- **Design just enough.** Draw C4 diagrams and specify only to the level the task needs (usually C4 levels 1–2). Over-designing for needs that do not exist is an error, just like under-designing.
- **Clear boundaries for the next teams.** The output must answer: which modules may be modified, which are off-limits, which data is the source of truth, and how errors are represented.

## 2. When to Use / When NOT to Use

**Use when:**

- The routing marks the Architect as mandatory, or conditional with the condition triggered (decision-tree questions 2, 4, 5 = Yes).
- Adding/changing APIs, changing the data model, adding a third-party integration, changing state management/routing, or adding a new module.
- The task must *comply with* an existing architecture or design system (a redesign inside a frame, extending a running system).
- There is a controversial or hard-to-reverse technical decision (choosing an external service, changing the auth mechanism, changing the storage strategy).

**Do NOT use when:**

- Only content/copy/figures change, with no change to structure or technical behavior (fast lane).
- A small bug inside one function/module whose cause and fix scope are already clear and which touches no contract/data → Dev + QA suffice; the Architect joins only if the bug turns out to be a design flaw.
- A throwaway prototype with no integration into the real system → a 5–10-line architecture sketch in the spec is enough; do not run the full Gate 2.

## 3. Inputs

| Input | From which role/gate | Required? | If missing or contradictory |
|---|---|---|---|
| `01-ba.md` with Gate 1 PASS (or the Gate 0 spec, when the routing lets the Architect proceed with a condensed BA) | BA — Gate 1 / Orchestrator — Gate 0 | Yes | Stop and send it back to the previous gate — never design on top of unsettled business logic |
| `00-spec-and-routing.md` (the Invariants, NFR, and Out of Scope sections) | Orchestrator — Gate 0 | Yes | Ask the Orchestrator |
| `constitution/PROJECT-PROFILE.md` (settled stack, hosting, prohibitions) | The project repo | Yes, if it exists | Record `[TBC]`; never choose the stack on the user's behalf |
| The current repo/codebase + branch list | The project | Yes | Without access, state the limitation explicitly and mark every current-state conclusion `[UNVERIFIED]` |
| `templates/API-CONTRACT.template.md`, `templates/ADR.template.md` | This repo | Yes | — |
| Known security requirements (if Security has early input: data types, permission requirements) | Security — Gate 4 (runs in parallel/early when question 6 = Yes) | Conditional | Record the security assumptions in the arch file for Security to review later |

## 4. What To Do — Step-by-Step Workflow

### Step 1 — Survey the current state (mandatory, never skip)
1.1. Read the repo structure: main modules/packages, entry points, the current organization; read existing architecture documents/ADRs if any.
1.2. Check **all relevant branches** before concluding that a feature/module does not exist — work in progress usually lives on another branch, not on the main branch.
1.3. Identify the existing design system/tokens/shared components (for FE) or shared services (for BE).
1.4. Record the current state in its own section of the arch file, with evidence for every claim (the file/folder paths inspected). A claim without evidence → mark it `[UNVERIFIED]`.

### Step 2 — Clarify the technical requirements from the business requirements
2.1. Map every US/BR in `01-ba.md` onto the system: which US can reuse existing modules, which need new parts.
2.2. Extract the NFRs from the spec/BA (performance, data volume, concurrent users, availability requirements) — an NFR missing a number that affects the design → ask back via the Orchestrator/BA, or record an assumption + its risk.
2.3. Identify external integrations (if any): what the third party provides, their limits/error rates/authentication — look up that party's official documentation; never guess their API.

### Step 3 — Design the structure (C4)
3.1. Draw the **Context diagram (level 1)** when the task adds a new external actor or external system; most tasks only need to update the **Container diagram (level 2)**: the independently running/storing blocks (web app, API, worker, DB, external services) and the communication channels between them.
3.2. Go down to **Component level (level 3)** only for the container undergoing the main change, and only when its internal boundaries are contested or several teams work inside it.
3.3. Produce the **module map**: New / Modified (what changes) / Do Not Touch (with the reason it is off-limits, if it is easily touched by mistake).
3.4. Draw the data flow for 1–2 main flows (happy path) and 1 important error flow: who calls whom, with what data, synchronous or asynchronous, and where an error stops.

### Step 4 — API Contract (contract-first)
4.1. List endpoints by US: every US gets at least the endpoints serving its AC, including error cases.
4.2. Specify each endpoint completely: method + path, required auth, request (fields, types, required/optional, validation constraints), success response, and **error responses: HTTP status + a stable error code + message + when it occurs**. Detailed rules are in playbook Section 3.
4.3. Settle the global conventions in the contract: the common error format, pagination, time format (store/transmit absolute UTC instants), idempotency for create/payment operations, and the versioning strategy.
4.4. FE and BE review the contract together once (checklist in Section 9); only when both confirm is it locked. Changes to a locked contract follow the process in the hard-cases table.

### Step 5 — Data model & migration
5.1. Specify new/changed entities: fields, types, constraints (unique, not null, foreign keys), relationships, and indexes for the known main queries.
5.2. Reconcile the data model with the BA's state model: where the state is stored, who may change it, and at which layer invalid transitions are blocked.
5.3. If running data changes: write the migration plan on the **expand → migrate → contract** principle (add new in a backward-compatible way → move the data → remove the old in a later round), including: estimated data volume, run time, the backup plan, how to roll back each step, and the deployment window. Details in playbook Section 4.
5.4. State clearly which data is the source of truth, which is a copy/cache, and how divergence between them is handled.

### Step 6 — Major decisions & ADRs
6.1. Identify the hard-to-reverse decisions in the design (choosing a service, the auth mechanism, the storage strategy, a new module boundary).
6.2. For each such decision: write an ADR from the template — context, the decision, **at least one considered alternative with the reason it was rejected**, and the consequences (good/bad/to monitor).
6.3. An ADR is in Proposed status when presented for approval; it moves to Accepted only when the gate approver agrees. Never edit an Accepted ADR — write a new one that supersedes it.

### Step 7 — Compliance boundaries & packaging
7.1. State for UI/UX: which layout frames/components/tokens must be used, which parts are creatively free, and which are forbidden to break.
7.2. State for Dev: which modules may/may not be modified, that the contract is immutable, and which points require coming back to the Architect instead of deciding alone (schema changes, error-code changes, new dependencies).
7.3. State for Security: the surface to review (new endpoints, sensitive data flows, external integrations) so Gate 4 has its entry points.
7.4. Self-check against the checklist in Section 9, update `STATUS.md`, and hand off per Section 11.

### Handling hard cases

| Situation | How to handle it |
|---|---|
| The BA is not settled yet but you are being pushed to design | Design the frame at a level independent of the unsettled parts (module boundaries, a draft contract marked `[DRAFT — awaiting BA]`); do not lock the contract/data for business areas still open |
| FE and BE disagree about the contract | The Architect arbitrates based on the BA's AC + the global conventions; record the decision + reason in the contract, and in a short ADR if the dispute is large. Never let the two sides build divergent versions |
| The contract must change after Dev has started | Contract-change process: state the reason → assess the impact on both sides → bump the version / record a change entry in the contract → both sides re-confirm. Silent edits are forbidden |
| A third-party integration has poor documentation / no sandbox | Design an anti-dependency layer (adapter) so it can be replaced; record the risk + an early-verification plan for Integration; do not scatter direct third-party calls across the codebase |
| Vague NFRs ("must be fast, must handle load well") | Propose default numbers suited to the project's context, record `[ASSUMPTION]` + how they will be measured; if the number would change the design fundamentally (e.g. requires a queue/cache), block the gate until it is settled |
| A legacy system with no documentation and hard-to-read code | Budget a separate survey step; mark current-state conclusions with a confidence level; propose specifying the current behavior with tests/AC before modifying it (characterization) instead of designing on conjecture |
| Two options are both good and hard to choose between | Compare them in an ADR against agreed criteria (cost of changing later, operational complexity, fit with the existing stack); record the condition under which the losing option would win, so the future knows when to revisit |

### Recording formats

**One endpoint in a contract:**
```
POST /api/v1/appointments
Auth: Bearer — role: patient
Request: { doctorId: string (required), slotId: string (required), note?: string ≤ 500 characters }
Header: Idempotency-Key: string (required)
201: { id, status: "PENDING", startsAt: ISO-8601 UTC, doctorId, slotId }
Errors: 409 SLOT_TAKEN — the slot already has a non-cancelled appointment
        422 SLOT_IN_PAST — the slot is in the past
        401 UNAUTHENTICATED — not signed in / session expired
```

**A "Do Not Touch" section in the arch file:**
```
DO NOT TOUCH: the payments module (stable, out of scope) ·
color/typography design tokens (use them, do not add new tokens in this task) ·
the users table (if a new field is needed, come back to the Architect for a separate migration).
```

**A condensed ADR:**
```
ADR-0007 — Prevent double booking with a unique constraint + 409 error
Context: BR-03 requires at most 1 appointment per slot; two concurrent requests can both pass a code-level check.
Decision: a unique constraint in the DB on (doctor_id, slot_id) over non-cancelled appointments; the API translates a constraint violation into 409 SLOT_TAKEN.
Considered: pessimistic locking per slot (complex, deadlock-prone, rejected); a serial queue (overkill at the current scale, rejected).
Consequences: a partial index by status is needed; when scale exceeds [threshold], revisit under the condition recorded here.
```

## 5. What To Use

**This repo's files:**

| Tool/file | Used for |
|---|---|
| `templates/API-CONTRACT.template.md` | The official contract structure |
| `templates/ADR.template.md` | The official ADR structure |
| `templates/BA.template.md` / the task's `01-ba.md` | The business input, for traceability cross-checks |
| `references/playbook.md` (this skill) | C4 level guidance, ADR writing frame, the API contract rule set (errors/versioning/pagination/idempotency/time), data modeling & migration safety |

**External GitHub skills for this role** (see `skills-index/SKILLS-INDEX.md` for install commands and safety guidance; standard pattern `npx skills add <owner>/<repo> --skill <name>`):

- **BMAD Architect (Winston)** (`bmad-code-org/BMAD-METHOD`) — the architecture process + an implementation-readiness check before development.
- **OpenSkills `system-design`** (`CODE-SAURABH/OpenSkills`) — a structured system-design frame.
- **alirezarezvani/claude-skills — the engineering/architecture group** — architecture patterns, ADRs, design review.
- **OpenSkills `api-design`** — support for standardizing contracts (also used at Gate 6, Integration).

## 6. What To Look Up

Consult these sources when the situation matches; **every major design decision must cite the source it rests on** — the PROJECT-PROFILE constraint, the BA rule it implements, the standard below, or the third party's official documentation — and that citation belongs in the arch file or the ADR.

| Source | What to look up / the question it answers |
|---|---|
| C4 Model (Simon Brown) | Which level does this task need (Context / Container / Component), and where do I stop? See playbook Section 1 |
| ADR format (Michael Nygard) | How is a decision recorded so its context and rejected alternatives survive? When must an ADR be superseded rather than edited? |
| OpenAPI / contract-first practice | How is an endpoint specified completely enough that FE and BE can build independently against it? |
| The API contract rule set in `references/playbook.md` Section 3 | The settled answers for: error format and HTTP status meanings, versioning (breaking vs. compatible), pagination style, idempotency, UTC time, auth errors (401 vs 403 vs 404) |
| Data modeling & migration safety in `references/playbook.md` Section 4 | Where do integrity rules belong (DB vs code)? How is a live-data change sequenced as expand → migrate → contract, with backup and rollback? |
| NFR-to-design table in `references/playbook.md` Section 5 | Which numbers must exist before designing (latency percentile, load, data growth, RTO/RPO, budget), and which design decisions each number drives |
| `constitution/PROJECT-PROFILE.md` | What stack/hosting/design system is already settled for this project — the design must comply unless an ADR justifies a deviation |
| The third party's **official** documentation (for any integration) | What are their real endpoints, limits, error model, and auth method? Never design against a guessed external API |
| Existing ADRs in the project | Has this been decided before? A new design that contradicts an Accepted ADR must supersede it explicitly |

When the current state of the system is uncertain: inspect more of the real codebase (including branches) rather than searching for a generic pattern — current-state questions are answered by the repo, not by references.

## 7. Outputs

| File | Contents | Template/source |
|---|---|---|
| `02-arch-fe.md` and/or `02-arch-be.md` | C4 at the needed level, the module map (new/modified/do-not-touch), the main data flows, compliance constraints for UI/UX & Dev, the NFRs and how they are met | Structure per Section 4 |
| `02-api-contract.md` | Every endpoint in scope: request/response, errors + error codes, auth, pagination, versioning | `templates/API-CONTRACT.template.md` |
| `docs/adr/ADR-xxxx-<slug>.md` — in the **project repo**, never in the task folder (when there is a major decision) | Context, decision, considered alternatives, consequences | `templates/ADR.template.md` |
| The migration section inside `02-arch-be.md` | The data-change plan + deployment safety (details in the playbook) | — |

## 8. Worked Example

Feature: **adding online appointment booking to a SaaS website that manages a clinic** (continuing the BA's example).

- Survey: the repo already has an accounts module + an email notification service; there is no scheduling module; the main branch and one in-progress feature branch were both checked — appointments have never been implemented.
- C4 level 2: Web App → API (a new `appointments` module is added) → DB (new appointments + time-slot tables); API → the existing email service (sends appointment reminders, asynchronously via the system's existing queue).
- Contract (excerpt): `POST /api/v1/appointments` — auth: signed-in patient; request: `doctorId`, `slotId`, `note?`; 201 returns the appointment in `PENDING` status; errors: `409 SLOT_TAKEN` (the slot was just taken), `422 SLOT_IN_PAST`, `403 FORBIDDEN_ROLE`. Creating an appointment requires an `Idempotency-Key` to prevent double booking from double-clicks/flaky networks.
- Data: the `appointments` table carries a unique constraint on (`doctor_id`, `slot_id`) over non-cancelled records — enforced at the DB layer, not only checked in code, because BR-03 (1 slot / 1 appointment) must hold even when 2 requests arrive simultaneously.
- ADR-0007: chooses the unique constraint + 409 error handling over a separate pessimistic-locking queue — reason: simple, uses the DB's existing mechanisms, low reversal cost.
- Constraints for UI/UX: use the design system's existing calendar + form components; for Dev: do not modify the accounts module; if a new permission is needed, come back to the Architect.

## 9. Gate Checklist (Gate 2 — self-check before presenting for approval)

- [ ] The real repo + relevant branches were surveyed; every current-state claim carries path evidence
- [ ] C4 is at exactly the needed level (no changed container missing, no unused extra levels drawn)
- [ ] The module map has all 3 categories: New / Modified / Do Not Touch
- [ ] The data flows include an important error flow, not only the happy path
- [ ] Contract: every endpoint has auth, validation, a success response **and** complete errors with stable error codes
- [ ] The contract settles the conventions: common error format, pagination, UTC time, idempotency (where needed), versioning
- [ ] Both FE and BE have reviewed and confirmed the contract
- [ ] The data model reconciles with the BA's state model; integrity constraints sit at the right layer
- [ ] If there is a migration: expand/migrate/contract, backup, rollback, and volume estimates are all present
- [ ] Every hard-to-reverse decision has an ADR (with a rejected alternative + reason)
- [ ] Compliance constraints for UI/UX, Dev, and Security are stated explicitly
- [ ] No decision contradicts PROJECT-PROFILE without an explanatory ADR

### Gate Test Cases (starter set — extend for each task)

These cases implement the Test-Case Gate law (`workflow/MASTER-WORKFLOW.md`): define the test cases before working, run all of them, 100% PASS to proceed — any FAIL → stop the gate and issue a Failure Report.

| ID | Test case | How to verify | Evidence for PASS |
|---|---|---|---|
| TC-02-01 | Every current-state claim in the arch file rests on a real survey, including all relevant branches | Check the current-state section for the inspected file/folder paths and the list of branches checked behind each claim; claims without evidence must be marked `[UNVERIFIED]` | The survey section of `02-arch-*.md` with path evidence per claim |
| TC-02-02 | The module map is complete: New, Modified, and Do Not Touch categories are all populated | Inspect the module map and confirm each of the three categories has entries (or an explicit "none" with a reason) | The module map in `02-arch-*.md` showing all three categories |
| TC-02-03 | The data flows include at least one important error flow, not only happy paths | Read the flow descriptions and identify the error flow: where the error originates, where it stops, and what the caller receives | The flow section of `02-arch-*.md` documenting the error flow end to end |
| TC-02-04 | Every endpoint in the contract is fully specified: auth, request validation, success response, and error responses with HTTP status plus a stable error code | Walk `02-api-contract.md` endpoint by endpoint against that four-part requirement | The contract file with complete per-endpoint entries, including stable error codes |
| TC-02-05 | The contract settles all global conventions: common error format, pagination, UTC time format, idempotency where needed, and versioning strategy | Check the contract's conventions section for each of the five items | The conventions section of `02-api-contract.md` covering all five items |
| TC-02-06 | Both FE and BE reviewed and confirmed the contract before it was locked | Look for the recorded confirmation from each side (review note, sign-off entry, or STATUS record) predating any implementation work | The confirmation records attached to `02-api-contract.md` / in `STATUS.md` |
| TC-02-07 | The data model reconciles with the BA's state model, and concurrency-critical integrity rules are enforced by DB constraints, not code checks alone | Map each BA state to its storage representation; for each uniqueness/state rule in `01-ba.md`, check a matching DB constraint exists in the model | The data-model section of `02-arch-be.md` listing states, constraints, and where each rule is enforced |
| TC-02-08 | If live data changes, the migration plan is safe: expand → migrate → contract sequencing, with backup, per-step rollback, and a volume estimate | Read the migration section and check for all four elements (sequence, backup, rollback, volume estimate) | The migration section of `02-arch-be.md` containing all four elements |

## 10. Common Failures & Anti-Patterns

| Failure | Why it breaks things | Do this instead |
|---|---|---|
| Concluding "the system doesn't have X" without checking other branches | Duplicate implementation, merge conflicts later | Check all relevant branches; record the survey evidence |
| A contract with success responses only | FE/BE each invent their own error handling; Integration breaks | Specify errors + error codes for every endpoint from the start |
| Using the error message as the error code (matching on text) | Changing the wording breaks the caller | A separate stable error code; the message is display-only |
| Over-engineering the architecture "for the future" | Slows the present, adds useless complexity, hard to maintain | Design for known needs + record the revisit condition in the ADR |
| Enforcing integrity only in the code layer | Two concurrent requests both slip through | Uniqueness rules must be locked in the DB (constraints) |
| A migration that modifies + deletes in a single deployment | No rollback; a mid-way failure loses data | Expand → migrate → contract across separate rounds |
| Editing an Accepted ADR to keep it "tidy" | Decision history is lost; nobody knows why it changed | A new ADR supersedes it; the old one stays untouched |
| The Architect reaching down into business/UI detail decisions | Role conflicts with BA/UI-UX; documents overlap | The Architect locks the frame + constraints; content belongs to the owning team |

## 11. Handoff to the Next Role

**(a) Who receives your work:** UI/UX (receives `02-arch-fe.md` + the compliance constraints) and FE/BE Developers (receive the arch files + `02-api-contract.md`); Security receives the review-surface section.

**(b) The exact artifacts and required contents:** `02-arch-fe.md` and/or `02-arch-be.md` (current-state survey with evidence, C4 at the needed level, module map with all three categories, data flows including an error flow, compliance constraints per receiving team, the migration plan where applicable); `02-api-contract.md` confirmed by both FE and BE, with complete error specifications; ADRs in Accepted state for every major decision.

**(c) Handoff checklist — complete all of these before passing:**
- [ ] Gate 2 is marked PASS in `STATUS.md`
- [ ] The contract has been reviewed and confirmed by both FE and BE
- [ ] ADRs for major decisions are in Accepted state
- [ ] Every remaining technical `[TBC]` has an owner, and none of them blocks the receiving team's work (or blocking ones are flagged as such)

**(d) Acceptance criteria the receiving roles will check (what gets your work sent back):** the contract is missing the error case of an AC; a constraint contradicts the design system/PROJECT-PROFILE; or the data model cannot hold a state the BA requires. A return must cite the specific endpoint/section.

**(e) Handling a rejection / rework loop:** mid-flight architecture changes go through the Architect → the arch file/contract is updated (version bumped, a change entry recorded) or an ADR supersedes → affected teams re-confirm. Dev never changes the contract/schema on their own while coding; a returned design is corrected at Gate 2 and re-checked against the same criteria in (d).

## 12. References

- `references/playbook.md` — C4 guidance per level and when to stop, the ADR writing frame, the API contract rule set (errors/versioning/pagination/idempotency/time), and data modeling & migration safety in detail.
- `references/architecture-patterns.md` — read when choosing or revisiting system structure: the pattern catalog (monolith → microservices, BFF, event-driven, CQRS-lite) with use/avoid/cost, integration and data patterns, auth architecture options, multi-tenancy models, scalability levers in cost order, the weighted technology-selection matrix, and fitness checks for later gates.
- `templates/API-CONTRACT.template.md` — the official contract structure.
- `templates/ADR.template.md` — the official ADR structure.
- `templates/BA.template.md` / the task's `01-ba.md` — the business input, for traceability cross-checks.
- Method foundations: the C4 Model, ADRs (Michael Nygard), OpenAPI contract-first.
