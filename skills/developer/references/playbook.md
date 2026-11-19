# Developer Playbook — Deep Reference

> Read while working Gate 5. SKILL.md gives the workflow; this file gives the detailed techniques.

## 1. The TDD Cycle in Detail

### RED — write a test that fails the right way
- The test describes *behavior* per the AC, not the internal implementation (a refactor must not break tests spuriously).
- One test checks one behavior; the test name reads like an assertion ("returns empty when the month has no data").
- Run the test and *watch it fail*: failing because the behavior does not exist = correct; failing because of a compile/environment error = not RED yet — fix the test first.
- Order of tests for one behavior: the main path (happy path) → edges (upper/lower boundary values) → errors (invalid input, missing permission, external system down).

### GREEN — minimum code
- Write just enough to make the test pass. Deliberately not yet optimized, not yet generalized for cases the AC does not require.
- If "minimum code" takes too long → the slice is still too big; stop and split it smaller instead of pushing on.

### REFACTOR — clean up inside the safe zone
- Only clean up while tests are green; run the tests after each small change.
- Priorities: obvious duplication, misleading names, the overly long function you just wrote. Never let refactoring spread into modules outside the scope.

### When TDD may be waived (record the reason in the dev notes)
- Purely presentational changes against an approved design (color, spacing, text) — verified by screenshot comparison.
- Glue/wiring code containing no logic — verified by a real end-to-end run.
- A throwaway prototype per the routing — it must still run, and must be declared a prototype.
Business logic, calculations, authorization, money/state handling: **never waived**, no matter the urgency.

### Bug fixing with TDD
1. Write a test that reproduces the bug from QA's information (inputs, steps, wrong result).
2. The test must fail on the current code — if it does not fail, you have not reproduced it correctly; go back and ask for information.
3. Fix until the test passes; run regression around the bug's area.
4. The dev notes record: the root cause (not just the symptom) + why this fix blocks that cause.

## 2. Vertical Slicing

- A vertical slice = one complete user behavior cutting through every layer it needs (UI → API → data → response).
  The opposite is a horizontal slice (finish all the DB, then all the API, then all the UI) — horizontal slices only reveal contract drift at the end.
- Slice size: finished + verified within one working session. Bigger than that → split further.
- Slice order: (1) the backbone — the main flow with minimal real data; (2) edge states around the main flow;
  (3) error handling and permissions; (4) polish. Never do (4) while (2)–(3) are unfinished.
- Every slice ends with the system in a *runnable* state; never leave the repo broken between two slices.

## 3. Detailed Frontend Checklist

**System & consistency**
- [ ] Components/tokens taken from the DS; a new component (if unavoidable) placed in the conventional location with all its states
- [ ] No one-off "orphan" styles: any color/spacing/font outside the tokens has a reason recorded in the dev notes
- [ ] UI terminology matches the BA/spec word for word on the key concepts

**States & data**
- [ ] All 5 states; loading does not make the layout jump; empty states offer a next action
- [ ] Each contract error code has its own message/behavior; a network failure offers a retry path
- [ ] Long, empty, or special-character data does not break the layout
- [ ] Forms: keep entered data on error; errors attached to the correct field; the submit button resists double-clicks while sending

**Interaction & access**
- [ ] Every action gives immediate feedback (button state, loading, or a result)
- [ ] Keyboard navigation reaches the main interactive elements; focus is visible
- [ ] Touch targets meet the platform/DS minimum size

## 4. Detailed Backend Checklist

**Input & output**
- [ ] Server-side validation: type, length, value range, format, and relationships between fields
- [ ] Responses match the contract field by field; errors have the correct code + format; no stack traces/SQL/internal details leaked
- [ ] Pagination/limits for lists; the default ordering is explicitly defined

**Permissions & data**
- [ ] Authentication + authorization checked on the server for every endpoint; ownership checked per record (IDOR)
- [ ] Parameterized queries; never concatenate input into commands
- [ ] Important multi-step operations have transactional integrity; duplicate calls handled (idempotency where needed)
- [ ] Sensitive data: encrypted/masked per SEC-REQ; logs contain no secrets/raw data

**Operations**
- [ ] Migrations have a rollback path, or state clearly that rollback is impossible; never edit a migration that has already run for real
- [ ] Environment variables/secrets go through the platform's mechanism; local default values are not real secrets
- [ ] Timeouts/limits on calls to external systems; a third party's failure must not collapse the main flow

## 5. Evidence Standards

Evidence meets the standard when someone else, using only the dev notes, can re-verify your conclusion:

| Work type | Minimum evidence |
|---|---|
| Logic/API | The test command + raw output (test count, pass/fail) + tests for edges and errors |
| Interface | Screenshots of each main state from the real running build + comparison against the design |
| Bug fix | The reproducing test: fails before the fix, passes after (record both results) |
| Migration/data | The migration command + sample data checks before/after + the rollback path tried in a safe environment |
| Performance (if the AC requires it) | Before/after measurements under the same conditions, with the measurement method stated |

Below standard: "tested, OK", a screenshot of code instead of run output, results from a different
environment than the handover environment.
Principle: a strong claim ("correct", "safe", "fast") needs equally strong evidence; without evidence,
lower the claim to exactly the level verified ("ran test X; not yet verified on device Y").

## 6. When to Stop and Escalate

Stop coding and escalate immediately on any of the following — continuing means taking on a decision
outside your authority:

1. Two approved artifacts contradict each other, or an artifact lacks the part that decides the behavior you are about to code.
2. Doing it right would require changing the API contract, the data schema, or a locked business rule.
3. You discover a security risk beyond the current SEC-REQs (an endpoint exposing data, a missing permission check in related old code).
4. The real scope is far larger than the original estimate (double or more), or it touches modules outside the routing.
5. The environment cannot run (a broken baseline, missing permissions/secrets), making verification impossible.

When escalating, submit: the concrete situation (file/section/line), the options you see (2–3 options +
consequences), and the unaffected work you can still continue. Escalating well-prepared is doing the job
right, not a failure.
