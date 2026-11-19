# GATE REPORT — Gate [N] · [Role] · Task: [task name]
Date: [ ] · Reported by: [role] · Artifact: [file name]

## 1. Objective
[What this gate had to achieve, per the spec and the Routing Decision — one or two sentences.]

## 2. What was done
- [Work performed, in order. Name the artifact(s) produced or changed.]

## 3. Verification results
[How the work was checked, and the evidence: logs, screenshots, file:line references, measured values.]

Gate test cases: Total: [N] · PASS: [N] · FAIL: [N] · BLOCKED: [N]

| ID | Result (PASS / FAIL / BLOCKED) | Evidence |
|---|---|---|
| TC-… | | |

[Any FAIL follows the Test-Case Gate law: full stop + a Failure Report. Any BLOCKED case is listed here with its reason — a gate with a BLOCKED case is not PASS.]

## 4. Open issues & risks
- [Issue / risk, its owner, and what it blocks — or "None known".]

## 5. Conditions to pass this gate
- [ ] [Condition — from the role's gate checklist and the spec's success criteria]

## 6. Recommended next step
[One concrete step: the next gate, a rework item, or a decision the user must make.]

## 7. Status
NOT STARTED / IN PROGRESS / AWAITING APPROVAL / COMPLETE

**Rule: never mark COMPLETE unless every condition in §5 is met.** This status is the role's own report; the gate verdict itself (PASS / REWORK / STOP) belongs to the user and is recorded in STATUS.md by the Orchestrator.
