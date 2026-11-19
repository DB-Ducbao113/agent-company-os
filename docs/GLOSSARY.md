# GLOSSARY — The repo's terms, defined once

| Term | Meaning in this repo |
|---|---|
| **Gate** | One stage of the workflow (Gate 0–8). A gate is complete only when its artifact exists, its test cases are 100% PASS, and the user has approved it. |
| **Artifact** | The single file a role produces as its output (e.g. `01-ba.md`). Work moves between roles only through artifacts. |
| **Handoff** | Passing an artifact to the next role, after completing the sender's handoff checklist; the receiver may reject it against their acceptance criteria. |
| **Playback** | The Orchestrator reading its understanding of the task back to the user for confirmation before writing the spec. Never skipped. |
| **Spec** | The Gate 0 document (`00-spec-and-routing.md`) describing WHAT is wanted: requirements, scope, out-of-scope, success criteria, routing. Contains no technical solution. |
| **Routing Decision** | The part of the spec that selects which roles run for a task (via the 12-question tree), with a stated reason for every skipped role. |
| **Requirement Inventory** | The item-by-item decomposition of the user's input (especially long input) into numbered segments, each mapped to a requirement, a question, or an out-of-scope note. |
| **Coverage check** | Verifying every input segment is mapped. Required result: `Unmapped: 0`. |
| **EARS** | A notation for unambiguous requirements: "WHEN [event] THE SYSTEM SHALL [behavior]" (plus WHILE / IF-THEN / WHERE patterns). |
| **Acceptance Criteria (AC)** | Given/When/Then statements from the BA that define when a user story is satisfied; QA's test cases trace back to them. |
| **Test case (gate)** | A verifiable check a role defines before working and runs before handing off. Result is PASS or FAIL, with evidence. |
| **Failure Report** | The mandatory written report issued the moment any test case FAILs: what failed, expected vs. actual, evidence, suspected cause, owning role, proposed fix. Stops the workflow. |
| **Maker ≠ Checker** | The rule that whoever produced work never approves it; a different role (or pass) verifies. |
| **Fast lane** | The shortened path for small, low-risk changes (content/typos/config): fewer questions, fewer roles — never applicable to auth/money/data work. |
| **`[ASSUMPTION]` / `[TBC]` / `[UNVERIFIED]`** | Honesty labels: an assumption the agent was forced to make / a fact to be confirmed / a claim lacking evidence. They must appear in artifacts, never be hidden. |
| **PROJECT-PROFILE** | The one file per project holding its durable truth (stack, design system, brand, invariants). Read before every task. |
| **Progressive disclosure** | How skills load: name+description at startup (~100 tokens), full SKILL.md when a task matches, `references/playbook.md` when doing the work. |
