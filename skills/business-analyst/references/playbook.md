# Playbook — Business Analyst (deep reference)

> The extension of `SKILL.md`: detailed checklists, the AC pattern library, state models, MoSCoW, and requirement smells.

## 1. INVEST Checklist for Every User Story

| Letter | Criterion | Self-check question | Violation sign → fix |
|---|---|---|---|
| I — Independent | Relatively independent | Can this story be built without waiting for another story to finish? | A hard dependency → record the dependency explicitly; consider merging or reordering |
| N — Negotiable | Negotiable | Does the story describe an *outcome*, leaving the implementation open to discussion? | The story reads like a technical spec → rewrite it in terms of behavior |
| V — Valuable | Valuable | Can the value in the "so that…" clause be named for a specific actor? | "So that the system is better" → ask for the real value, or drop the story |
| E — Estimable | Estimable | Can a developer estimate the effort after reading it? What unknowns remain? | The unknowns are unsettled rules → settle the rule, or attach a blocking `[TBC]` |
| S — Small | Small enough | Can it be built + verified within one short cycle? | Multiple actors/independent flows in one story → split it |
| T — Testable | Testable | Can at least one AC with a clear pass/fail be written? | No AC can be written → the story is a wish; handle it per Step 6 / the hard-cases table in SKILL.md |

## 2. Given/When/Then Pattern Library

### 2.1 Happy path (the favorable flow)
```
Given [a valid initial state]
When [the actor performs the main action]
Then [the main result, observable] And [side effects if any: notification, business log entry, new state]
```

### 2.2 Boundary cases — always test 3 points: just below the boundary / exactly at the boundary / just above the boundary
```
Example rule: uploaded files may be at most 10 MB.
Given a file of 9.9 MB → When uploaded → Then success.
Given a file of exactly 10.0 MB → When uploaded → Then success (at the boundary: allowed).
Given a file of 10.1 MB → When uploaded → Then rejected, the message states the 10 MB limit, and no partial record is created.
```

### 2.3 Error cases / bad conditions
```
Given [a bad condition: network drops mid-way, invalid input data, an external service does not respond]
When [the action]
Then [which consistent state the system keeps] And [what the user sees] And [whether they can retry, and how]
```
Bad-condition groups to scan: empty/malformed/overlong input · duplicates (submitted twice) · expirations (session, code, reservation hold) · external service errors/timeouts · concurrency (two actors editing the same record).

### 2.4 Permission cases
```
Given user A does not have permission for [action] (per the permission matrix)
When A attempts [action] through the UI or by calling directly
Then the system refuses, exposes no data outside A's permission scope, and the action leaves no side effects
```

### 2.5 State cases
```
Given the entity is in state [S1]
When event [E] occurs, caused by [an allowed actor]
Then the entity moves to [S2]
— and the forbidden pair —
Given the entity is in [final state]
When event [E] occurs
Then the system refuses, and the state remains [final state]
```

## 3. State Models — How to Build One

1. List states from the *business viewpoint* (states users/admins can see and distinguish), not technical states inside the code.
2. Determine: the start state (at creation), the end states (no way out), and abnormal states (error, stuck, awaiting intervention).
3. For every (state, event) pair: fill in the target state, or FORBIDDEN. A complete table beats a pretty diagram with missing pairs.
4. Attach to each transition: the allowed actor + the blocking condition (guard), cited by BR ID where one exists.
5. Cross-check: every state has an entry path (except the start state) and either an exit path or is an end state; an "orphan" state is a sign of a missing rule.

**Example transition table — a support request (ticket):**
| Current | Event | Actor | Target | Condition |
|---|---|---|---|---|
| NEW | accept | Support agent | IN PROGRESS | — |
| IN PROGRESS | reply to customer | Support agent | AWAITING CUSTOMER | — |
| AWAITING CUSTOMER | customer replies | Customer | IN PROGRESS | — |
| IN PROGRESS | close | Support agent | CLOSED | an outcome note exists |
| CLOSED | reopen | Customer | — FORBIDDEN — | after 7 days from closing, a new ticket must be created instead (BR-11) |

## 4. MoSCoW — Level Assignment Criteria

| Level | Criterion | The deciding question |
|---|---|---|
| Must | Without it, the feature is meaningless or violates a law/legal/safety requirement | "If we drop this, can we still release?" — No → Must |
| Should | Important, painful to lack, but a temporary workaround exists | Is there an acceptable short-term workaround? |
| Could | Nice to have; dropping it does not affect this round's goal | Does it compete for resources with Must/Should items? |
| Won't (this round) | Deliberately considered and excluded from this round | Record it explicitly to fight scope creep; Won't ≠ forgotten |

Rule: the total effort of Must items should be ≤ ~60% of the round's capacity; exceeding that is a sign prioritization is not real yet — cut or split the round.

## 5. Requirement Smells — Bad-Requirement "Smells" and How to Fix Them

| Smell | Example | Why it is bad | Fix it to |
|---|---|---|---|
| Unmeasurable adjective | "a friendly interface", "fast processing" | Cannot be verified | Replace with an observable criterion/number, or move it to an NFR with a threshold |
| Absolutes with no exceptions | "always", "never", "in all cases" | There is almost always a hidden exception | Add the specific condition/exception, or confirm it truly is absolute |
| One sentence, many behaviors | "the system saves, sends email, and updates points" | One AC holds 3 behaviors; a failure cannot be located | Split into 3 AC |
| Vague subject | "the data is carefully checked before saving" | Who/what checks it, against what? | Name the system + the concrete checking criteria |
| A number with no source | "hold the reservation for 30 minutes" | Nobody knows who decided the number or whether it may change | Attach the source: spec/Q&A/policy/`[PROPOSED — VALIDATE]` |
| AC = restating the story | The Then repeats the "I want…" clause verbatim | It adds no verification condition | The Then must state an observable state/message/figure |
| Missing negative cases | Only "when valid, then…" | Behavior when invalid is left for Dev to guess | Add a refusal AC for every input/permission/state |
| Terminology drift | The same concept goes by 3 names in one file | Teams understand it differently | Glossary + one consistent name throughout |
| A rule buried in a note | An important rule sits in a footnote/subordinate clause | Easily missed during implementation | Promote it to its own BR-xx |
| Hidden dependency | A story needs data/permissions from a system that does not exist yet | The blockage is discovered mid-flight | Record the dependency + a blocking `[TBC]` at the top of the document |

## 6. Quick Self-Review Before Submitting (10 minutes)

1. Search the file for: "reasonable", "appropriate", "fast", "easy", "good", "usually", "normally" — at each hit, either quantify it or delete it.
2. Find every number without a source — attach a source or a label.
3. Read only the Then column of every AC: is there any AC where QA could not conclude pass/fail at a glance?
4. Check that every core noun appears in the Glossary.
5. Check that every state mentioned in an AC exists in the state model (and vice versa).

## 7. Acceptance Criteria for Probabilistic (AI) Features

When a feature's output is generated by a model (chat, generation, summarization, recommendation, classification), **binary acceptance criteria do not apply**: the same input class legitimately produces varying outputs, so "Given X, Then exactly Y" is unfalsifiable. Use rate-based criteria instead.

**The golden set — owned by the BA:**
- A fixed, versioned set of representative real inputs for the feature: typical cases, boundary cases, hostile/ambiguous cases, and cases drawn from real user failures once the feature is live.
- The BA owns the set's contents and coverage; QA executes against it; nobody edits it mid-evaluation to make results look better (changes are versioned and re-run in full).

**Rate-based criteria — every AI feature's AC must state:**
- **Acceptable-output rate:** "≥ X% of golden-set outputs are graded acceptable" — X is set per feature from the cost of a wrong output, not copied from another feature.
- **ZERO critical failures:** define the critical classes explicitly for this feature (e.g. fabricated facts presented as sourced, disallowed content, leaking another user's data, an irreversible action taken without confirmation). A single critical failure fails the evaluation regardless of the overall rate.
- **A human grading rubric for "acceptable":** 3–5 concrete dimensions (correct, complete, on-format, safe, tone-appropriate — pick what applies) with a pass bar per dimension, so two graders reach the same verdict. Borderline examples are recorded in the rubric as calibration anchors.

**Re-eval triggers — the feature returns through this check when any of these change:**
- The model (provider, version, or configuration)
- The prompts / system instructions
- The retrieval corpus or connected data sources

A re-eval that misses the threshold is a failed gate, handled like any other: Failure Report, fix, full re-run of the golden set — never a threshold quietly lowered to pass.
