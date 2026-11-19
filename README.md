# Agent Company OS

> **Turn one AI coding agent into a disciplined software company.**
> One vague request in → clarifying questions → a written spec → the right specialist
> roles in the right order → gated, verifiable output. For **any project, any stack, any user**.

## The problem this repo solves

Vibe coding fails for three reasons — none of them is "the agent is bad":
1. The user describes things briefly/vaguely → the agent **guesses** → wrong from the start.
2. One agent does everything → nobody checks anybody, and you can't tell which stage a defect came from.
3. There is no definition of "done" → the agent says it's finished, and the result doesn't work.

Agent Company OS fixes all three with the structure of a real company, shrunk for one human + AI agents.

## The core idea — every role answers four questions

Whenever an agent reaches a role, that role's skill tells it, in a fixed structure:

| Question | Where it lives in each SKILL.md |
|---|---|
| **What do I do?** | The step-by-step workflow section |
| **What do I use?** | Tools, this repo's templates, and the external GitHub skills assigned to the role |
| **What do I look up?** | The standards/sources to consult, and exactly what to search for when uncertain |
| **What do I hand off?** | The output artifact, its required contents, and the acceptance criteria the next role will check |

Work circulates **only** through these artifacts. The full map is in [`workflow/ROLE-CHAIN.md`](workflow/ROLE-CHAIN.md).

## How a task flows

```
Raw task (usually vague)
  → GATE 0  Orchestrator: clarify → playback → SPEC (Spec-Driven Development) → ROUTING
  → GATE 1  BA: user stories + acceptance criteria
  → GATE 2  Architect: C4 + ADRs + API contract
  → GATE 3  UI/UX: research real products → prototype (if the task has UI)
  → GATE 4  Security: threat model + permissions (if it touches auth/money/data)
  → GATE 5  Developer + Code Review (two separate roles)
  → GATE 6  Integration: real joining, contract verification
  → GATE 7  QA: test cases traced back to acceptance criteria
  → GATE 8  Release: changelog, version, rollback plan — the human approves last
```
Not every task runs all 8 gates — the Orchestrator uses [`workflow/ROUTING-MATRIX.md`](workflow/ROUTING-MATRIX.md)
(a 12-question decision tree) to pick the right roles, enough roles, and record why skipped roles were skipped.

**Two rules keep the flow honest:**
- **The Test-Case Gate:** every gate defines its test cases up front and runs all of them. The next gate starts
  only at **100% PASS**. A single FAIL stops the workflow and triggers a written **Failure Report** to you —
  what failed, expected vs. actual, evidence, suspected cause, owning role, proposed fix — before anything else continues.
- **Exhaustive input processing:** your instructions are often long and detailed, so Gate 0 decomposes them
  segment by segment into a Requirement Inventory with a zero-drop coverage check — every clause becomes a
  requirement, a question, or an explicit out-of-scope note. Nothing is summarized away.

**How do you know it works?** [`docs/TESTING-GUIDE.md`](docs/TESTING-GUIDE.md) gives you a 10-case test suite
(WT-01…WT-10) with exact prompts to paste into your agent, the expected behavior, and PASS/FAIL signs —
covering clarification, long-input decomposition, routing, pressure to skip gates, failure handling, and more.

## Installation — install it, then invoke it like a real skill

This repo follows the **Agent Skills** standard (agentskills.io): each skill is a folder `skills/<name>/SKILL.md`
(plus a deep `references/playbook.md`). An agent loads each skill's `name` + `description` at startup
(~100 tokens/skill), reads the full text when a task matches, and opens the playbook when doing the real work.
The canonical repo lives under `DB-Ducbao113` — if you fork it, substitute your own username.

### A. Claude Code (plugin marketplace — the cleanest way)
```
/plugin marketplace add DB-Ducbao113/agent-company-os
/plugin install agent-company-os@agent-company-os
```
`.claude-plugin/marketplace.json` ships 3 plugins: `agent-company-os` (all 10 skills),
`agent-company-front` (Gates 0–3 only), `agent-company-delivery` (Gates 4–8 only).

### B. Skills CLI (Claude Code / Codex / Cursor / Copilot / Gemini CLI…)
```bash
# Install the whole set
npx skills add https://github.com/DB-Ducbao113/agent-company-os
# Or install a single skill
npx skills add https://github.com/DB-Ducbao113/agent-company-os --skill ui-ux-design
npx skills add https://github.com/DB-Ducbao113/agent-company-os --skill orchestrator-intake
```

### C. Manual copy into a project
| Tool | Destination folder |
|---|---|
| Claude Code | `.claude/skills/` |
| Codex / Cursor / Agent-Skills-standard agents | `.agents/skills/` |
| GitHub Copilot | `.github/skills/` |

### D. Claude.ai (chat + skill upload)
Zip **each skill folder** (`skills/<name>/`) separately and upload it in Claude.ai's Skills section — each becomes an invocable skill in chat.

### E. Any chat AI (Muse / ChatGPT / Gemini…) — no installation
See the [`chat/`](chat/CHAT-GUIDE.md) folder: paste the repo's GitHub link + the ready-made starter prompt in
[`chat/START-PROMPTS.md`](chat/START-PROMPTS.md). If the chat reads links poorly, use the single-file edition
[`dist/FULL-CONTEXT.md`](dist/FULL-CONTEXT.md) (raw link or file attachment) — one file contains the whole system.
Note: chat mode needs a public repo or attached files, and artifacts must be saved as files on your side (see CHAT-GUIDE).

### How to invoke a skill after installing
- **Automatically:** just assign work normally ("redesign the settings screen", "security-check the payment flow") — the agent matches the description and activates the right skill.
- **By name:** "Use the `orchestrator-intake` skill for this task: …" / "Apply the `ui-ux-design` skill to review this screen."

### Option 0 — No install, just have the agent read the repo
```
Read this repo before doing anything: <repo link or folder path>
Read AGENTS.md at the root and follow it. My task is: "<your raw task>"
```
The agent will read `AGENTS.md` → run `orchestrator-intake` → clarify with you → write the spec → route to the right roles.

### Adding curated external skills
Each role also lists battle-tested external GitHub skills (UI/UX Pro Max, Impeccable, Spec Kit, BMAD,
Superpowers, Trail of Bits, Sentry…) with install commands in [`skills-index/SKILLS-INDEX.md`](skills-index/SKILLS-INDEX.md).
**Read an external skill's SKILL.md before installing it** — a skill runs with your agent's privileges; never install blind.

## First step for a new project
Fill in [`constitution/PROJECT-PROFILE.template.md`](constitution/PROJECT-PROFILE.template.md) and save it as
`constitution/PROJECT-PROFILE.md`: project name, stack, design system, brand, invariants. This is the **only file
that contains project-specific facts** — everything else in the repo is universal. Same mechanism as Impeccable's
`PRODUCT.md` and Spec Kit's constitution: the project's durable truth lives in one place, and the agent reads it before every task.

## Repository structure

```
AGENTS.md                  ← Entry point: every agent reads this FIRST (bootstrap rules)
CLAUDE.md                  ← Points Claude Code users to AGENTS.md
.claude-plugin/            ← marketplace.json — install via /plugin marketplace add
constitution/              ← PROJECT-PROFILE (fill in once per project) + shared principles
skills/                    ← 10 role skills in Agent Skills format, each with:
  <skill-name>/SKILL.md       the detailed skill: workflow, tools, lookups, handoff
  <skill-name>/references/    playbook.md — deep reference (read on demand)
  orchestrator-intake/  business-analyst/  solution-architect/  ui-ux-design/
  security-engineer/    developer/         code-review/         integration-engineer/
  qa-tester/            release-devops/
workflow/                  ← MASTER-WORKFLOW (gates) + ROLE-CHAIN (who hands what to whom) + ROUTING-MATRIX
templates/                 ← SPEC, BA, API-CONTRACT, ADR, SECURITY, TEST-REPORT, FAILURE-REPORT, RELEASE, STATUS
skills-index/              ← External GitHub skills by role + install commands + safety notes
examples/                  ← Worked examples: a UI redesign, a feature through all 8 gates (with a real FAIL),
                             and a filled-in PROJECT-PROFILE to learn the format from
chat/                      ← Using it on a chat AI: CHAT-GUIDE + START-PROMPTS
dist/FULL-CONTEXT.md       ← The entire repo in one file, for chat AIs to read in one go
scripts/                   ← build-full-context.sh (regenerates dist/ after editing skills)
docs/                      ← How agents use this repo / How to customize / TESTING-GUIDE (verify it yourself) /
                             GLOSSARY / FAQ & troubleshooting / USER-PROMPTS (steering commands for the owner)
LICENSE · CONTRIBUTING.md · SECURITY.md ← MIT license, contribution rules, security policy
```

## Design principles of this repo (learned from the best skill repos)
- **A skill is a folder + `SKILL.md`** (the anthropics/skills standard): instructions, templates, and references travel together; the `description` states what it does and when to use it, because that description is the activation mechanism.
- **A bootstrap rule** (learned from obra/superpowers): one entry file orders the agent to check for a relevant skill *before* any action — never rely on the agent remembering.
- **The spec is the source of truth** (learned from github/spec-kit): specify → clarify → plan → tasks → implement → converge; clarification answers are written back into the spec.
- **Project truth in one file** (learned from pbakaus/impeccable): `/impeccable init` writes `PRODUCT.md` once and every later command re-reads it — here, that file is `PROJECT-PROFILE.md`.
- **Searchable design data** (learned from nextlevelbuilder/ui-ux-pro-max): UI/UX decisions come from looking up style/palette/font/guideline data by product type, not from the model's "taste".
- **A roster of roles with deliverables** (learned from BMAD-METHOD): Analyst → PM → Architect → Dev → QA, each role owning one concrete handover artifact.

## License & attribution
This repo's original structure and content: free to use for personal and commercial projects; attribution appreciated when redistributing.
External skills *linked* in the skills index keep their own authors' licenses — this repo does not copy their content.
