# MASTER WORKFLOW — The company's gate flow

```
Raw task → GATE 0 Orchestrator (clarify → spec → routing)
  → GATE 1 BA → GATE 2 Architect → GATE 3 UI/UX → GATE 4 Security
  → GATE 5 Developer + Code Review → GATE 6 Integration → GATE 7 QA → GATE 8 Release
```
Roles skipped by Routing are jumped over, preserving the relative order of the rest. Allowed in parallel:
Architect FE ∥ Architect BE (contract agreed at the end) · Dev FE ∥ Dev BE (after the contract) · QA writes test cases from Gate 1 onward.

## Gate law (applies to every gate)
- Each gate produces **one artifact** and self-checks against the checklist in that role's SKILL.md.
- The user rules on each gate with exactly three verdicts: **PASS** (proceed) · **REWORK** (back to the same role) · **STOP** (abandon this direction).
- **Maker ≠ Checker:** the next role (or Code Review / QA) is the independent check on the previous one.
- An error discovered in an old gate while working in a newer one → go back to the old gate and fix the original artifact; never patch over it downstream.

## Test-Case Gate law (the hard stop — applies at EVERY gate)
Every gate works test-first at the process level:
1. **Define the test cases before doing the work.** Each role derives its gate's test cases from its SKILL.md gate checklist plus the spec's success criteria and acceptance criteria, and writes them into its artifact *before* executing (for QA these are the functional test cases; for design/architecture gates they are verifiable acceptance checks — e.g. "all 5 states present", "every endpoint in the contract has an error format").
2. **Run every test case and record the result with evidence.** Result values are only `PASS` or `FAIL`, each with its evidence (log, screenshot, file:line, measured value). "Probably fine" is not a result.
3. **100% PASS is the only way forward.** The next gate starts only when every test case of the current gate is PASS.
4. **One FAIL = full stop.** The workflow halts at that gate. The responsible role immediately writes a **Failure Report** (template: `templates/FAILURE-REPORT.template.md`) stating: which test case failed, the expected vs. actual result, the evidence, the suspected cause, the owning role of the root cause, the proposed fix, and what (if anything) the user must decide. The report is surfaced to the user before anything else continues.
5. **Fix → re-run the failed case AND the full gate suite.** A fix is verified by re-running the whole gate's test cases (not only the one that failed), because fixes regress neighbors. Only a clean 100% PASS reopens the gate.
6. **Never** skip a failing case, mark it "known issue" to proceed, weaken a test case to make it pass, or continue to the next gate "in parallel while fixing" — unless the user explicitly overrides in writing, and that override is recorded in STATUS.md with the risk accepted.

## The user's gate-review checklist (5 questions, ~5 minutes)
1. Does the artifact file exist and open?
2. Does it follow the previous gate's artifact (or did the role invent extra scope)?
3. Is anything fabricated outside the agreed scope?
4. Where is the evidence (logs / screenshots / tests), and can it be checked independently?
5. What is the biggest remaining risk — and is it acceptable?

## Fast lane (small, low-risk work)
Fixing text/data/typos, display-only config changes: shortened Orchestrator (≤2 questions) → Developer → QA verifies against the source.
Conditions: no behavior change, no layout change, no touching auth/data/money. Outside those conditions → full flow.
