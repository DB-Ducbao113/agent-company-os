# DEEP WORK PROTOCOL — Heavy tasks, top-tier output

Most agent failures on heavy work share one root cause: the task is treated as a
single conversational turn, so the agent cuts quality to fit the turn. This
protocol is the opposite contract: **heavy work runs as a multi-stage pipeline
with checkpoints, scripted production, and scored iteration — however many
sessions it takes.** Speed is negotiable; the quality bar is not.

## When a task is Deep Work (classification)

The Orchestrator classifies every task at Gate 0 / routing and records the
class in the Spec and STATUS.md. A task is **Deep Work** when ANY of these hold:

- It is expected to exceed one session, or roughly 30+ tool actions.
- It produces a rich artifact: a 3D scene/model, a full application, a long
  document or deck, a video, a data pipeline.
- Its quality is **iterative or visual** — "good" is judged by looking,
  comparing, and refining, not by a single check.
- It needs long-running computation: rendering, building, training, encoding,
  large test suites.
- The cost of a mediocre result is high (public launch, client-facing, money).

Everything else is Standard work and follows the normal gate flow (or the fast
lane). Misclassifying Deep Work as Standard is a Gate 0 defect.

## The five laws

### 1. Pipeline, not handwork
Heavy production is done by **scripts and pipelines the agent writes** —
generator code (e.g. Blender Python, build scripts, scene code, document
generators) that is deterministic, parameterized, and re-runnable end-to-end.
The agent directs and verifies; the machine does the long labor. One-off manual
manipulation is for exploration only — anything that survives into the result
must be reproducible by re-running the pipeline.

### 2. Stages with checkpoints on disk
The work is decomposed into stages in a **Deep Work Plan**
(`templates/DEEP-WORK-PLAN.template.md`). Every stage ends with:
(a) its artifact file(s) saved on disk, (b) STATUS.md updated — stage, evidence,
next step, (c) the stage's verification result. **No stage may exist only in
chat context.** A session that ends mid-task leaves a clean checkpoint, never
a half-state.

### 3. Scored iteration loop
Before production starts, the plan defines a **quality rubric**: the criteria
that make the result top-tier for THIS task, each with a pass threshold
(e.g. for a 3D scene: silhouette/proportion match to reference, material
realism, lighting, clean geometry, renders from 3+ angles). Each iteration is:
produce → capture evidence (renders, screenshots, measurements — from multiple
angles/states, not one flattering view) → a **checker** (not the maker) scores
against the rubric → a written fix list → next iteration. The loop ends when
the rubric passes or the iteration budget is spent. Ending below threshold is
reported as REWORK with the gap list — never silently accepted.

### 4. Budget honesty — no silent quality cuts
Budgets (iterations, sessions, compute time) are declared in the plan up
front. When a budget runs low, the agent finishes the current checkpoint
cleanly, updates STATUS.md, and reports: what is done, the rubric score so
far, what is missing, and what the next session should do. **Lowering the
quality bar, the rubric threshold, or the scope to fit a budget requires the
user's written approval** (the mid-task approval law) — an agent that quietly
ships 60% as "done" has failed the task even if the artifact looks plausible.

### 5. Long-running compute discipline
Renders, builds, and other long jobs run as background jobs with logs. The
agent monitors the logs; it does not block the session narrating a progress
bar. When a job fails, the fix goes into the **pipeline** and the job re-runs —
outputs are never hand-patched, because a hand-patched output cannot be
reproduced and hides the pipeline defect that will recur.

## Sessions and resume

- **Session start:** read STATUS.md and the Deep Work Plan; verify the last
  checkpoint's artifacts actually exist on disk; continue from the next stage.
- **Session end:** leave a checkpoint summary in STATUS.md — stage reached,
  rubric score, evidence paths, exact next action.
- The plan is a living artifact: stage changes follow the correct-course
  protocol (record, assess blast radius, re-approve scope changes).

## Anti-patterns

| Anti-pattern | Why it fails | The right way |
|---|---|---|
| One-shot heroics — attempting the whole heavy task in a single turn | Quality is cut invisibly to fit the turn | Classify Deep Work; pipeline + stages + checkpoints |
| Hand-crafting the artifact instead of scripting its production | Not reproducible; every fix risks the whole result | Generator pipeline; fix the pipeline, re-run it |
| "Looks good" with no rubric or one flattering render | Unverifiable, self-graded quality | Pre-declared rubric, multi-angle evidence, checker scores it |
| Quietly shrinking scope/threshold when time runs short | The user receives 60% labeled as done | Budget honesty: checkpoint, report the gap, ask |
| State kept only in the conversation | Session loss = work loss | Artifacts + STATUS.md on disk at every stage |
| Blocking the session on a long render/build | Burns the session on waiting | Background job + logs; verify from the logs |

## Worked mini-example — a 3D product scene

1. **Classify:** Deep Work (rich artifact, visual quality, render compute).
2. **Plan:** stages = brief/references → blockout → detail pass → materials &
   lighting → render set → QC. Rubric: proportions match reference (3-angle
   renders), materials read correctly under the key light, no visible geometry
   defects, poly budget met. Iteration budget: 4. 
3. **Pipeline:** one Blender Python script builds the scene from parameters;
   a render script outputs the 3 standard angles.
4. **Loop:** iteration 1 scores 3/5 rubric criteria → fix list (bevel widths,
   key-light angle) → script parameters change → re-run → iteration 2 scores
   5/5 → gate evidence = the render set + the scored rubric.
5. **Budget event:** if iteration 4 still failed a criterion, the report says
   exactly which one and why — the user decides: more budget, lower threshold,
   or accept with the gap recorded.
