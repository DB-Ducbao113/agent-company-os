# WORKED EXAMPLE 2 — A small feature through every gate (fictional)

> Task (fictional project "BookMyClinic", see example-project-profile.md): **"Let patients cancel an appointment."**
> This example shows the artifacts, the test-case gate in action — including one real FAIL and its Failure Report.

## Gate 0 — Orchestrator
- Decomposition: 1 segment (short input) → requirement "patient can cancel own appointment".
- Clarifying round (3 questions): cancel until when? (default proposed: up to 4h before) · does the slot reopen instantly? (default: yes) · notify the clinic? (default: yes, in-app + SMS).
- Playback confirmed. Spec written with REQ-01…REQ-04, out-of-scope: "no refund logic (appointments are free)", "no reschedule in this task".
- Routing (12-question tree): BA ✅ (state rules) · Architect ✅ (state transition + API) · UI/UX ✅ (button + confirm dialog) · Security ✅ (ownership/IDOR risk) · Dev ✅ · Integration ✅ · QA ✅ · Release ✅.

## Gate 1 — BA (artifact `01-ba.md`)
- Story US-01 + AC: cancel own appointment ≥4h before → status CANCELLED, slot reopens; <4h → action hidden, message explains; cancelling someone else's → impossible (see Gate 4); double-cancel → idempotent, no error storm.
- Gate test cases TC-01-01…06: all PASS (state model cross-checked against AC both directions).

## Gate 2 — Architect (`02-arch-cancellation.md`, `02-api-contract.md`, ADR-0012)
- `POST /api/v1/appointments/{id}/cancel`, idempotency key required; errors: `409 TOO_LATE`, `403 NOT_OWNER`, `404 NOT_FOUND`. State transition enforced in a DB transaction. ADR-0012: cancellation as a status, not a row deletion (audit trail).

## Gate 3 — UI/UX (`03-design.md`)
- Cancel button (destructive style) on the appointment detail, confirmation dialog stating the 4h rule, success state freeing the slot, empty/late states designed — 5 states covered. TC-03 suite: PASS.

## Gate 4 — Security (`04-security.md`)
- Threat: IDOR (cancel by guessing IDs) → server checks ownership on every call; rate limit on the endpoint; mandatory security tests handed to QA: cancel with another patient's token (must 403), cancel with expired token (401), replay with same idempotency key (no double effect).

## Gate 5 — Developer + Code Review (`05-dev-notes.md`, `05-code-review.md`)
- Implemented per contract; unit tests for the 4h boundary (3 points: 3h59, 4h00, 4h01). Code Review: 1 [BLOCKER] — the 4h check used the server's local time instead of UTC → fixed, re-reviewed, APPROVE.

## Gate 6 — Integration (`06-integration.md`)
- FE↔BE verified against the contract on staging. **One FAIL:** TC-06-04 "slot reopens after cancel" — the booking page cached the slot list for 60s, so a cancelled slot still showed as taken.
- **Workflow STOPPED.** Failure Report FR-001 issued: expected "slot bookable immediately after cancel", actual "still blocked ≤60s", evidence (staging timestamps + cache headers), suspected cause "slot-list cache not invalidated on cancel", owning role: Developer (BE cache), proposed fix: invalidate the slot cache inside the cancel transaction.
- Fix applied → failed case + full Gate 6 suite re-run: **100% PASS**. Gate reopened.

## Gate 7 — QA (`07-test-report.md`)
- 23 functional cases traced to AC (incl. boundary, error, and all 3 mandatory security tests): 23/23 PASS. Regression on booking flow: PASS.

## Gate 8 — Release (`08-release.md`)
- Version 1.4.0 (MINOR), changelog entry, rollback plan (feature flag `cancellations_enabled`, default on; rollback = flag off), smoke test on the production URL (book → cancel → rebook): PASS. Owner approved release in chat.

**Total elapsed shape:** 8 gates, 1 real failure — caught at Integration instead of by patients, reported in writing within the same session, fixed at the owning role, and re-verified with the full suite. That is the system working as designed.
