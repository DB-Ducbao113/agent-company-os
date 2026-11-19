# Elicitation Deep Dive — Advanced Techniques for Gate 0

> Companion to `references/playbook.md` (the rubric, question bank, and EARS patterns).
> This file is the advanced toolkit: use it when the standard question round leaves ambiguity behind,
> when stakeholders disagree, or when the user's words are quality adjectives instead of requirements.

## 1. The 5 Whys — done properly

The 5 Whys fails when each "why" is answered with a restatement. Rules:
- Each answer must name a **cause**, not a symptom and not a solution. If the answer is a solution ("because we need a dashboard"), ask "why do you need that?" — you are still at the symptom layer.
- Stop when you reach a cause the user can **act on or measure** (a lost sale, a manual step, a compliance risk), or when the answer becomes "because that's how it is" twice in a row — that layer is a constraint, record it as one.
- Branch, don't tunnel: at each level, ask "and what else causes that?" once. Real problems usually have 2–3 root causes; a single chain hides them.
- Write the chain into `00-idea.md`. The final cause becomes the spec's Problem statement; every intermediate layer is evidence for prioritization.

**Worked chain** — request: "Add an export button to the reports page."
| Step | Answer | Layer |
|---|---|---|
| Why export? | "The accountant asks for the numbers every month." | symptom |
| Why does she ask you? | "She can't see the reports herself." | cause candidate |
| Why can't she? | "Her account role has no report permission." | cause candidate |
| Why not? | "When roles were set up, finance was never added." | **root cause (process)** |
| Why was she never added? | "Nobody owns role administration." | root cause (ownership) |

Outcome: the real task is a permission change + a role-administration owner — a 1-hour fix, not a reporting feature. The export button is still recorded (it may be wanted for other reasons), but the spec's Problem section now names the root cause, and routing changes completely.

## 2. Laddering — feature → consequence → value

Users request features; specs need values. Ladder upward with three prompts, in order:
1. "What will that let you (or the user) **do** that you can't do today?" → consequence
2. "Why does that matter — what goes wrong, or what is lost, without it?" → impact
3. "How would you know it worked — what number or event would change?" → measurable value

Stop laddering a branch when the answer repeats, becomes abstract ("be more professional"), or the user says "that's just it". Record the top rung as the requirement's **rationale** — BA and QA use it to judge edge cases the literal wording doesn't cover ("the point is the accountant stops waiting" decides questions the button spec never mentions).

**Micro-example:** "Add dark mode" → consequence: "staff use the app on night shifts" → impact: "the bright screen wakes patients / causes complaints" → value: "zero brightness complaints in night-shift feedback". The spec now protects the *value* (readability at night) — which also admits alternatives (a dimmed night theme) the feature request would have excluded.

## 3. Scenario and day-in-the-life walkthroughs

When behavior is still vague after direct questions, stop asking abstractly and walk a concrete story:
- Pick the **most typical actor** and one specific day: "It's Tuesday 9:05, a customer has just paid. Walk me through exactly what happens next — who sees what, in what order?"
- Narrate it back step by step and stop at every verb: "You said the manager 'checks' the order — checks *what*, against *what*, and what happens if it fails?"
- Then run two variant passes over the same story: the **bad day** (payment fails, user abandons halfway, two people act at once) and the **busy day** (100× volume). Most missing requirements live in these two passes, not the happy path.
- Every step of the walkthrough maps to one or more EARS requirements; any step you cannot narrate concretely is an unresolved `[TBC]` with an owner.

Use scenarios when: the task involves a workflow, multiple actors, timing, or money. Skip them for pure content or cosmetic tasks — they cost the user real time.

## 4. Eliciting non-functional requirements (NFR catalog)

Users almost never volunteer NFRs; unasked, they become late-stage surprises. Ask one question per category that applies — do not read the whole catalog at the user.

| Category | The question to ask | What a usable answer looks like |
|---|---|---|
| Performance | "What is the slowest acceptable response for the main action, on a normal connection?" | a number + condition ("list opens < 2 s on 4G") |
| Scale | "How many users / records / orders at launch, and in a year if it goes well?" | two numbers (now, growth) |
| Concurrency | "What happens when two people do this at the same time?" | rule: block, queue, last-wins, or merge |
| Availability | "If this is down for an hour, what breaks? When is downtime acceptable?" | criticality tier + maintenance window |
| Security posture | "Who must NOT be able to see or do this? Is any of it personal, financial, or health data?" | named exclusions + data class |
| Devices & platforms | "Which devices/browsers/versions must it work on — including the oldest?" | explicit minimum (e.g. "Android 10+, Chrome last 2") |
| Weak environments | "Will users be on slow networks or low-end devices? Must anything work offline?" | yes/no + which flows degrade how |
| Accessibility | "Must it meet an accessibility standard? Which users with disabilities are expected?" | target (e.g. WCAG AA) or explicit non-goal |
| Internationalization | "Which languages, currencies, time zones, and date formats — now and planned?" | list + whether design must leave room |
| Data retention | "How long must this data be kept? Who can delete it, and must deletion be provable?" | retention period + deletion rule |
| Auditability | "If something goes wrong, must we be able to prove who did what, when?" | yes/no → audit-log requirement |
| Cost ceiling | "Is there a per-user or monthly infrastructure cost this must stay under?" | a budget number or "not a constraint" |

Record each answered NFR as a numbered NFR-xx in the spec with its measurement. A category the user explicitly waves off is recorded as "not a constraint — confirmed", which protects later roles from gold-plating it.

## 5. Stakeholder conflict resolution protocol

When two stakeholders (or the user vs. the PROJECT-PROFILE) want incompatible things:
1. **Name the conflict precisely** — one sentence each side, in their own terms. Most "conflicts" dissolve here: the sides often want different *things*, not the same thing differently.
2. **Classify it:** (a) factual disagreement → settle with evidence (data, a test, the source document); (b) priority disagreement → it is a decision, not a fact — go to step 3; (c) misunderstanding → restate both positions until each side confirms the other's summary.
3. **Escalate as a decision question**, never resolve it yourself: present both options with the cost/consequence of each and your recommendation labeled as a recommendation. The user (or the named decision owner) decides.
4. **Record the decision and the loser**: the decision, who made it, the date, and the rejected option with its reason go into the spec's Clarifications/decision log. The rejected side is not deleted — it is the first thing needed if the decision is revisited.
5. If no decision is possible now: mark the requirement `[TBC — blocked on decision D-n]`, route around it if the rest of the work is independent, and say explicitly what cannot start.

Never average two conflicting requirements into a compromise nobody asked for ("show 15 records" from "10" vs "all") — a merged number satisfies neither side and hides the disagreement from the approver.

## 6. Scope-splitting heuristics

Split the task before routing when **any** of these is true:
- The spec needs more than ~12 functional requirements, or the playback takes more than ~7 lines to state.
- Two parts have different users, different success criteria, or different deadlines.
- One part is well understood and another is exploratory — the exploratory part will churn the whole spec.
- A part touches money/permissions/data migration while the rest is cosmetic (the risky part deserves its own gates and pace).
- The user says "and also…" three or more times — each "also" is a candidate split.

**How to sequence the parts:**
1. Split along **value seams**: each part must be independently usable or independently verifiable. Never split by technical layer alone ("backend first, UI later") as separate user-facing tasks — split by user-visible outcome, and let the Architect sequence layers inside each part.
2. Order by: (a) the part that unblocks the most other parts, (b) the riskiest assumption first if a cheap part can test it, (c) the user's stated deadline order.
3. Each part gets its own task folder and spec; the original `00-idea.md` stays as the parent record linking them, with the split rationale.
4. State what is deferred, not dropped: deferred parts are listed in the parent's Out of Scope with "deferred to task <slug>", never silently vanished.

## 7. Decision log discipline

Every clarification answer that *chooses* between alternatives is a decision. The log (in the spec's Clarifications section or a `DECISIONS.md` for long tasks) has one row per decision:

| Field | Content |
|---|---|
| ID | D-01, D-02… |
| Decision | one sentence, active voice ("Cancel is allowed up to 4 hours before") |
| Alternatives rejected | each with the one-line reason |
| Decided by / date | the user or named owner — never "the team" |
| Affects | REQ/NFR ids it constrains |
| Reversible? | cheap / costly / irreversible — irreversible decisions get extra scrutiny before proceeding |

Rules: a decision that later changes is **superseded**, not edited — add a new row and mark the old one "superseded by D-n". If you cannot find who decided something, treat it as undecided and ask. Roles downstream cite decision IDs when a requirement looks arbitrary ("per D-03") instead of re-litigating it.

## 8. "Just make it good" — operationalizing vague quality words

Quality adjectives are placeholders for criteria the user has not articulated yet. Never let one into a spec untranslated. Use this table to convert, then confirm the numbers with the user (propose the default, let them correct it):

| User says | Ask / propose | Measurable translation (examples) |
|---|---|---|
| "fast" | "Fast for which action, on what connection?" | "Main list renders < 2 s on 4G; actions respond < 300 ms or show progress" |
| "simple" | "Simple for whom — first-time or daily users?" | "Core task completable in ≤ 3 steps; a new user succeeds unaided in testing" |
| "modern" | "Modern like which product?" (demand a reference) | "Matches the patterns of <named reference>: <2–3 concrete traits>" — no reference, no requirement |
| "secure" | "Secure against whom, protecting what?" | "Passes Gate 4's mandatory tests: wrong-role, IDOR, expired-token cases all rejected" |
| "reliable" | "What failure hurts most, and how often is acceptable?" | "Error rate < 0.1% on the main flow; failed submissions recoverable without data loss" |
| "user-friendly" | "Which users struggled, at which step?" | "Task success ≥ 90% in a 5-person walkthrough; zero required training materials" |
| "scalable" | "Scale to what number, by when?" | "Holds targets at <N> concurrent users / <M> records, verified by load check" |
| "clean / polished" | "Show me two screens — one that feels clean, one that doesn't." | Convert the contrast into design rules (spacing, hierarchy, state coverage) for Gate 3 |
| "like <product X>" | "Which parts of X — look, flow, or behavior?" | Name the borrowed trait per screen; record what is explicitly NOT copied |

If the user cannot or will not quantify a quality word after one attempt with a proposed default, record it as a **direction** (guides judgment, not a testable criterion) and say so in the spec — QA must never be handed an unmeasurable success criterion disguised as one.

## 9. Estimating the ambiguity that remains after 2 rounds

After the second clarification round, some dimensions stay vague. Do not pretend otherwise — quantify and price the residue:
1. Re-score the 8 ambiguity dimensions. For each dimension still at Vague (1) or Unknown (2), write: what is unknown, the `[ASSUMPTION]` you are forced to make, and its **blast radius** — what gets reworked if the assumption is wrong (one screen? the data model? the whole flow?).
2. Classify each remaining assumption: **cheap to reverse** (proceed, note it), **costly to reverse** (proceed only with the user's explicit acceptance of the rework risk), **blocking** (the work cannot responsibly start — say so, name the one question that unblocks it, and stop).
3. State the summary in the spec and in STATUS.md: "Residual ambiguity: 2 assumptions — 1 cheap, 1 costly (accepted by user on <date>), 0 blocking."
4. Set a **revisit trigger** for each costly assumption: the earliest moment reality will test it (first prototype review, first real data, contract signing) — and which gate owns re-checking it.

An intake that ends with named, priced, owned ambiguity has done its job. An intake that ends claiming zero ambiguity after a vague request has failed silently.

## 10. Mining existing artifacts before you ask

Questions are expensive; documents are free. Before any clarification round, mine what already exists — every fact found here is a question you do not ask (the playbook's Step 2 discipline, expanded):

| Source | What to extract | Trap to avoid |
|---|---|---|
| PROJECT-PROFILE | stack, design system, invariants, review format | treating `[TBC]` fields as facts — they are open questions wearing a uniform |
| Prior task folders (`tasks/`) | decisions (D-ids), rejected options, residual assumptions | assuming a past decision still holds after a scope or stakeholder change — confirm, don't inherit blindly |
| Existing product / codebase | what the current behavior actually is (screens, states, limits) | documenting the current behavior as the *requirement* — today’s behavior may be the bug being reported |
| Analytics / support tickets / reviews | where users actually struggle, in their words | loud-minority bias: one angry ticket is a hypothesis, not a requirement |
| Competitor / reference products the user names | the concrete traits behind "make it like X" | copying surface look while missing the behavior the user actually valued |

Rule: anything mined is labeled by source in `00-idea.md` ("per PROJECT-PROFILE §4", "per task 2026-…/D-03"). If two sources disagree, that disagreement becomes a clarification question — sources never silently outrank each other except the PROJECT-PROFILE, which wins by design (AGENTS.md rule 3).

## 11. Running the round — sequencing and recovery

**Sequencing inside one round.** Order questions so early answers can retire later questions: scope before behavior, behavior before constraints, constraints before aesthetics. If the user's answer to Q1 makes Q4 moot, drop Q4 and say so ("that settles Q4 as well") — visible adaptivity is what makes the round feel like a conversation instead of a form.

**Recovery moves when the round goes wrong:**
- *User answers a different question than the one asked* → their answer is data (it is what they care about); record it, then re-ask the original once, shorter. Twice deflected = the question is probably unanswerable by this person — route it to its real owner or log it as residual ambiguity.
- *User contradicts an earlier answer* → do not pick the newer one silently; surface the pair ("earlier you said X, now Y — which governs?") and log both in the decision log, the loser marked superseded.
- *User gets impatient* ("just start") → offer the explicit trade: "I can start now on these 3 recorded assumptions; if any is wrong, the rework lands at Gate N and costs roughly X." If they accept, the assumptions and their acceptance go into the spec verbatim. Impatience is a decision, and decisions get logged.
- *User delegates back* ("you decide") → decide, but as a *proposed default with a reversal cost stated*, and log it as decided-by-agent-with-user-delegation. "You decide" transfers the pen, not the accountability for recording it.

**Closing the round.** End every round by restating: questions asked, answers received, questions deliberately not asked (and why — found in artifacts, or deferred), and what happens next (playback). This closing summary is the audit trail that the clarification duty was actually discharged — and it is what the WT-01-style review of your own gate will look for.
