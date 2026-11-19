# AGENTS.md — Entry Point (READ THIS FIRST)

> This file is the contract between the user and every AI agent working with this repo.
> If you are an agent: read this entire file BEFORE answering or doing anything for a new task.

## The Purpose of This Repo (never lose sight of it)

This repo exists so that **whenever an agent reaches a role, it knows four things**:
1. **What to do** — the role's step-by-step workflow.
2. **What to use** — the tools, templates, and external skills assigned to that role.
3. **What to look up** — the reference sources and standards to consult, and what to search for when uncertain.
4. **What to hand off** — the exact output artifact that passes the work to the next role, in the format that role can accept.

Every role skill in `skills/` is written in exactly that structure. Follow it.

## Bootstrap Rules (mandatory, no exceptions)

1. **Every new task starts at the Orchestrator.** Read `skills/orchestrator-intake/SKILL.md` and follow it:
   clarify → playback → spec → routing. No task jumps straight into design, code, or tests.
2. **Before acting in any role, read that role's SKILL.md** in `skills/`. Read only the skill relevant to
   the current step (to save context), plus the previous gate's artifact. Read the skill's
   `references/playbook.md` when you need the deep material it points to.
3. **Read `constitution/PROJECT-PROFILE.md`** (if it exists) before every task: it is the project's durable
   truth (stack, design system, brand, invariants). A task that conflicts with the profile → stop and ask the user.
4. **Never guess.** Anything unclear that would change the outcome must be asked. Forced assumptions are
   recorded as `[ASSUMPTION]`; unverified claims as `[TBC]` / `[UNVERIFIED]`.
5. **Gate discipline:** Every stage ends with one artifact (a file) plus a checklist. The next stage does not
   start until the previous gate is PASS (see `workflow/MASTER-WORKFLOW.md`). The user approves gates.
6. **Evidence over claims:** Any "done / works / safe" claim must carry independently checkable evidence
   (raw logs, screenshots, file:line references, test results including a negative control).
   Without evidence, label it "unverified".
7. **No autonomous commit / push / deploy.** The agent prepares; the user approves irreversible actions.
8. **External skills:** When a role needs deeper capability, consult `skills-index/SKILLS-INDEX.md` for the
   GitHub skill assigned to that role and its install command. Only use external skills the user has approved installing.
9. **Handoff discipline:** Work moves between roles ONLY through artifacts. Before passing work on, complete
   the "Handoff to the Next Role" checklist in your skill. If you receive a handoff that fails your role's
   acceptance criteria, send it back with specific reasons — do not silently fix another role's artifact.
10. **Test-Case Gate (hard stop):** Every gate defines its test cases up front and runs all of them.
    The next gate starts ONLY at 100% PASS. A single FAIL stops the workflow: write a Failure Report
    (`templates/FAILURE-REPORT.template.md`) — what failed, expected vs. actual, evidence, suspected cause,
    owning role, proposed fix — and surface it to the user before doing anything else. A fix is verified by
    re-running the failed case AND the full gate suite. Never skip, weaken,
    or quietly work around a failing test case (see `workflow/MASTER-WORKFLOW.md`).
11. **Exhaustive input processing:** The user's instructions are often long and detailed. At Gate 0, decompose
    them item by item into a Requirement Inventory and run a coverage check against the original text
    (protocol in `skills/orchestrator-intake/SKILL.md`): every clause becomes a requirement, a clarifying
    question, or an explicit out-of-scope note. Nothing is dropped or summarized away silently.
12. **Approvals inside a task:** Gate approvals are not the only approvals. Mid-task, pause and ask the user
    BEFORE: (i) a significant architecture change, (ii) deleting or overwriting data, (iii) a risky database
    change, (iv) using a paid or cost-incurring service, (v) a disruptive change to a running system.
    One decision per approval request, with the evidence attached — never batch unrelated approvals into a
    single yes/no (bundled approvals get rubber-stamped, and a rubber stamp is not a decision).
13. **Resume protocol:** At the start of any session on an existing task, first reconstruct where the task
    stands from its task folder — `STATUS.md`, the artifacts present, and the gate verdicts recorded — and
    state the next action before doing anything. Never restart a task from memory or from chat history alone.

## Quick Map — what to read when

| Situation | Read |
|---|---|
| Any new task | `skills/orchestrator-intake/SKILL.md` |
| Overall flow and gates | `workflow/MASTER-WORKFLOW.md` |
| Who hands what to whom | `workflow/ROLE-CHAIN.md` |
| Which roles a task needs | `workflow/ROUTING-MATRIX.md` |
| Writing a spec | `templates/SPEC.template.md` |
| Finding an external skill for a role | `skills-index/SKILLS-INDEX.md` |
| A worked example | `examples/example-redesign-ui.md`, `examples/example-feature-end-to-end.md` |
| A test case failed | `templates/FAILURE-REPORT.template.md` + the Test-Case Gate law in `workflow/MASTER-WORKFLOW.md` |
| A term is unclear | `docs/GLOSSARY.md` |

## Working folder convention for each task (the agent creates this when Gate 0 passes)

```
tasks/<YYYY-MM-DD>-<slug>/
  00-idea.md  00-spec-and-routing.md  01-ba.md  02-arch-*.md  02-api-contract.md
  03-design.md  04-security.md  05-dev-notes.md  05-code-review.md  06-integration.md
  07-test-report.md  08-release.md  FAILURE-REPORT-[nn].md (only when a failure occurs)  STATUS.md
```
Files outside a task's routing are not created — and the Routing Decision must state why each skipped role was skipped.

**ADRs do not live in the task folder.** Architecture Decision Records are project-durable and belong in the project repo (`docs/adr/` or `adr/`); the task folder only references them by ID.

**`constitution/PROJECT-PROFILE.md` is maintained by the Orchestrator.** At task close, the Orchestrator proposes profile updates drawn from the task's retrospective; the user approves them before anything is written.
