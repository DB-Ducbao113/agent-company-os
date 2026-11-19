# USER PROMPTS — Ready-made commands for the repo's owner

> Copy-paste prompts for steering an agent that runs Agent Company OS. Keep this file next to chat/START-PROMPTS.md (which covers starting a session; this file covers everything after).

## Starting a task
```
New task: "<your raw request, as detailed as you like>".
Run Gate 0 properly: decompose my input into the Requirement Inventory first, then clarify, playback, spec, routing. Do not start any specialist work yet.
```

## Approving a gate
```
Gate <n> verdict: PASS. Proceed to the next role in the routing.
```
```
Gate <n> verdict: REWORK. Problems: <what's wrong, in your words>. Fix them in this role's artifact and present the gate again — do not move on.
```
```
STOP this direction. Record the reason in STATUS.md and close the task folder.
```

## When you receive a Failure Report
```
Acknowledged. Fix at the owning role as proposed, then re-run the failed case and the full gate suite and show me the new results.
```
```
I override this failure and accept the risk: <your reason>. Record the override in STATUS.md and continue.
```
(Use the override rarely — it exists for deadline emergencies, and the record keeps future-you informed.)

## Checking the agent's work at any moment
```
Show me: current STATUS.md, which gate is active, which test cases have run with PASS/FAIL and their evidence, and what is waiting on me.
```
```
Show me the Requirement Inventory and the coverage result for my original input. Any unmapped segment?
```
```
Which claims in your last report are unverified? Label them.
```

## Resuming in a new session
```
Read this repo and follow AGENTS.md: <repo link or attached FULL-CONTEXT.md>.
Here is the STATUS summary from the previous session: <paste>. Continue from exactly that state — do not redo passed gates.
```

## Ending a task
```
Close this task: final STATUS.md with every gate's verdict, the test summary per gate, any overrides I approved, and the release artifact link if it shipped.
```
