# ROLE CHAIN — How work circulates from role to role

> This is the map of the whole company on one page. Work moves ONLY through the artifacts in this table.
> Each role's SKILL.md details its own row: what to do, what to use, what to look up, and how to hand off.

| # | Role (skill) | Receives (from) | Produces → Hands to | Handoff artifact |
|---|---|---|---|---|
| 0 | Orchestrator (`orchestrator-intake`) | The user's raw task + PROJECT-PROFILE | Spec + Routing Decision → BA (and every later role reads the spec) | `00-idea.md`, `00-spec-and-routing.md`, `STATUS.md` |
| 1 | Business Analyst (`business-analyst`) | Spec (Gate 0) | Stories, business rules, acceptance criteria → Architect, UI/UX, QA (QA starts test design from this) | `01-ba.md` |
| 2 | Architect (`solution-architect`) | BA doc + existing codebase | Structure, API contract, ADRs → UI/UX (layout frame), Developer (build frame), Security (surface map) | `02-arch-*.md`, `02-api-contract.md`, ADR files |
| 3 | UI/UX (`ui-ux-design`) | BA doc + Architect's frame + design system | Researched design + prototype → Developer FE; states & flows also inform QA cases | `03-design.md` + board/prototype |
| 4 | Security (`security-engineer`) | Architect's design + contract | Threat model, permission matrix, mandatory security requirements → Developer (must implement); security test list → QA (must execute) | `04-security.md` |
| 5 | Developer (`developer`) | Spec + BA + contract + design + security requirements | Working implementation + evidence → Code Review, then Integration | code + `05-dev-notes.md` |
| 5b | Code Review (`code-review`) | Developer's diff + spec/contract | Verdict + findings → Developer (fix loop); APPROVE unlocks Integration | `05-code-review.md` (its own file — never a section inside the developer's notes) |
| 6 | Integration (`integration-engineer`) | FE + BE builds + API contract | Verified combined system, deviation log, honest mock inventory → QA | `06-integration.md` |
| 7 | QA (`qa-tester`) | BA acceptance criteria (from Gate 1) + integrated build + Security's test list | Test report with traceability → Release (PASS required); bugs → Developer (fix → re-test loop) | `07-test-report.md` |
| 8 | Release (`release-devops`) | QA PASS + user's explicit release order | Live, verified release + changelog + rollback plan → the user / end users | `08-release.md` |

## The circulation rules
1. **No artifact, no handoff.** If the file doesn't exist or is incomplete against the sender's handoff checklist, the receiver sends it back — they do not start.
2. **Receivers check, senders prove.** Each SKILL.md states the acceptance criteria its receiver will apply; the sender completes their handoff checklist against those same criteria before passing.
3. **Rework returns to the owner.** A defect goes back to the role that owns that decision (business rule → BA, contract → Architect, visual → UI/UX, code → Developer), never fixed silently by the finder.
4. **The spec is the spine.** Every artifact references the spec (requirement IDs, acceptance criteria IDs) so any output can be traced back to what the user actually asked for.
5. **STATUS.md is the board — and only the Orchestrator records verdicts in it.** The Orchestrator keeps `STATUS.md` current: which gate is active, what is waiting on whom, which risks are open. Other roles *submit* their status content (progress, evidence, risks) to the Orchestrator; they never mark their own gate PASS — PASS is the user's verdict, and the Orchestrator records it. On a STOP verdict, the Orchestrator closes STATUS.md with the final state and the reason, and archives the task folder as-is (see `workflow/MASTER-WORKFLOW.md`).
