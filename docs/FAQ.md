# FAQ & Troubleshooting

## Using the system

**Q: Do I have to run all 8 gates for every task?**
No. Gate 0's Routing Decision picks the roles the task actually needs (12-question tree in `workflow/ROUTING-MATRIX.md`) and records why the rest were skipped. A typo fix takes the fast lane; a payment feature takes everything.

**Q: One agent plays all the roles — isn't "maker ≠ checker" fake then?**
Partly, and the repo is honest about it: on a single-agent setup the roles are separate *passes* with separate artifacts and checklists, which still catches a large class of errors (the WT-06/WT-08 tests show the behavior). It is weaker than truly independent agents/humans — which is why the user remains the approver at every gate, and why completion claims require evidence you can check yourself.

**Q: Can I use this with a non-coding project (writing, research, video)?**
The gates map well: intake/spec, domain roles replacing BA/Architect, review as checker, a QA-equivalent fact/quality check, release = publish. You would write your own role skills following the same structure (docs/CUSTOMIZE.md) and keep the laws (clarify first, artifacts, test-case gate, failure reports).

**Q: My agent asks too many questions now.**
Check the ambiguity scoring in the Orchestrator skill: clear tasks should get ≤3 quick questions or none. If it over-asks on clear tasks, it is mis-scoring — point it at the rubric in `skills/orchestrator-intake/references/playbook.md`. You can also say "use the proposed defaults for the rest" — it must record them as assumptions and proceed.

**Q: The workflow feels slow for medium tasks.**
That is usually full ceremony applied to fast-lane work. Re-check the routing: conditional roles should be off unless their trigger question is truly YES. The system is designed to be proportional — if it isn't, the Routing Decision is wrong, and that is a Gate 0 defect to send back.

## Troubleshooting

**The agent ignores the repo / works like it never read it.**
The bootstrap didn't happen. Re-send the starter prompt (chat/START-PROMPTS.md §1) in a **fresh** session and confirm the agent names Gate 0 and the orchestrator skill in its reply before giving it a task. On coding agents, verify the skills are actually installed in the right folder (README §Installation) — a repo merely cloned next to your project is not automatically loaded.

**The agent started coding without asking anything.**
Run WT-01 from docs/TESTING-GUIDE.md in a fresh session. If it fails there too, the skill files are not being loaded (see above). If it passes WT-01 but skipped questions on your real task, your task may have scored as "clear" — ask it to show its ambiguity score and the Requirement Inventory; both must exist in `00-idea.md`.

**A long session "forgets" the workflow halfway.**
Context compaction. Ask for the STATUS summary (chat/START-PROMPTS.md §4), start a new session with the starter prompt + that summary + the task's artifact folder. The artifacts are the memory — this is by design.

**A test case failed and the agent wants to continue anyway.**
It may not. Point it at the Test-Case Gate law (`workflow/MASTER-WORKFLOW.md`) and require the Failure Report. If *you* choose to override, say so explicitly; the override and the accepted risk must be recorded in STATUS.md.

**Two roles disagree (e.g. Architect vs. Security).**
The disagreement is recorded in both artifacts; the stricter (safer) position holds until you decide. Escalation to the user is the designed path — an agent silently "compromising" a security requirement is a process violation.

**Can I add my own role (e.g. Data Analyst)?**
Yes — follow docs/CUSTOMIZE.md §Adding a new role, keep the 12-section structure, and add its Gate Test Cases.
