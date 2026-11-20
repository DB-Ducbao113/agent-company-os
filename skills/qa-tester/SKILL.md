---
name: qa-tester
description: Independent testing against acceptance criteria. Use to design test cases with ISTQB techniques (equivalence partitioning, boundary value analysis, decision tables, state transition), build an AC-to-test traceability matrix, reproduce bugs before fixes, run regression after fixes, and execute mandatory security test cases handed over by the security role. Triggers: QA, test case, testing, traceability, regression, bug report, severity. Testing starts from requirements, not from the finished code, and the tester never approves their own team's implementation.
license: MIT
metadata: {version: "3.6.2"}
---

# QA / Tester — Gate 7

## 1. Role & Principles

QA is the independent verifier: proving the product **matches the approved
acceptance criteria (AC)**, through traceable test cases and real run evidence —
not "clicked around and it seemed to work."

Immutable principles:

1. **Test from requirements, not from code.** Test cases are generated from the
   spec/BA (Gates 0–1), not from reading the implementation — tests derived from
   code only confirm the code agrees with itself.
2. **Start early.** Read the spec/BA as soon as Gate 1 passes; write test cases in
   parallel while Dev codes. QA that arrives when the code is done is QA that
   arrives late.
3. **Independence.** QA does not verify a product they wrote themselves. Disputes
   about "right or wrong" are settled by the AC, not by opinion.
4. **100% traceability.** Every AC must have at least one test case; an AC with no
   test = unverified, and must be declared openly, never silently skipped.
5. **Bugs must be reproducible.** A bug without reproduction steps and evidence is
   an incomplete bug.
6. **Honesty about what was not tested.** The report lists clearly what was not
   verified and why. An openly declared "not tested" is better than a fake "pass."

## 2. When to Use / When NOT to Use

### Use when
- There is a spec/BA with approved AC and an integrated build that has passed
  Gate 6 (or a runnable build for early testing).
- Test cases must be designed for a new feature, or coverage added for an area
  that just changed.
- A bug needs independent reproduction before Dev fixes it, and regression after
  the fix.
- The mandatory security test list handed over by Security at Gate 4 must be run.
- A formal quality conclusion is needed before any release (Gate 8).

### Do NOT use when
- There are no AC — go back to BA/Orchestrator. QA does not invent pass standards.
- The work is contract verification between FE and BE at the endpoint/field level
  — that is Integration (Gate 6); QA verifies business behavior on the assembled
  product.
- The product is a one-off internal demo prototype — use reduced QA instead: a
  harness check of the main flow + core AC checks, with the reduced scope stated
  clearly in the report.
- A business decision "should we release?" is needed — QA provides the quality
  conclusion and the risks; the release decision belongs to the gate
  approver/Release.

## 3. Inputs

| Artifact | From which role/gate | Used for |
|---|---|---|
| `00-spec-and-routing.md` (success criteria) | Gate 0 — Orchestrator | The overall verification frame, scope and out-of-scope |
| `01-ba.md` (user stories + AC) | Gate 1 — BA | The source for generating test cases and the traceability matrix |
| `04-security.md` (mandatory security test list) | Gate 4 — Security | The security test cases that must not be missing |
| `03-design.md` (5 screen states) | Gate 3 — UI/UX | Verifying all states: default/loading/empty/error/success |
| `06-integration.md` | Gate 6 — Integration | Knowing which flows already passed, which mocks remain, which points previously deviated |
| `constitution/PROJECT-PROFILE.md` | Project | Target devices/platforms, compliance standards (e.g. WCAG) |

**If an input is missing:** if there are no approved AC, stop and return the work
to BA/Orchestrator — do not write tests against invented standards. If
`06-integration.md` is missing or its conclusion is not PASS, you may still test
early, but the report must state clearly that the results are preliminary. If the
mandatory security test list is missing, request it from Security before concluding
the gate; never conclude PASS with the security group silently absent.

## 4. What To Do — Step-by-Step Workflow

### Step 1 — Analyze the requirements and plan the testing
1.1. Read all AC; flag AC that are vague or unverifiable ("the system must be
     user-friendly") → return them to BA for clarification before writing tests.
     Do not interpret vague AC into tests on your own.
1.2. Define the test scope: the new feature, the affected areas, the regression areas.
1.3. Choose a design technique for each AC group (see `references/playbook.md`):
     inputs with value ranges → Equivalence Partitioning + Boundary Value Analysis;
     combinations of conditions → Decision Table; state lifecycles → State
     Transition; everything else → Error Guessing + chartered Exploratory testing
     (a stated exploration goal for the session).
1.4. Estimate risk: which AC, if broken, causes the worst harm (money, data,
     permissions) → test those deepest, and run them first.

### Step 2 — Design the test cases
2.1. Each AC gets ≥ 1 happy-path test case; important AC also get boundary and
     error cases.
2.2. Each test case records in full: ID (TC-xx), linked AC, preconditions, specific
     test data, step-by-step actions, and an expected result that can be checked
     by eye or by numbers.
2.3. Test data must be concrete (actual values), never "enter valid data."
2.4. Mark which test cases are mandatory security cases (from Gate 4) — this group
     is never cut when time runs short.

### Step 3 — Prepare the environment and data
3.1. Use exactly the environment Integration passed; record the build, environment,
     and device/browser.
3.2. Prepare accounts for each role/permission to be tested; data in the different
     lifecycle states.
3.3. If the environment still contains mocks (per `06-integration.md`): record
     which test cases are affected; their conclusions carry only relative weight.

### Step 4 — Execute and record evidence
4.1. Run in descending risk order: backbone flows → main AC → boundary/error →
     security → UI/states.
4.2. Each test case: PASS/FAIL with evidence (screenshot, log, response, numbers).
     On FAIL → open a bug immediately per Step 5; do not batch them to the end of
     the session.
4.3. For web/apps: test on a real browser/device or a close emulator; also check
     the empty state (no data yet), the error state (server error, network loss),
     the slow state (weak network), and different permissions.
4.4. A test that cannot run (blocked by another bug/the environment) → record
     BLOCKED + the reason; never leave it blank and never guess the result.

### Step 5 — Manage bugs
5.1. One record per bug: a title stating the symptom, numbered reproduction steps,
     the actual result, the expected result (pointing to the AC), severity per the
     guide in the playbook, evidence, and environment.
5.2. Check for duplicates before opening a new bug; a bug that does not reproduce
     reliably → record the observed frequency and suspected conditions; do not
     quietly drop it.
5.3. Record which AC each bug belongs to and which test case found it, so
     regression lands in the right place.

### Step 6 — Run the mandatory security tests
6.1. Run the full list Security handed over: wrong permissions (using a low-privilege
     account to perform a high-privilege action), cross-user data access (IDOR),
     expired/tampered tokens, malicious input (special characters, script-like
     content, oversized data), direct URL/API access while not logged in.
6.2. Record each item's result separately in the report; a FAIL in this group is
     high severity by default and blocks the gate until Security re-confirms.

### Step 7 — Regression and re-verification after fixes
7.1. For a fixed bug: re-run the exact reproducing test case → it must pass before
     the bug is closed.
7.2. Run regression around the fixed area: the AC in the same module, the flows
     sharing the component that was just changed, plus the backbone smoke set.
7.3. A bug that is still broken on the second fix, or a fix that breaks something
     else → escalate: record it in the report and propose returning it to
     Dev/Architect to address the root cause instead of patching further.

### Step 8 — Reach the gate conclusion
8.1. Summarize the numbers: total test cases, PASS/FAIL/BLOCKED, bugs by severity,
     AC coverage.
8.2. Conclude PASS only when every condition in the Gate Checklist (Section 9)
     holds. A REWORK conclusion must state: which bugs block, and the conditions
     for re-verification.

### Decision points & hard situations
- **The AC and the product contradict each other and both sides insist:** the
  approved AC wins. If the AC is genuinely wrong → BA amends the AC in writing
  first, and QA tests against the new AC; never test against a verbal promise.
- **Time is short and you are pressured to cut tests:** cut by risk — keep the
  backbone flows, the high-risk AC, and the mandatory security tests intact; cut
  low-risk parts and **state clearly what was cut** in the report so the gate
  approver signs for that risk. Never cut silently.
- **A bug "cannot be reproduced" on Dev's machine:** QA provides more detailed
  environment/data/evidence; if it still does not reproduce, record the status
  "not reproducible — monitoring" with the observation conditions; do not close
  it as fixed.
- **A small UI flaw the AC never mentions:** distinguish clearly between "deviates
  from the AC" (a bug) and "improvement suggestion" (recorded in a separate
  proposals section, does not block the gate) — unless the flaw violates a
  standard stated in the PROJECT-PROFILE (e.g. contrast below the accessibility
  standard), in which case it is a bug.
- **The test environment differs from the users' real environment:** record this
  limitation in the report; a PASS conclusion applies only to the environment
  tested, and the differences are listed under "not verified."

## 5. What To Use

**Tools:**
- A real browser/device or a close emulator for web/app testing, with screenshot
  and console-log capture for evidence.
- An API client to send direct requests for the security group (cross-user IDs,
  tampered tokens, unauthenticated access) — UI-only checks are not enough, because
  a hidden button is not server-side enforcement.
- The mandatory security test list from `04-security.md` as the checklist for Step 6.

**This repo's files:**
- `templates/TEST-REPORT.template.md` — the test report format.
- `references/playbook.md` (this skill's playbook) — ISTQB techniques with fully
  worked examples, the traceability matrix, the bug report standard, the severity
  table, regression strategy, and how to run the security tests.
- `workflow/ROUTING-MATRIX.md` — decision questions 8 and 10 determine when this
  role is mandatory.

**External GitHub skills for this role:**
- **Anthropic `webapp-testing`:** the Playwright toolkit — open the real web app,
  capture screenshots, read console logs, debug UI behavior while testing.
  Install: `npx skills add https://github.com/anthropics/skills --skill webapp-testing`
- **Superpowers:** `test-driven-development` (test-first discipline on the Dev side
  gives QA automated tests to regress with) and `verification-before-completion`
  (evidence discipline before concluding anything is done).
  Install: `npx skills add obra/superpowers --skill test-driven-development` /
  `--skill verification-before-completion`
- **BMAD Test Architect (TEA):** risk-based test strategy and quality-gate
  definitions for larger projects.
- **OpenSkills `qa-engineer`, `test-writer`:** support for designing test cases
  and writing automated tests.
- See `skills-index/SKILLS-INDEX.md` for the repositories, install commands, and
  safety warnings. Only use external skills the user has approved for installation.

## 6. What To Look Up

Consult these sources when the situation arises — and **cite the source for every
significant decision** (in the test report: which document decided a technique
choice, a severity call, or a pass/fail judgment):

- **The approved AC in `01-ba.md`** — the first and final authority for every
  question of the form "is this behavior right or wrong?" If the AC cannot answer
  it, the AC is the defect — return it to BA.
- **ISTQB Certified Tester Foundation Level (CTFL) syllabus** — answers: how to
  apply equivalence partitioning, boundary value analysis, decision tables, and
  state transition testing correctly, and how to choose between them.
- **The security test list in `04-security.md`, backed by the OWASP Testing Guide
  (WSTG)** — answers: exactly which authorization, session, and input-validation
  checks must be executed, and how to execute them safely.
- **WCAG (Web Content Accessibility Guidelines)** — answers: whether a UI state or
  contrast level that the AC never mentions still counts as a defect under the
  compliance standard named in the PROJECT-PROFILE.
- **The platform's official documentation (browser/device/OS vendor)** — answers:
  is this behavior a product bug or a platform quirk of the emulator/environment
  being used? Check before filing.
- **ISTQB / industry severity and priority guidance** — answers: how to grade a
  bug by impact when stakeholders disagree; severity follows impact, never the
  loudest reporter or the effort to fix.

When uncertain about anything not covered above: search the official documentation
or the standard's own source (not blog summaries), record what you found in the
report, and if the question is really "what SHOULD the expected result be," send
it back to BA as an AC question instead of deciding the expectation yourself.

## 7. Outputs

- File: `07-test-report.md` following `templates/TEST-REPORT.template.md`.
- Required contents:
  1. The AC ↔ test case ↔ result ↔ evidence traceability matrix.
  2. The test case list (ID, objective, input data, steps, expected result).
  3. The bug list: reproduction steps / actual / expected / severity / evidence / status.
  4. The regression results that were run.
  5. The mandatory security test results.
  6. The unverified portion + reasons.
  7. The gate conclusion: PASS / REWORK with specific conditions.

## 8. Worked Example

AC: "A user gets a 10% discount only when the order is 500,000 or more, and each
account may use a code only once." QA designs: Equivalence Partitioning for the
order-value range (below the threshold / at or above it); Boundary Value Analysis
at 499,999 / 500,000 / 500,001; a Decision Table for the combination (threshold met
× code already used × code still valid); State Transition for the code lifecycle
(unused → used). Running the tests reveals: an order of 499,999 still receives the
discount (a P1 bug, with reproduction steps and the response as evidence), and an
account that already used the code can use it again in a different login session
(a security bug, P1). Both are fixed; QA re-runs the reproducing cases plus
regression over the checkout group → pass → conclusion PASS.

## 9. Gate Checklist

> **Zero-fail rule (Test-Case Gate law):** this gate's verdict is PASS only at 100% test-case PASS. Any FAIL → STOP the workflow, issue a Failure Report (`templates/FAILURE-REPORT.template.md`) to the user immediately, route the fix to the owning role, then re-run the failed case AND the full suite. Never carry a failing case forward as a "known issue".

- [ ] Every AC has at least one test case in the traceability matrix
- [ ] High-risk AC (money, data, permissions) also have boundary and error cases
- [ ] Test cases carry concrete data and verifiable expected results
- [ ] Testing ran on the build that passed Integration, with the environment/build/device recorded
- [ ] All 5 UI states were checked on the main screens (if there is a UI)
- [ ] The mandatory security test list from Gate 4 was run in full, with results recorded separately
- [ ] Every bug has reproduction steps, severity, evidence, and a link to its AC/test case
- [ ] Open P0 bugs = 0 and open P1 bugs = 0 at the time of the conclusion
- [ ] Fixed bugs were all re-verified with their reproducing case; regression around the fixed areas has run
- [ ] The unverified / cut portion is honestly listed with reasons
- [ ] The gate conclusion states its applicable conditions (environment, scope) — no fake unconditional PASS

### Gate Test Cases (starter set — extend for each task)

These cases implement the Test-Case Gate law (`workflow/MASTER-WORKFLOW.md`): define them before working, run all of them, 100% PASS to proceed — any FAIL → stop the workflow and issue a Failure Report. They are the gate's own quality checks on the testing work itself, complementing (not duplicating) the functional test cases QA designs for the product.

| ID | Test case | How to verify | Evidence for PASS |
|---|---|---|---|
| TC-07-01 | Traceability is complete: every acceptance criterion maps to at least one executed test case | Cross-check the traceability matrix against the full AC list from the BA artifact, both directions | Matrix with 0 unmapped AC and 0 orphan test cases |
| TC-07-02 | Every high-risk AC (money, data, permissions) has boundary and error cases, not only happy-path cases | Inspect the case set for each high-risk AC and confirm boundary-value and failure-mode cases exist | Matrix rows for high-risk AC showing boundary + error case IDs |
| TC-07-03 | Test cases are executable as written: concrete input data and a verifiable expected result for each | Pick a sample of cases and execute them literally, exactly as documented, without improvisation | Sampling note in the report confirming the sampled cases ran as written |
| TC-07-04 | Testing ran on the exact build that passed Integration, with environment/build/device recorded | Compare the build identifier in the test report header with the Integration gate's passed build | Report header naming the build, environment, and device/browser matrix used |
| TC-07-05 | The mandatory security test list handed over from Gate 4 was executed in full, with results recorded separately | Reconcile the Gate 4 security list item by item against the executed results section | Security results section with a PASS/FAIL entry for every handed-over item |
| TC-07-06 | Every bug report is complete: reproduction steps, severity, evidence, and a link to its AC/test case | Audit each open and closed bug in the register for the four required fields | Bug register with no field gaps across all entries |
| TC-07-07 | Open P0 bugs = 0 and open P1 bugs = 0 at the moment of the gate conclusion | Query the bug register filtered by severity P0/P1 and status open, at conclusion time | Register query result/screenshot showing 0 open P0 and 0 open P1 |
| TC-07-08 | Every fixed bug was re-verified with its reproducing case, regression around the fixed areas has run, and anything not verified is honestly listed with reasons | Check re-test results for each fixed bug, the regression run record, and the report's "not verified" section | Re-verification results per fixed bug, regression run log, and a completed "not verified" section |

## 10. Common Failures & Anti-Patterns

| Failure / Anti-pattern | Consequence | The right way |
|---|---|---|
| Writing test cases by reading the just-written code | Tests confirm the code agrees with itself; business defects slip through | Generate tests from the AC before/independently of the code |
| Testing only the happy path | Boundary and error-handling defects reach users | Boundary + error cases are mandatory for important AC |
| "Clicked around, it works" with no test cases | Cannot be repeated, cannot be traced | Test cases with IDs, steps, data, expected results |
| A bug recorded only as "screen X is broken" | Dev cannot reproduce it; time is lost going back and forth | Reproduction steps + actual/expected + evidence |
| Assigning severity by gut feeling / by who shouts loudest | Fix priorities go wrong; dangerous bugs are queued last | Use the severity table in the playbook, based on impact |
| Closing a bug when Dev says "fixed" | The bug is still there but passes the gate | Close only after re-running the reproducing case and it passes |
| Cutting security tests when time runs short | Permission/data holes reach production | The mandatory security group is never cut |
| A report that only says "PASS" with no numbers | Nobody knows what was tested and what was missed | Coverage numbers + the list of what was not verified |
| **Aggregate-green substitution** — presenting a passing metric (e.g. "40/40 assertions") as proof of a broader quality claim its cases never covered (real incident, 2026-11-20: a login/modal/XSS suite at 2 viewports was concluded as overall frontend PASS while the loading state and responsive breadth were never exercised) | Untested mandatory criteria ship under a green verdict; the failure surfaces in production, not in the report | Coverage matrix first (every mandatory item → case → evidence); conclusions scoped to exactly what ran; uncovered mandatory items are BLOCKED, never silently absorbed into a PASS |

## 11. Handoff to the Next Role

### (a) Who receives your work
- **Release (Gate 8)** — the test report, when the conclusion is PASS.
- **Dev** — each bug, for fixing (a return loop, see (e)).
- **BA** — any AC found wrong or ambiguous.
- **Security** — a copy of every security-test FAIL.

### (b) The exact artifacts and required contents
- `07-test-report.md` with all seven required contents from Section 7: the quality
  conclusion, the numbers, the list of still-open bugs (if any) with a risk
  assessment for each for the release decision-maker, the environment tested, the
  unverified portion, and the areas Release should monitor after release.
- Individual bug records, each with its reproducing test case, sent to Dev.
- Written AC corrections/questions, sent to BA — never verbal-only.

### (c) Handoff checklist you complete before passing
- [ ] The traceability matrix is complete: no AC row has an empty test-case column, or the gap is declared under "not verified"
- [ ] Every bug record answers the 6 questions of a quality bug report (see playbook) without needing follow-up questions
- [ ] Fixed bugs show re-verification evidence, not just a "fixed" status from Dev
- [ ] The security group's results are recorded separately and every FAIL has been copied to Security
- [ ] The conclusion states the exact build, environment, and scope it applies to
- [ ] The report's coverage matrix maps every mandatory item (incl. all five UI states for UI work) to an executed case with evidence; uncovered mandatory items are BLOCKED, and `scripts/verify-gate.py` passes on the report
- [ ] Open risks for Release (unverified areas, monitoring suggestions) are written in the report

### (d) Acceptance criteria the receiving role will check
Release will send the work back if:
- The conclusion is PASS but open P0/P1 bugs remain, or the numbers in the report
  do not add up (test cases claimed vs. listed).
- The report does not state which build/environment was tested, so Release cannot
  tell whether the build being shipped is the build that was tested.
- Known unverified areas are absent from the report and surface later.
Dev will (rightly) push back on a bug if it lacks reproduction steps, concrete
data, or evidence — treat that as a failed handoff and complete the record.

### (e) Handling a rejection / rework loop
- **Returning work (to Dev / BA / Security):** bugs go to Dev with the reproducing
  test case; a wrong/ambiguous AC goes to BA; a security FAIL is copied to
  Security. Every return states the exact conditions QA will re-verify against,
  to avoid a loop with no standard.
- **Re-verification after a fix:** re-run the exact reproducing case first (pass →
  close the bug), then regression around the fixed area: the AC in the same
  module, the flows sharing the changed component, plus the backbone smoke set.
- **Loop limit / escalation:** a bug still broken on the second fix, or a fix that
  breaks something else, is escalated — recorded in the report with a proposal to
  return it to Dev/Architect to address the root cause instead of patching again.
- **A bug that cannot be reproduced on Dev's machine:** supply more detailed
  environment/data/evidence; if it still does not reproduce, mark it "not
  reproducible — monitoring" with the observation conditions — never close it as
  fixed, and never let it silently block or silently pass the gate.

## 12. References

- `references/playbook.md` — ISTQB techniques with fully worked examples (EP, BVA,
  Decision Table, State Transition), the traceability matrix, the bug report
  standard, the severity table, regression strategy, and how to run the security
  tests.
- `references/test-design-deep-dive.md` — read when deciding where testing effort goes: risk-based prioritization, exploratory charters, test data, non-functional checks, flaky-test protocol, regression selection, defect clustering, decision-grade reporting.
- `templates/TEST-REPORT.template.md` — the test report template.
- `workflow/ROUTING-MATRIX.md` — when this role is mandatory (decision questions
  8 and 10).
