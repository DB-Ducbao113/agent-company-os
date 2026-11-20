# GATE REPORT — Gate [N] · [Role] · Task: [task name]
Date: [ ] · Reported by: [role] · Artifact: [file name]

## 1. Objective
[What this gate had to achieve, per the spec and the Routing Decision — one or two sentences.]

## 2. What was done
- [Work performed, in order. Name the artifact(s) produced or changed.]

## 3. Verification results
[How the work was checked, and the evidence: logs, screenshots, file:line references, measured values.
Every claim states its exact scope — what ran, where, and which dimensions it covered.]

Gate test cases: Total: [N] · PASS: [N] · FAIL: [N] · BLOCKED: [N]

| ID | Result (PASS / FAIL / BLOCKED) | Evidence |
|---|---|---|
| TC-… | | |

[Any FAIL follows the Test-Case Gate law: full stop + a Failure Report. Any BLOCKED case is listed here with its reason — a gate with a BLOCKED case is not PASS.]

## 4. Coverage matrix (mandatory)
[One row per mandatory item of this gate: the role's gate-checklist items, the spec's success criteria, and every standard the gate invokes (for UI work, all five interface states: normal, loading, empty, error, success). A mandatory item with no test case is BLOCKED by definition — leave its Test case cell as `NONE` and its Result as `BLOCKED`; the gate cannot be PASS while any row is not PASS. Evidence paths are relative to this report's folder and must point to real, non-empty files.]

| Mandatory item | Test case(s) | Evidence | Result (PASS / FAIL / BLOCKED) |
|---|---|---|---|
| [item] | TC-… | [evidence file path] | |

## 5. Not tested / not covered (mandatory)
[List everything in this gate's scope that was NOT exercised, with the reason. An empty list must be written as the single line `None.` — never delete this section. Any item listed here that belongs to the gate's mandatory scope blocks PASS, unless the user accepted the gap in writing in STATUS.md — mark such items `[ACCEPTED GAP]`. Items outside the gate's scope are marked `[OUT OF SCOPE]`.]

- [Item not tested — reason]

## 6. Open issues & risks
- [Issue / risk, its owner, and what it blocks — or "None known".]

## 7. Conditions to pass this gate
- [ ] [Condition — from the role's gate checklist and the spec's success criteria]

## 8. Recommended next step
[One concrete step: the next gate, a rework item, or a decision the user must make.]

## 9. Status
NOT STARTED / IN PROGRESS / AWAITING APPROVAL / COMPLETE

**Rules: never mark COMPLETE unless every condition in §7 is met, every coverage-matrix row in §4 is PASS, and §5 holds no unaccepted mandatory gap.** Before requesting the user's verdict, run `python3 scripts/verify-gate.py <this-report.md>` — a report the script rejects is not submittable, whatever its text claims. This status is the role's own report; the gate verdict itself (PASS / REWORK / STOP) belongs to the user and is recorded in STATUS.md by the Orchestrator.
