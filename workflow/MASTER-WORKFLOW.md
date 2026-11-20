# MASTER WORKFLOW — The company's gate flow

```
Raw task → GATE 0 Orchestrator (clarify → spec → routing)
  → GATE 1 BA → GATE 2 Architect → GATE 3 UI/UX → GATE 4 Security
  → GATE 5 Developer + Code Review → GATE 6 Integration → GATE 7 QA → GATE 8 Release
```
Roles skipped by Routing are jumped over, preserving the relative order of the rest. Allowed in parallel:
Architect FE ∥ Architect BE (contract agreed at the end) · Dev FE ∥ Dev BE (after the contract) · QA writes test cases from Gate 1 onward · Security early input (when routing Q6 = Yes): Security issues known security requirements to the Architect before Gate 4.

## Gate law (applies to every gate)
- Each gate produces **one artifact** and self-checks against the checklist in that role's SKILL.md.
- The user rules on each gate with exactly three verdicts: **PASS** (proceed) · **REWORK** (back to the same role) · **STOP** (abandon this direction).
- **Maker ≠ Checker:** the next role (or Code Review / QA) is the independent check on the previous one.
- **STATUS.md verdicts are recorded only by the Orchestrator.** Other roles submit status content (progress, evidence, open risks) for their gate; they never mark a gate PASS themselves — PASS is the user's verdict, and the Orchestrator records it.
- **STOP closes the task.** On a STOP verdict, the Orchestrator closes STATUS.md with the final state and the reason, archives the task folder as-is, and records the abandonment. The process ends there; picking the work up again later means a new Gate 0 that references the archived folder.
- An error discovered in an old gate while working in a newer one → go back to the old gate and fix the original artifact; never patch over it downstream.

## Test-Case Gate law (the hard stop — applies at EVERY gate)
Every gate works test-first at the process level:
1. **Define the test cases before doing the work.** Each role derives its gate's test cases from its SKILL.md gate checklist plus the spec's success criteria and acceptance criteria, and writes them into its artifact *before* executing (for QA these are the functional test cases; for design/architecture gates they are verifiable acceptance checks — e.g. "all 5 states present", "every endpoint in the contract has an error format").
2. **Run every test case and record the result with evidence.** Result values are `PASS`, `FAIL`, or `BLOCKED` — `BLOCKED` means the case could not be executed (missing environment, data, access, or an upstream dependency), each with its evidence (log, screenshot, file:line, measured value). "Probably fine" is not a result. A gate with any BLOCKED case is **not PASS**: the gate report must list every blocked case with its reason, and the blockage must be cleared — or explicitly accepted by the user in writing, recorded in STATUS.md — before the gate can pass.
3. **100% PASS is the only way forward.** The next gate starts only when every test case of the current gate is PASS.
4. **One FAIL = full stop.** The workflow halts at that gate. The responsible role immediately writes a **Failure Report** (template: `templates/FAILURE-REPORT.template.md`) stating: which test case failed, the expected vs. actual result, the evidence, the suspected cause, the owning role of the root cause, the proposed fix, and what (if anything) the user must decide. The report is surfaced to the user before anything else continues.
5. **Fix → re-run the failed case AND the full gate suite.** A fix is verified by re-running the whole gate's test cases (not only the one that failed), because fixes regress neighbors. Only a clean 100% PASS reopens the gate.
6. **Never** skip a failing case, mark it "known issue" to proceed, weaken a test case to make it pass, or continue to the next gate "in parallel while fixing" — unless the user explicitly overrides in writing, and that override is recorded in STATUS.md with the risk accepted.
7. **Coverage law — a verdict is only as wide as its coverage matrix.** A gate's test cases must cover **every mandatory item** of the gate (the role's gate checklist + the spec's success criteria + any standard the gate invokes — e.g. for UI work, all five interface states: normal, loading, empty, error, success). The gate report must contain a **coverage matrix** mapping each mandatory item → the test case(s) that check it → the evidence artifact → the result. A mandatory item with **no test case is automatically BLOCKED** — the gate cannot be PASS until coverage is complete or the user accepts the gap in writing in STATUS.md. Running 100% of an incomplete suite proves only the suite, never the gate.
8. **Claim-scoping law — conclusions never exceed what was executed.** Every result claim states its scope exactly: the cases run, the environment, the dimensions covered (e.g. "40/40 assertions PASS — guest login, modal, date edit, XSS, permissions; viewports 390×844 and 1280×800; loading state not exercised"). An aggregate metric must never be presented as proof of a broader quality claim its cases did not cover. Substituting a green metric for an untested criterion is a named process violation (**aggregate-green substitution** — see the qa-tester skill's anti-patterns). Reports also carry a mandatory **"Not tested / not covered"** list; anything on it that belongs to the gate's mandatory scope blocks PASS exactly like a BLOCKED case.
9. **Machine verification.** A gate report that follows `templates/GATE-REPORT.template.md` can be checked mechanically with `scripts/verify-gate.py <report.md>`: it validates the coverage matrix (every row has a case, an existing non-empty evidence file, and a PASS result), the not-tested list, and the status consistency, and exits non-zero on any violation. A report that fails the script is not submittable for the user's verdict, whatever its text claims.

## Pre-Implementation Consistency Audit (after Gate 4, before Gate 5)

Before any code is written, the complete planning set gets one cross-check as a set — per-gate checks only ever see one artifact at a time. (Modeled on Spec Kit's `analyze` step and BMAD's implementation-readiness gate.)

- **Scope:** spec × BA document × architecture × API contract × design × security requirements — the full set, read together.
- **What it looks for:** conflicts between artifacts (the contract contradicts the BA rules; the design needs a state the spec never defines), gaps (a requirement no artifact picks up), and orphan requirements (specified, but owned by no downstream artifact).
- **Read-only:** the audit **never edits artifacts**. Every finding goes back to the gate that owns it, is fixed there, and the audit re-runs.
- **Blocking verdict:** Gate 5 does not start until the audit comes back clean (no unresolved conflicts, gaps, or orphans).
- **Ownership:** the Orchestrator runs or schedules the audit (see the orchestrator skill, Step 8.4) and records its verdict in STATUS.md.

## The user's gate-review checklist (5 questions, ~5 minutes)
1. Does the artifact file exist and open?
2. Does it follow the previous gate's artifact (or did the role invent extra scope)?
3. Is anything fabricated outside the agreed scope?
4. Where is the evidence (logs / screenshots / tests), and can it be checked independently?
5. What is the biggest remaining risk — and is it acceptable?

## Fast lane (small, low-risk work)
Fixing text/data/typos, display-only config changes: shortened Orchestrator (≤2 questions) → Developer → QA verifies against the source.
Conditions: no behavior change, no layout change, no touching auth/data/money. Outside those conditions → full flow.

## Deep Work (heavy tasks — the fast lane's opposite)
At Gate 0 the Orchestrator classifies the task. Work that is multi-session, produces a rich artifact (3D scene, full app, video, long document), has iterative/visual quality, or needs long-running compute is **Deep Work** and runs under `workflow/DEEP-WORK-PROTOCOL.md`: a Deep Work Plan with a re-runnable production pipeline, per-stage on-disk checkpoints, a pre-declared quality rubric scored by a checker across iterations, and declared budgets. Budget exhaustion means checkpoint + report — never a silent cut to quality or scope. Misclassifying Deep Work as Standard (or fast lane) is a Gate 0 defect.

## Correct-course (requirements change mid-task)
Requirements changing mid-flight is normal; absorbing them silently is not.
1. **Record the change** in the spec (new version) and in STATUS.md — what changed, who requested it, when.
2. **Assess the blast radius:** which already-completed gates does the change touch (a changed business rule touches BA; a changed flow touches UI/UX; a changed data shape touches the Architect)?
3. **Re-run ONLY the affected gates** — each re-checks its artifact against the changed spec and re-runs its gate test cases. Unaffected gates keep their PASS.
4. The change is never "just handled" inside the current gate: if it alters scope, behavior, or routing, the Orchestrator re-presents the affected part for the user's approval, exactly as in the rework loop.

## Retrospective (after Gate 8)
Once a task is released (or closed), the Orchestrator appends a short lessons record to the task folder: what went well, what failed or surprised, which assumptions proved wrong, and what the company should do differently next time. Lessons that are durable (project facts, conventions, recurring pitfalls) are **proposed** as updates to `constitution/PROJECT-PROFILE.md` — the user approves them before they are written (see AGENTS.md).
