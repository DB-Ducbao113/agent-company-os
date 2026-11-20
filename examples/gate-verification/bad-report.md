# GATE REPORT — Gate 7 · QA / Tester · Task: Guest login screen (fictional example of a BAD report)
Date: 2026-11-20 · Reported by: qa-tester · Artifact: 07-test-report.md

> This example reproduces a real failure pattern (2026-11-20): a green technical
> suite was presented as proof of overall frontend quality, while mandatory
> coverage (the loading state, responsive breadth) was never exercised.
> `scripts/verify-gate.py` rejects this report on several independent grounds.

## 1. Objective
Verify the guest login screen against its acceptance criteria, including all five interface states and responsive behavior.

## 2. What was done
- Executed the browser suite; produced 07-test-report.md.

## 3. Verification results
Browser suite: 40/40 assertions PASS. Frontend quality is therefore confirmed.

Gate test cases: Total: 40 · PASS: 40 · FAIL: 0 · BLOCKED: 0

| ID | Result (PASS / FAIL / BLOCKED) | Evidence |
|---|---|---|
| TC-07-01 | PASS | evidence/normal-state.log |

## 4. Coverage matrix (mandatory)

| Mandatory item | Test case(s) | Evidence | Result (PASS / FAIL / BLOCKED) |
|---|---|---|---|
| UI state: normal | TC-07-01 | evidence/normal-state.log | PASS |
| UI state: loading | NONE | | BLOCKED |
| UI state: empty | TC-07-03 | evidence/empty-state.log | PASS |
| Responsive: layout at all spec viewports | TC-07-06 | evidence/responsive-full.log | PASS |

## 5. Not tested / not covered (mandatory)
- Loading state during initial page load — the suite waits 10s after navigation, so the initial loading experience was not exercised.
- Error state on a dropped connection mid-login.

## 6. Open issues & risks
- None known.

## 7. Conditions to pass this gate
- [x] All gate test cases PASS with evidence

## 8. Recommended next step
Proceed to Gate 8 (Release).

## 9. Status
COMPLETE
