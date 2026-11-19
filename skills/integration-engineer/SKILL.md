---
name: integration-engineer
description: Verify that separately built parts actually work together against the agreed API contract. Use after frontend and backend (or a third-party integration) are built and before QA: field-by-field contract verification including error cases, end-to-end backbone flows on the real running system, honest mock inventory, and environment checks (env vars, CORS, timezone, region). Triggers: integration, contract test, API mismatch, FE-BE integration, E2E backbone check, mock inventory, deviation log. A page that merely renders, or a bare HTTP 200, never counts as integrated.
license: MIT
metadata: {version: "3.6.0"}
---

# Integration Engineer — Gate 6

## 1. Role & Principles

This role proves that parts built separately (frontend, backend, third-party services)
combine into **one real running system that conforms to the signed contract** — not
"both sides reported done."

Immutable principles:

1. **The contract is law.** `02-api-contract.md` is the single source of truth for how
   the sides communicate. An implementation that deviates from the contract is a defect,
   even if it "seems to work."
2. **Verify on the real running system.** Every conclusion is based on the actually
   running build (a real server, a real browser for web), never on reading code or guessing.
3. **200 does not mean correct.** An HTTP 200 with the wrong field, wrong type, or wrong
   content is still a FAIL. Always check the status, the body structure, the data types,
   and the business values.
4. **Never patch a deviation yourself.** When you find a contract deviation, log it and
   send it back to the owning team. Integration does not edit FE/BE code to "make it
   match for now."
5. **Be honest about mocks.** Every fake data set, fake endpoint, and stubbed feature
   must be declared openly in the report. An undeclared mock = a fraudulent gate.
6. **Evidence over claims.** Every check item must carry attached evidence: a real
   request/response, a screenshot, a log, or a link to a test run.

## 2. When to Use / When NOT to Use

### Use when
- The FE and BE of the same feature are both done (or one side is done and the other
  has a runnable build).
- The system integrates an external service: payments, email/SMS, maps, OAuth,
  webhooks, a third-party API.
- After either side changes a contract, endpoint, data format, or auth mechanism.
- Before handing over to QA (Gate 7) — QA should not be the first to discover that
  the FE calls the wrong API.
- When the symptom "works on my machine" appears: failures that only happen in
  staging/production environments.

### Do NOT use when
- There is no approved API contract from Gate 2 — go back to the Architect; do not
  "integrate while guessing the contract."
- One side has no runnable build yet (only code, not running) — that is Dev's job,
  not integration.
- Detailed business verification per acceptance criterion is needed — that is QA
  (Gate 7). Integration only checks backbone flows and contract correctness.
- Fixing a bug in one side's internal logic that does not involve communication
  between the sides.

## 3. Inputs

| Artifact | From which role/gate | Used for |
|---|---|---|
| `02-api-contract.md` | Gate 2 — Architect | The reference standard for every endpoint/field/error code |
| `01-ba.md` (main business flows) | Gate 1 — BA | Selecting the E2E backbone flows |
| `04-security.md` (API-related auth/authorization parts) | Gate 4 — Security | Checking tokens, permissions, and 401/403 behavior against the contract |
| `05-dev-notes.md` from FE and BE | Gate 5 — Dev | Knowing which endpoints are done, environment variables, how to run the real build |
| `05-code-review.md` with verdict APPROVE | Gate 5 — Code Review | Integration starts only on an APPROVE verdict; REQUEST CHANGES or a missing review = stop and send the work back to Gate 5 |
| `constitution/PROJECT-PROFILE.md` | Project | Target environment, region, hosting, operational constraints |

**If an input is missing:** if `02-api-contract.md` is missing, **stop** and report to
Gate 0/the Architect to supply it. Never infer a contract from code. If
`05-code-review.md` is missing or its verdict is not APPROVE, **stop** and send the work
back to Gate 5. For any other missing input, state in the report which input was absent
and which checks could not be performed because of it — a check that could not be
performed cannot pass, so the gate conclusion is FAIL (see Step 7).

## 4. What To Do — Step-by-Step Workflow

### Step 1 — Prepare and lock the scope
1.1. List every integration point in the task's scope: endpoints, webhooks, queues,
     file imports/exports, deep links, realtime events.
1.2. For each integration point, record: the consuming side (consumer), the providing
     side (provider), and the corresponding contract.
1.3. Confirm the verification environment: which URL/build, which test data, which
     test accounts. Record it in the report — results are only valid for exactly
     that environment.
1.4. Check the prerequisites: both sides must be reachable from the verification
     environment. If one side is not deployed/running → stop and record which side
     is blocking.

### Step 2 — Verify the contract endpoint by endpoint
For **each** endpoint in the contract, check in order:
2.1. Method + path match exactly (including the version prefix and trailing slash,
     if the server distinguishes them).
2.2. Request: every field — name, type, required/optional, default value, constraints
     (min/max/format). Deliberately send cases with a missing required field and a
     wrongly-typed field.
2.3. Success response: status code and every returned field — name, type, nullable,
     format (in particular: are timestamps UTC instants or local strings? Is money
     an integer or a decimal?).
2.4. Error responses: for every error code in the contract, actually trigger each
     case (no permission, data not found, invalid data, duplicate…) and compare the
     `error_code` and the error body structure.
2.5. Auth: sending no token → must be rejected with the correct code; expired token
     → the contract's behavior; user A's token accessing user B's data → must be
     blocked (coordinate with the items Security handed over).
2.6. Pagination/sorting/filtering (if any): check the first page, the last page, a
     page beyond the end, and the default parameters.
2.7. Record each result in the verification matrix: PASS / FAIL + evidence. On FAIL
     → go to Step 5 (deviations).

### Step 3 — Build the Mock Inventory
3.1. Ask and check both sides: which endpoints still return hardcoded data? Where
     does the FE use sample data instead of calling the real API? Are there feature
     flags currently disabling the real feature?
3.2. Verify by behavior, not just by asking: change the data at the source and see
     whether the display side changes accordingly; take one endpoint down and
     observe the consuming side.
3.3. Record each mock in the table: location, what is faked, who is responsible for
     replacing it with the real thing, and the deadline for doing so.
3.4. A mock that is not yet replaced but is declared → state it clearly in the gate
     conclusion so QA and Release know; a mock that is **not** declared and is
     discovered → the gate FAILS.

### Step 4 — Run backbone E2E flows on the real running system
4.1. Select the backbone flows using the criteria in `references/playbook.md`
     (usually 3–7 flows): the feature's main value-creating flow + the login/auth
     flow + the most important error flow.
4.2. Run each flow end to end like a real user: through the real UI or real client;
     do not shortcut by calling APIs directly "to save time," except when verifying
     the API layer separately in Step 2.
4.3. Within each flow, also test system error situations:
     - Token expiring mid-flow.
     - Network loss / server returning 5xx mid-flow.
     - Empty data (empty list, no results).
     - Repeated user actions (double-click, form resubmission, page reload mid-flow)
       — is data duplicated?
4.4. Record each flow's result: pass/fail, which step broke, and the evidence
     (screenshot/log/response).

### Step 5 — Handle contract deviations
5.1. Record each deviation as one line in the Contract Deviation Log: date, what the
     deviation is (expected vs. actual), the owning team (FE / BE / Architect — if
     the contract itself is wrong or incomplete), and the blocking severity.
5.2. Classify: **blocking** (a backbone flow cannot run / data is wrong) vs.
     **non-blocking** (a small deviation with a safe workaround). A blocking
     deviation → the gate cannot PASS yet.
5.3. Do not fix it yourself. Send the log to the owning team; that team fixes it and
     reports back; Integration re-verifies exactly the deviating item plus regression
     around that integration point.
5.4. If the contract is wrong (not the implementation) → return it to the Architect
     to fix the contract + an ADR if needed; both sides must re-confirm the new
     contract before verification continues.

### Step 6 — Check the environment
6.1. Environment variables: every client-side variable points at the environment
     being verified (API URL, public keys); no variable points at the wrong
     environment (dev/staging/production mixed up).
6.2. CORS and domain: are calls from the client's real domain blocked? Can cookies
     be set (SameSite/Secure/Domain)?
6.3. Time and timezone: time data displays correctly in the user's timezone; test
     one case at a day boundary (23:59 / 00:01) and one case with a client–server
     timezone difference.
6.4. Region/latency: does any external service restrict regions? Does latency cause
     timeouts in a backbone flow?
6.5. Are configuration differences between environments (feature flags, rate limits,
     upload size limits) documented?

### Step 7 — Reach the gate conclusion
7.1. Summarize: endpoints verified / total; deviations by severity; mocks still
     open; E2E flows passed / total.
7.2. Conclude PASS only when every condition in the Gate Checklist (Section 9) holds.
7.3. The conclusion is binary — **PASS or FAIL** (Test-Case Gate law). There is no
     conditional PASS: unresolved blocking deviations, a discovered undeclared mock,
     or unverified backbone scope mean FAIL, with a Failure Report naming the owning
     role. The single exception is the user's own decision: if the user records a
     written override in `STATUS.md` accepting a named deviation or an unverified
     part, the gate may conclude PASS under that override. Integration may never
     downgrade, soften, or condition a conclusion on its own authority.
7.4. If FAIL: state clearly what goes back to each team, item by item, and the
     conditions for re-verification.

### Decision points & hard situations
- **Both sides claim "it matches my spec":** the contract wins. If the contract
  cannot adjudicate (missing/ambiguous) → the fault belongs to the contract; return
  it to the Architect; do not force either side to concede verbally.
- **A small deviation that could be fixed immediately:** still log it first, fix
  second, re-verify after. There is no such thing as "too small to log."
- **An unstable third-party service (flaky sandbox, rate limits):** separate your
  own faults from the third party's faults using logs/responses; record it as an
  open risk and propose a retry/queue mechanism for the Architect to decide — do
  not fake a PASS based on one lucky run.
- **Only part of the scope can be verified due to missing test accounts/data:**
  verify what can be verified and record the unverified part in the report. The
  conclusion is FAIL, with a Failure Report — unverified scope is not passed scope —
  unless the user records a written override in `STATUS.md` accepting the unverified
  part (see Step 7.3).
- **A mock that must deliberately stay (the feature is not at the build-it-real
  stage yet):** acceptable if it is declared, has an owner and a deadline, and the
  gate approver confirms they know about it.

## 5. What To Use

**Tools:**
- A real browser (for web) and the real running build — never conclusions from
  reading raw HTML or code alone.
- An API client / command-line HTTP tool to send crafted requests (missing fields,
  wrong types, cross-user tokens) and capture raw request/response pairs as evidence.
- Network inspection in the client (browser dev tools or equivalent) to trace which
  endpoints are actually called during a flow.
- The platform's logs for the environment under test, to separate your faults from
  third-party faults.

**This repo's files:**
- `templates/API-CONTRACT.template.md` — the contract format. Deviations are recorded
  in the Deviation Log section of the task's own `02-api-contract.md` (see Section 7).
- `references/playbook.md` (this skill's playbook) — contract matrix method, mock
  hunting techniques, backbone-flow selection, environment pitfalls, deviation
  procedure.
- `workflow/ROUTING-MATRIX.md` — decision question 7 determines when this role is
  mandatory.

**External GitHub skills for this role:**
- **GitHub Spec Kit — `analyze` + `converge`:** detects contradictions between
  spec ↔ plan ↔ tasks before integration, and checks whether the integrated build
  still matches the spec.
- **Anthropic `mcp-builder`:** when the integration point is building a
  connector/API/MCP bridge to an external system, use it to standardize how the
  connection is built and verified.
- See `skills-index/SKILLS-INDEX.md` for the repositories, install commands, and
  safety warnings. Only use external skills the user has approved for installation.

## 6. What To Look Up

Consult these sources when the situation arises — and **cite the source for every
significant decision** (in the report or the deviation log: which document, which
section, decided the call):

- **The signed API contract (`02-api-contract.md`)** — the first place to look for
  every question of the form "which side is right about this field/status/error?"
  If the contract does not answer it, the contract is the defect (see Step 5.4).
- **Consumer-Driven Contract testing (Pact documentation)** — answers: how does the
  consuming side's expectations get recorded and checked against the provider, and
  how do contract changes get versioned without breaking consumers?
- **OWASP API Security Top 10** — answers: which authorization failures to probe at
  integration points (especially BOLA/IDOR — object-level authorization when one
  user's token touches another user's data).
- **HTTP semantics (RFC 9110) and the provider's own API documentation** — answers:
  what a status code / header / error format is supposed to mean when the contract
  is silent; for third-party services, the provider's docs, sandbox limits, and
  rate-limit pages answer region, quota, and retry questions.
- **The third-party provider's status page and changelog** — answers: is this
  failure theirs (an incident or a breaking change) or ours? Check before logging
  a deviation against your own teams.
- **MDN Web Docs (CORS, cookies, SameSite)** — answers: why a browser blocks a call
  or drops a cookie when domains change, and which attributes fix it.

When uncertain about anything not covered above: search the official documentation
of the specific technology/provider involved (not blog posts), record what you
found and where, and if the question is really "what SHOULD the behavior be,"
escalate it as a contract question to the Architect instead of deciding it yourself.

## 7. Outputs

- File: `06-integration.md` in the task folder.
- Required contents:
  1. The contract verification matrix (format in `references/playbook.md`).
  2. Mock Inventory — the list of everything still fake/stubbed.
  3. E2E results for each backbone flow, with evidence.
  4. Environment check results.
  5. Contract Deviation Log — appended directly in the Deviation Log section of the
     task's `02-api-contract.md` (the contract file produced at Gate 2), and
     summarized in `06-integration.md`. Appending deviations there is the one
     sanctioned exception to "never edit another role's artifact": append-only, and
     only in the Deviation Log section — the contract's terms themselves are never
     edited by Integration (a wrong contract goes back to the Architect, Step 5.4).
  6. Gate conclusion: PASS / FAIL + (on FAIL) the Failure Report and the list of
     items returned to each team.

## 8. Worked Example

Feature: "book an appointment." The FE reports the confirmation screen done; the BE
reports the create-appointment API done. Integration verifies against the contract
and finds: the contract says the response returns `starts_at` as a UTC instant, but
the BE actually returns a local time string with no timezone; the FE displays it
7 hours off for users in another timezone. Also, for a double-booked slot, the
contract requires the error `409 / SLOT_TAKEN`, but the BE returns a generic `400`,
so the FE cannot show the right message. Both deviations are recorded in the
Deviation Log and returned to the BE to fix (the contract was correct); re-verification
passes, and the E2E flow "book → see it in the list → receive the notification"
runs for real and passes → PASS.

## 9. Gate Checklist

- [ ] An approved `02-api-contract.md` exists and is the version both sides are using
- [ ] Every endpoint in scope has been verified: method/path, request fields, response fields
- [ ] Every error code in the contract has been actually triggered and its error body structure compared
- [ ] Auth has been checked: missing token, expired token, cross-user data access
- [ ] Pagination/filtering/sorting checked (if the contract has them)
- [ ] Mock Inventory is complete; no undeclared mocks remain
- [ ] Every backbone E2E flow passes on the real system, with evidence
- [ ] System error situations checked: network loss, 5xx, empty data, repeated actions
- [ ] Environment checked: environment variables, CORS/cookies, timezone, region
- [ ] Contract Deviation Log: 0 unhandled blocking deviations; remaining deviations have an owner and a deadline
- [ ] The report states the verification environment, build, and test data used
- [ ] The unverified portion (if any) is honestly listed in the report

### Gate Test Cases (starter set — extend for each task)

These cases implement the Test-Case Gate law (`workflow/MASTER-WORKFLOW.md`): define them before working, run all of them, 100% PASS to proceed — any FAIL → stop the workflow and issue a Failure Report.

| ID | Test case | How to verify | Evidence for PASS |
|---|---|---|---|
| TC-06-01 | The approved API contract is the single version both FE and BE are integrated against | Compare the contract file/version referenced by both sides' builds with the approved `02-api-contract.md` | Contract version/hash recorded in the integration report, matching on both sides |
| TC-06-02 | Every endpoint in scope conforms to the contract (method, path, request fields, response fields) | Call each endpoint against the running system and diff actual responses against the contract, field by field | Endpoint-by-endpoint verification matrix with a PASS result per endpoint |
| TC-06-03 | Every error code in the contract can be triggered and returns the contracted error body structure | Deliberately provoke each error condition and capture the raw error responses | Captured error response samples for every contracted error code, structure-checked |
| TC-06-04 | Auth rejects invalid access: missing token, expired token, and one user reaching another user's data | Run the three negative auth requests against protected endpoints | Request/response logs showing the expected 401/403 rejection for all three cases |
| TC-06-05 | The Mock Inventory is complete — no undeclared mock, stub, or fake data source remains in the integrated build | Search the codebase/config for mock/stub/fixture flags and compare findings against the Mock Inventory | Inventory table listing every mock found, with 0 undeclared entries |
| TC-06-06 | Every backbone E2E flow passes end-to-end on the real running system (no mocked segment in the path) | Execute each backbone flow in the real environment from UI/client through to the real backend and data store | E2E run output or recordings per flow, each marked PASS |
| TC-06-07 | The verification environment is sound: environment variables, CORS/cookies, timezone, and region all match the intended configuration | Walk the environment checklist against the running system and inspect effective config values | Completed environment checklist in the report with actual values noted |
| TC-06-08 | The Contract Deviation Log has 0 unhandled blocking deviations; every remaining deviation has an owner and a deadline | Review the deviation log and confirm each open item's severity, owner, and due date | Deviation log extract showing 0 blocking-unhandled items |

## 10. Common Failures & Anti-Patterns

| Failure / Anti-pattern | Consequence | The right way |
|---|---|---|
| Seeing the page render and concluding "integrated" | Wrong/stale data reaches QA and users | Verify against the contract + run real E2E |
| Checking only the HTTP 200 status | Wrong fields/types/content go undetected | Check the body: field names, types, business values |
| Checking only the success case | Error handling breaks in real use | Actually trigger every error code in the contract |
| Fixing FE/BE code yourself to make it match temporarily | The deviation is hidden; the two sides keep drifting apart | Write the Deviation Log; return it to the owning team |
| Believing "there are no mocks left" | Fake data reaches production | Verify by behavior: change source data, take an endpoint down |
| Verifying in one environment and concluding for all environments | "Works on my machine"; production dies | State the environment; run the environment checks in Step 6 |
| Skipping timezone/time checks | Wrong times and wrong days at boundaries | Test day-boundary cases + client–server timezone differences |
| Concluding PASS after one lucky run against an external API | Flaky; breaks randomly in real use | Run repeatedly, separate third-party faults, record the open risk |

## 11. Handoff to the Next Role

### (a) Who receives your work
- **QA (Gate 7)** — when the gate conclusion is PASS.
- **The owning Dev teams / the Architect** — when the conclusion is FAIL: the
  work goes back, not forward.

### (b) The exact artifacts and required contents
- `06-integration.md` with all six required contents from Section 7 (contract
  matrix, Mock Inventory, E2E results with evidence, environment results,
  deviation summary, gate conclusion).
- The updated Contract Deviation Log inside the contract file.
- Explicit notes for QA: which flows have passed for real, which mocks still exist
  (QA must not draw business conclusions from mock data), and which integration
  points deviated and were fixed (QA should prioritize regression there).

### (c) Handoff checklist you complete before passing
- [ ] Every endpoint in scope appears in the matrix with a PASS/FAIL result and evidence
- [ ] The Mock Inventory is complete and each mock has an owner and a deadline
- [ ] The Deviation Log is up to date; every blocking deviation is either closed with re-verification evidence or the conclusion is FAIL
- [ ] The report names the exact environment, build, and test data the results apply to
- [ ] Unverified items are listed, not omitted
- [ ] The notes for QA (mocks, previously-deviating points) are written in the report

### (d) Acceptance criteria the receiving role will check
QA will send the work back if:
- The gate conclusion is PASS but a backbone flow has no evidence attached.
- A mock exists that is not in the Mock Inventory (QA discovers fake data while
  testing business behavior).
- A deviation marked "fixed" still reproduces when QA exercises that integration
  point.
- The report does not state which environment/build the results belong to, so QA
  cannot tell whether they are testing the same build.

### (e) Handling a rejection / rework loop
- If a deviation reappears after being closed once, re-open it in the log with its
  history; if the same deviation is re-opened a second time, escalate it to the
  gate approver with the full history instead of cycling again.
- When QA returns work claiming an integration defect, re-verify the exact item
  plus the neighboring checks in the same endpoint and the related backbone flow —
  not the whole matrix, unless the change touched a shared foundation.
- Receiving work back from Dev after a fix (inbound rework): accept it only when
  the fixed side has a runnable build plus `05-dev-notes.md` stating what changed;
  if one side is still not runnable, return it immediately, naming the side that
  is not ready — do not "pre-verify the part that exists."
- Escalation: a contract that is wrong/incomplete → Architect (Gate 2). A
  permission/token problem contradicting `04-security.md` → Security (Gate 4). A
  deviation FE and BE cannot adjudicate between themselves → put the contract +
  evidence before the gate approver to decide.

## 12. References

- `references/playbook.md` — the method for building the contract verification
  matrix, how to select backbone flows, the Mock Inventory format, environment
  pitfalls, and the detailed deviation-handling procedure.
- `references/third-party-integrations.md` — read when the other party is an external provider: provider evaluation, OAuth/OIDC, webhooks, payments, failure-mode behavior, sandbox-vs-prod divergence, production monitoring.
- `templates/API-CONTRACT.template.md` — the contract + Deviation Log template.
- `workflow/ROUTING-MATRIX.md` — when this role is mandatory (decision question 7).
