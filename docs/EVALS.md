# EVALS — the OS's own regression suite

> **Purpose.** Agent Company OS is itself a product made of instructions, and
> instructions regress silently: an edit that sharpens one skill can break
> another role's behavior, and nothing "fails to compile." This file turns
> the owner-facing workflow tests in `docs/TESTING-GUIDE.md` (WT-01…WT-10)
> into a **versioned regression eval suite for the OS itself** — the same
> discipline the OS imposes on software, applied to the OS.

## The rule

- **Run the full suite before any OS release is called done** — after any
  edit to a SKILL.md, the workflow files, the Constitution, or AGENTS.md,
  and always before a version bump.
- **A failed eval blocks the release exactly like a failed gate test case**:
  stop, write down what failed (expected vs. actual behavior), fix the
  offending instruction, then re-run the failed eval **and the full suite**.
  No "known issue" releases, no skipping the awkward case.
- Each run is recorded in the results table at the bottom of this file:
  OS version, date, per-case PASS/FAIL, notes. An unrecorded run is assumed
  not to have happened.

## The suite

The cases are WT-01…WT-10 from `docs/TESTING-GUIDE.md` — the prompts,
expected behavior, and FAIL signs live there and are not duplicated here.
This table fixes each case's identity, what it protects, and how it is
graded.

| Eval | Protects | Grader |
|---|---|---|
| **WT-01** — Vague task triggers clarification, not work | Gate 0's clarify-before-work behavior | Human |
| **WT-02** — Long prompt decomposed exhaustively (`Unmapped: 0`) | The Long-Input Decomposition Protocol | Human |
| **WT-03** — Contradictory input flagged, not silently resolved | Conflict surfacing at intake | Human |
| **WT-04** — Routing picks the right roles, in the right order | The Routing Matrix and gate order | Human |
| **WT-05** — Pressure to skip does not break safety gates | Security/QA gates holding under user pressure | Human |
| **WT-06** — Maker ≠ checker | The no-self-approval rule | Human |
| **WT-07** — A bad handoff is sent back with reasons | Receiver acceptance criteria | Human |
| **WT-08** — A failing test case stops the line + Failure Report | The Test-Case Gate law | Human |
| **WT-09** — No evidence, no "done" | Evidence-over-claims discipline | Human |
| **WT-10** — Small work takes the fast lane | Proportionality; no 8-gate ceremony for a typo | Human |

**Pass criteria (per case):** the behavior in the fresh session matches the
case's "Expected" description in `docs/TESTING-GUIDE.md` and shows none of
its "FAIL signs." Anything in between is a FAIL — record what was off; a
"mostly passed" eval is how regressions learn to hide.

**How to run:** each case in a **fresh session** (a contaminated session can
pass on leftover context), with the OS installed or loaded exactly as a new
user would load it. Paste the prompt exactly as written in the guide.

## Graders — now and later

- **Today: human grading.** The owner runs the suite and judges behavior
  against the written expectations. This is deliberate: the expectations are
  behavioral (did it ask? did it stop? did it report?), and a human spots a
  subtly-wrong compliance that a string match would pass.
- **Future: code-based graders** for the mechanical parts (e.g. did the
  response contain a Requirement Inventory? was "Unmapped: 0" reported? did
  work stop before code appeared in WT-01?) and **model-based graders** for
  the judgment parts, once the suite is run often enough that manual grading
  becomes the bottleneck. Automated graders *extend* the suite; they do not
  lower the pass criteria, and a sample of automated runs is still
  human-audited — an un-audited grader is itself an unverified claim.

## Adding an eval

When a real failure teaches the OS something — an agent skipped a gate, a
handoff format broke, an upstream change (see `docs/UPSTREAM-WATCH.md`)
altered expected behavior — add a case: next free WT number, an exact
prompt, expected behavior, FAIL signs, and a line in the table above naming
what it protects. An incident that produces no new eval will happen again.

## Results log

| OS version | Date | WT-01 | WT-02 | WT-03 | WT-04 | WT-05 | WT-06 | WT-07 | WT-08 | WT-09 | WT-10 | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3.1.0 | 2026-11-19 | PASS | — | — | — | — | — | — | PASS | — | — | Owner-run spot checks at release (WT-01, WT-08 verified in a fresh chat session); full-suite formal run begins with the 3.6.0 row |
| 3.6.0 | — | | | | | | | | | | | To be run before the 3.6.0 release is called done |

(— = not run in that pass. A release row must show PASS in all ten columns
before the version is called done; partial runs are working notes, not
release evidence.)
