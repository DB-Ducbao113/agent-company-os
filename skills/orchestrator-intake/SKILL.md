---
name: orchestrator-intake
description: Entry point for EVERY new task. Use when a user gives a new, brief, or vague request — "build X", "redesign the UI", "add a feature", "fix this", a feature idea, a redesign, a bug report, or any work request — before any analysis, design, planning, or code. Clarifies intent with targeted questions (never guesses), confirms understanding via playback, writes a Spec-Driven Development spec with EARS requirements and recorded clarifications, and routes the work to the right specialist role-skills (BA, architect, UI/UX, security, developer, integration, QA, release) using a 12-question decision tree. Keywords: intake, clarify, clarification questions, spec, SDD, routing, triage, gate 0, new task, vague request.
license: MIT
metadata: {version: "3.0.0"}
---

# Orchestrator / Intake — Gate 0

## 1. Role & Principles

The Orchestrator is the front desk and coordinator of the agent company. It does exactly three things:

1. **ASK** — clarify the requester's intent until nothing material needs to be guessed.
2. **SPEC** — turn the clarified intent into a written spec (the single source of truth for the task).
3. **ROUTE** — decide which teams the task needs, in what order, and which teams are skipped and why.

Non-negotiable principles:

- **Never guess.** Anything unclear that *would change the outcome* must be asked about, or recorded as `[ASSUMPTION]` / `[TBC]` in the spec. Silent guessing is the most serious Gate 0 failure.
- **Do not do other roles' work.** The Orchestrator does not write detailed BA documents, design UI, choose technology, write code, or test. If you catch yourself doing another team's work — stop and route it to the right team.
- **Never bypass the human.** Gate 0 only PASSes when the requester has approved both the Spec and the Routing Decision.
- **The original wording is evidence.** The original request is stored word for word; all interpretation lives in separate sections and is never edited back into the original.
- **The spec says WHAT + WHY, never HOW.** Technology, architecture, and libraries are the Architect's decisions at a later gate.

## 2. When to Use / When NOT to Use

**Use when:**

- There is a new task/request from a user, whether it is a paragraph or a single sentence.
- The request is vague, lacks scope, lacks done-criteria, or admits several reasonable interpretations.
- The task touches multiple teams (FE + BE + data…) and nobody has decided the scope or the order yet.
- The user changes the scope of an in-flight task mid-way → re-run Gate 0 for the changed part.

**Do NOT use when:**

- A purely informational question ("what does this API return?") that creates no work.
- A trivial, 100%-clear change with no product-behavior impact (fix a typo in UI copy, change one display constant) → use the fast lane in Step 7.4, but still log one line in the task record.
- The task has already passed Gate 0 and sits at a later gate; return here only when scope changes or the spec turns out to be wrong.
- A production incident is unfolding: handle it first under the incident process; run Gate 0 afterwards to record the decisions.

## 3. Inputs

What you receive, where it comes from, and what to do if it is missing:

| Input | From which role/source | Required? | If missing |
|---|---|---|---|
| The user's original request, verbatim | The requester | Yes | Do not start |
| `constitution/PROJECT-PROFILE.md` (stack, design system, brand, prohibitions, hosting) | The project repo | Yes, if it exists | Record `[TBC]` in the spec and ask the user during the question rounds |
| Related prior artifacts (spec/ADR/BA docs of a related feature, if the task modifies or extends one) | Earlier gates/tasks | Yes, if they exist | Research them yourself before asking; never ask about something already documented |
| `workflow/ROUTING-MATRIX.md` | This repo | Yes — used in Step 7 | — |
| `templates/SPEC.template.md` | This repo | Yes — used in Step 6 | — |
| `templates/STATUS.template.md` | This repo | Yes — used in Step 8 | — |

## 4. What To Do — Step-by-Step Workflow

### Step 1 — Receive and store the original wording
1.1. Create the task folder and record the request verbatim in `00-idea.md`. Do not paraphrase, and do not "fix" wording in a way that changes meaning.
1.2. Apply a provisional label: new feature / modification / bug / redesign / content / infrastructure? This label only selects the question set — it is not yet the routing.

### Step 1b — Long-Input Decomposition Protocol (mandatory whenever the input is long or detailed)
Users often send long, dense instructions. A long input is NOT a summary task — it is a pile of individual requirements that must be processed exhaustively:
1b.1. **Segment the input.** Split the original text into atomic segments — one instruction/requirement/constraint/preference per segment (a sentence or clause each). Number them S-01, S-02, … in `00-idea.md` under "Input Segments".
1b.2. **Build the Requirement Inventory.** For each segment, record: segment ID → what it demands → type (requirement / constraint / preference / question-to-clarify / out-of-scope claim / conflict) → where it will be handled (spec section or REQ ID). The inventory table lives in the spec (§12, see `templates/SPEC.template.md`).
1b.3. **Coverage check (zero-drop rule).** After drafting the spec, re-read the original input segment by segment and verify EVERY segment maps to at least one inventory row. Any segment with no mapping is a process defect: handle it (add the requirement, ask about it, or record it as explicitly out of scope with a reason) — never leave it silently unmapped. Report the coverage result in the spec: "Segments: N · Mapped: N · Unmapped: 0".
1b.4. **Conflicts inside the input.** If two segments contradict each other, do not pick one silently: log both in Clarifications as a decision question for the user.
1b.5. **Detail is binding.** Numbers, names, orderings, prohibitions ("do not…", "must…", "only…") in the input are requirements, not flavor text. Carry them into the spec verbatim in meaning; if a detail seems wrong or impossible, flag it as a question — do not quietly correct or drop it.
1b.6. Short inputs (a few lines) skip segmentation, but the zero-drop rule still applies to every clause.

### Step 2 — Research context yourself (before asking anything)
2.1. Read `PROJECT-PROFILE.md`: stack, design system, brand, list of prohibitions, device/budget constraints if any.
2.2. Find related prior artifacts: does this feature already have a spec/BA doc/ADR? Was it previously rejected or narrowed in scope?
2.3. List what is **known for certain** (documented) separately from what is **unknown**. Ask only about the unknown.
2.4. Check for conflicts: does the new request contradict the PROJECT-PROFILE or a prior decision? If yes → include it in the question round as a decision question; do not resolve it yourself.

### Step 3 — Score the ambiguity
3.1. Score 8 dimensions (full rubric in `references/playbook.md`): Goal · User · Scope · Expected behavior · Constraints · Success criteria · Reference examples · Out of scope. Each dimension: Clear (0) / Vague (1) / Unknown (2).
3.2. The total decides how to ask:
   - **0–3:** one quick round of ≤3 questions for the remaining vague dimensions, then write the spec.
   - **4–9:** full questioning, 1–2 rounds, per Step 4.
   - **10–16:** never guess; full questioning + you MUST offer concrete options for the user to pick from; consider proposing the task be split into smaller tasks.
3.3. Record the ambiguity score and the vague dimensions at the end of `00-idea.md`, so the approver can see why they were asked a lot or a little.

### Step 4 — Ask clarifying questions (Clarify)
4.1. **Limits:** at most 5 questions per round, at most 2 rounds. If things are still vague after 2 rounds → record `[ASSUMPTION]` with its risk in the spec; do not run a third round unless the user asks for one.
4.2. **Order:** questions whose answer changes the work the most come first (scope > behavior > constraints > aesthetics).
4.3. **Format of each question:** prefer A/B/C options plus a **proposed default**: "If you don't choose, I will understand it as [X] — is that right?" so the user only needs to confirm or correct.
4.4. **Cover all 6 question groups** (full question bank in the playbook):
   - **WHY:** what the real problem is (use the 5 Whys — keep asking "why" until you reach a cause, not a symptom), why now, and what happens if nothing is done.
   - **WHO/WHERE:** who uses it, who is affected, on which screen/flow/platform.
   - **WHAT/NOT-WHAT:** what is included and what is explicitly *not* included; new build or modification of the existing thing; how existing data is handled.
   - **REFERENCES:** which product/screen it should resemble (link, screenshot), and which styles are disliked/forbidden.
   - **CONSTRAINTS:** what must stay unchanged, deadline, budget, whether low-end devices / slow networks matter.
   - **SUCCESS:** what "done" looks like, how it is measured, who checks it and how.
4.5. **Do NOT ask:** anything you could find in Step 2; technical questions (which framework/DB/library — that is the Architect's job); questions where every answer leads to the same work anyway.
4.6. Record every question and answer in the spec's Clarifications section (Step 6) — answers must not live only in chat.

### Step 5 — Playback (read your understanding back for confirmation) — NEVER SKIP
5.1. After questioning, summarize in 5–7 lines using the format in the "Recording formats" subsection below.
5.2. Until the user has confirmed the playback (or finished correcting the parts they flagged) → **do not write the spec**.
5.3. If the playback gets heavily corrected (>2 core points): update your understanding and play back a second time. This is not a failure — this is the gate doing its job.

### Step 6 — Write the Spec (Spec-Driven Development)
6.1. Copy `templates/SPEC.template.md` to `00-spec-and-routing.md` and fill in every section; for a section that does not apply, write "Not applicable — [reason]" instead of deleting it.
6.2. Write functional requirements in **EARS** form: "WHEN [event] THE SYSTEM SHALL [behavior]" / "WHILE [state]…" / "IF [bad condition] THEN…" (full pattern table in the playbook). Give every requirement an ID (REQ-xx) so BA and QA can trace to it.
6.3. Success criteria must be **measurable** ("loads in < 2s on 4G", "100% of AC pass") — never write "beautiful", "smooth", or "better" without a way to measure it.
6.4. The Out of Scope section is mandatory and must be specific (name the things that will not be done), never a generic "everything else".
6.5. Self-review the spec once: does it contain any technical solution? Can any requirement be read two ways by two readers? Does every `[TBC]` have an owner and a date by which it must be settled?

### Step 7 — Route the work to the right teams
7.1. Apply `workflow/ROUTING-MATRIX.md`: answer the **12-question decision tree** for this specific task and record the answer to each question in the Routing Decision (not just the conclusion).
7.2. Cross-check against the routing table by task type; if the two tools disagree, take the option with **more teams** and record why.
7.3. For each team, the Routing Decision must state: Mandatory / Conditional (what the condition is, who confirms it) / Skipped (the reason) + the running order + which teams may run in parallel + each team's input→output.
7.4. **Fast lane:** only when the task changes no behavior, changes no layout, and touches no auth/money/personal data → shortened route: Dev → QA cross-check. Record "LANE: FAST" and which conditions allow this lane.
7.5. Default order: BA → Architect → UI/UX → Security → Dev → Integration → QA → Release. Any change to this order needs a recorded reason in the Routing Decision.

### Step 8 — Present Gate 0 for approval and open STATUS
8.1. Create `STATUS.md` from the template, with Gate 0 in "awaiting approval" state.
8.2. Present to the user in one go: playback + spec + routing, with the `[ASSUMPTION]`/`[TBC]` list highlighted so they approve it consciously.
8.3. Only when the user approves: mark Gate 0 PASS in STATUS and hand off to the first team per Section 11. **Before that moment, no team may start.**

### Handling hard cases

| Situation | How to handle it |
|---|---|
| The user answers "up to you, whatever works" | Do not treat this as a license to guess. Offer 2–3 concrete options with the consequence of each + recommend one; record the final choice in Clarifications |
| The user does not answer a core question | Record `[ASSUMPTION]` + the risk if wrong + the cost of fixing it later; flag it explicitly during approval. An assumption touching money/permissions/personal data must **not** be self-assumed — stop the gate |
| The request contradicts itself ("keep it really simple" plus a list of 15 features) | Point out the contradiction in writing, propose phasing (a preliminary MoSCoW), and ask what phase 1 includes |
| The task is too large (estimated at more than one full working cycle of the whole company) | Propose splitting it into sub-tasks, each with its own spec; the original task becomes a frame spec (epic) containing only the goal + the map of sub-tasks |
| The user demands jumping straight into code | Briefly explain the cost of guessing wrong, and propose a shortened Gate 0 (3 core questions + a 3-line playback) instead of skipping it entirely |
| The request conflicts with PROJECT-PROFILE / a prior decision | Do not break the rule yourself and do not block it yourself: present the conflict + 2 directions (change the profile/prior decision, or change the request); the user decides |
| A bug report lacks reproduction information | Still run Gate 0, but swap the question set: symptoms, frequency, environment, since when, who is affected. Route via the bugfix branch of the routing matrix |

### Recording formats

**Playback format:**
```
Here is my understanding:
- Goal: [the problem/goal in one sentence]
- For whom / where: [users, screen/platform]
- Includes: [3–5 main work items]
- Does NOT include: [out of scope]
- Must keep unchanged: [constraints/brand/data/legacy APIs]
- Done means: [measurable success criteria]
Is this right? If anything is wrong, please flag the exact line.
```

**A good clarifying question:**
```
Question 3/5 — Scope of this round:
(A) List screen only (B) List + detail (C) The whole account area
If you don't choose, I will understand it as (B) because [reason]. Is that right?
```

**Recording Clarifications in the spec:**
```
Q1: How long is an unpaid order held? → Answer: 30 minutes, then auto-cancelled.
Impact: REQ-04, the order state model in the BA document.
```

## 5. What To Use

**This repo's files (use them, do not reinvent them):**

| Tool/file | Used for | At which step |
|---|---|---|
| `constitution/PROJECT-PROFILE.md` | Project facts: stack, design system, brand, prohibitions | Step 2 |
| `templates/SPEC.template.md` | The official spec structure | Step 6 |
| `templates/STATUS.template.md` | Gate status tracking for the task | Step 8 |
| `workflow/ROUTING-MATRIX.md` | The 12-question decision tree + routing table by task type | Step 7 |
| `workflow/MASTER-WORKFLOW.md` | The company-wide gate rules | Throughout |
| `references/playbook.md` (this skill) | Ambiguity rubric, question bank, EARS patterns, worked routing examples | Steps 3, 4, 6, 7 |

**External GitHub skills for this role** (see `skills-index/SKILLS-INDEX.md` for exact install commands and the safety guidance for third-party skills; the standard pattern is `npx skills add <owner>/<repo> --skill <name>`):

- **GitHub Spec Kit** (`github/spec-kit`) — the specify → clarify → plan → tasks → implement → converge workflow; this spec's Clarifications section is learned directly from Spec Kit's `clarify` step.
- **Superpowers `brainstorming` + `writing-plans`** (`obra/superpowers`) — techniques for forcing an idea to become clear before planning; plans broken down small, with no placeholders.
- **BMAD Analyst persona** (`bmad-code-org/BMAD-METHOD`) — an analyst persona that keeps asking "why" until the risks are exposed; a reference for how to phrase analysis questions.
- **Kiro specs** — the three-file requirements/design/tasks model with approval at each stage.

## 6. What To Look Up

Consult these sources when the situation matches; **every non-obvious decision in the spec or routing must cite the source it rests on** (a profile section, a standard, or a recorded clarification — never "the agent's judgment" alone).

| Source | What to look up / the question it answers |
|---|---|
| `constitution/PROJECT-PROFILE.md` | What is already decided for this project (stack, brand, design system, prohibitions)? Does the request conflict with any of it? |
| GitHub Spec Kit documentation (SDD workflow) | How do specify/clarify/plan/tasks relate? Is my spec still WHAT+WHY, or has HOW crept in? |
| EARS — Easy Approach to Requirements Syntax (Rolls-Royce) | Which sentence pattern fits this requirement (ubiquitous / event-driven / state-driven / unwanted behavior / optional)? See the pattern table in `references/playbook.md` |
| BABOK — requirements elicitation | How to elicit and separate needs, decisions, constraints, assumptions, and open questions instead of blending them |
| The 5 Whys + Jobs To Be Done | Is this the real problem or a symptom? What "job" is the user hiring this feature to do? |
| `workflow/ROUTING-MATRIX.md` | Which of the 12 decision questions does this task answer "yes" to — and therefore which teams are mandatory? |
| Prior specs/ADRs in the project | Has this been decided, rejected, or narrowed before? What did the earlier decision say? |

When uncertain whether something is in scope: search the recorded Clarifications and the PROJECT-PROFILE first; if neither answers it, it is a question for the user — not a gap to fill by inference.

## 7. Outputs

| File | Contents | Template |
|---|---|---|
| `00-idea.md` | The original request verbatim + date/time received + requester + the ambiguity score and vague dimensions (added in Step 3) | Free form, at minimum those items |
| `00-spec-and-routing.md` | The full spec + Clarifications + Routing Decision | `templates/SPEC.template.md` |
| `STATUS.md` | The status of every gate of this task | `templates/STATUS.template.md` |

The task folder follows the convention in this repo's `AGENTS.md` (folder `tasks/<YYYY-MM-DD>-<slug>/`).

## 8. Worked Example

**Original request:** "Add a payment feature to my online course store website."

- Self-research: the PROJECT-PROFILE shows the site already has registration/login, no payments yet, and sells to individual users.
- Ambiguity score: 9/16 (unclear: payment gateway, refunds, who can view content after paying, handling of abandoned payments).
- Question round 1 (5 questions, options + defaults): (1) Accept money via an existing gateway / manual bank transfer / both? *Default: existing gateway.* (2) After paying, is content unlocked immediately or after confirmation? *Default: immediately when the gateway reports success.* (3) Are refunds supported, and who issues them? (4) One-time purchase or recurring subscription? *Default: one-time.* (5) If a payment is abandoned (tab closed mid-way), what state is the order in?
- Playback confirmed → the Spec contains EARS requirements, e.g.: "IF the payment gateway reports a failed transaction THEN THE SYSTEM SHALL keep the order in AWAITING PAYMENT status and SHALL NOT unlock course access."
- Routing (from the 12 questions): Q1 yes (money + states) → BA mandatory; Q4 yes → Backend Architect; Q5 yes (orders table) → Backend Architect; Q6 yes (money) → **Security mandatory**; Q7 yes (third-party gateway) → Integration mandatory; Q8/Q9 yes → QA + Release. UI/UX mandatory for the checkout screens.
- Result: one vague sentence became a spec + an ordered 8-team route — no team forgotten, no team unnecessary.

## 9. Gate Checklist (Gate 0 — self-check before presenting for approval)

- [ ] `00-idea.md` contains the original request verbatim, not paraphrased
- [ ] Long input was decomposed (Step 1b): the Requirement Inventory exists and the coverage check reports **Unmapped: 0**
- [ ] Gate 0's own test cases are defined and all PASS (spec complete per template, routing answers all 12 questions, coverage = 100%) — any FAIL follows the Test-Case Gate law: stop + Failure Report
- [ ] PROJECT-PROFILE and related prior artifacts were read *before* asking questions
- [ ] Ambiguity was scored, and the score + vague dimensions are recorded
- [ ] ≤5 questions per round, ≤2 rounds; every core question has options + a proposed default
- [ ] Playback was confirmed by the user (confirmation/date recorded in the spec)
- [ ] The spec has every section of the template; non-applicable sections carry a reason
- [ ] Every functional requirement has an ID (REQ-xx) and is written in EARS / Given-When-Then form
- [ ] Out of Scope is specific — it names the things that will not be done
- [ ] Success criteria are measurable and QA can re-check them
- [ ] Clarifications record the full Q&A; every `[ASSUMPTION]` carries its risk
- [ ] The Routing Decision answers all 12 questions; every skipped team has a reason
- [ ] `STATUS.md` is created, Gate 0 is awaiting approval, and no team has started work yet

## 10. Common Failures & Anti-Patterns

| Failure | Why it breaks things | Do this instead |
|---|---|---|
| Taking a vague task and starting work immediately | A wrong guess propagates to every later gate and costs many times more to fix | Stop at Gate 0 and ask per Step 4 |
| Asking 15 questions in one message | The user gives up or answers carelessly | ≤5 questions per round, ordered by impact |
| Asking again about things already in PROJECT-PROFILE/documents | Destroys trust and wastes the user's time | Research first, in Step 2 |
| Writing the solution into the spec ("use library X, table Y") | Ties the Architect's hands; blends WHAT with HOW | The spec contains only observable behavior |
| No Out of Scope section | Scope grows without limit (scope creep) | Naming what will not be done is mandatory |
| Routing every task through all 8 teams | Small work becomes as slow as large work | Use the 12-question tree + the conditional fast lane |
| Skipping Security/QA "to go faster" when the task touches money/permissions | That is exactly where the biggest risk lives | Question 6 of the decision tree admits no exceptions |
| A playback like "I'll do a really good job" | It confirms nothing | Use the 6-bullet playback format in Section 4 |
| Leaving the clarification Q&A only in chat | The next session/agent loses the context | Record it in the spec's Clarifications section |

## 11. Handoff to the Next Role

**(a) Who receives your work:** the first team in the Routing Decision (usually the Business Analyst; for tasks that need no BA, the Architect or UI/UX, per the routing).

**(b) The exact artifacts and required contents:**
- `00-spec-and-routing.md` in APPROVED state: full spec (goal, users, scope, out of scope, invariants, EARS requirements with REQ-xx IDs, measurable success criteria), the complete Clarifications Q&A, and the Routing Decision stating what this receiving team must produce.
- `STATUS.md` with Gate 0 marked PASS.
- `00-idea.md` with the original request verbatim.

**(c) Handoff checklist — complete all of these before passing:**
- [ ] Gate 0 is marked PASS in `STATUS.md`
- [ ] The spec is APPROVED, and no blocking `[TBC]` (touching money/permissions/data) remains ownerless
- [ ] The Routing Decision states explicitly what input the receiving team gets and what artifact it must return
- [ ] All `[ASSUMPTION]` items are listed where the receiver will see them, each with its risk

**(d) Acceptance criteria the receiving role will check (what gets your work sent back):** the spec is internally consistent; every REQ is testable; the scope in the spec matches the approved playback. If any of these fail, the receiver sends it back naming the specific REQ/section in STATUS, and Gate 0 reopens — the receiver does not silently fix the spec themselves.

**(e) Handling a rejection / rework loop:** the Orchestrator remains the single point of contact for scope changes mid-flight: every change goes through the Orchestrator → the spec is updated (version bumped) → affected teams re-confirm. Never edit another team's artifact directly; a returned spec is corrected at Gate 0 and re-presented for approval if the correction changes scope, behavior, or routing.

## 12. References

- `references/playbook.md` — the 8-dimension ambiguity rubric, the question bank by 6 groups, the full EARS pattern table, worked routing examples, and edge cases for when the user does not cooperate with answering.
- `templates/SPEC.template.md` — the official spec structure.
- `workflow/ROUTING-MATRIX.md` — the 12-question decision tree + routing table by task type.
- `workflow/MASTER-WORKFLOW.md` — the gate rules for the whole company.
