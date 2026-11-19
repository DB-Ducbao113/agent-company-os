# START PROMPTS — Copy & paste into any chat AI

> For working on **chat** (Muse, ChatGPT, Gemini, Muse chat…) instead of a coding agent.
> Replace `<REPO_URL>` with this repo's GitHub link after you push it (e.g. `https://github.com/DB-Ducbao113/agent-company-os`).
> If the chat AI cannot read links, use the single-file method in §3.

## 1. Full starter prompt (recommended)
```
Read this repository and work according to it for the whole session:
<REPO_URL>

How to read it: open AGENTS.md at the root first and follow its Bootstrap Rules.
Then read skills/orchestrator-intake/SKILL.md.

Your role: the Orchestrator of Agent Company OS.
My task is: "<your raw task>"
My project: <1-2 sentences + stack, or paste my PROJECT-PROFILE here>

Start with Gate 0: clarify with me first (max 5 questions, with options and a proposed default),
then play back your understanding for my confirmation, and only then write the spec and routing.
Do not do the specialist roles' work yourself.
```

## 2. Calling one specific role (when you already have the previous gate's artifact)
```
Read this file and work exactly in the role it defines:
<REPO_URL>/blob/main/skills/<skill-name>/SKILL.md

Here is the previous gate's artifact: <paste content or attach the file>
Here is my project's PROJECT-PROFILE: <paste content>
Follow the skill's workflow, return the artifact in exactly the template the skill specifies,
with its gate checklist self-checked. If information is missing, ask — do not guess.
```
Valid skill names: `orchestrator-intake` · `business-analyst` · `solution-architect` · `ui-ux-design` ·
`security-engineer` · `developer` · `code-review` · `integration-engineer` · `qa-tester` · `release-devops`.

## 3. When the chat cannot read many files — the single-file edition
This repo ships a concatenated single file: `dist/FULL-CONTEXT.md`. Paste its raw link:
```
https://raw.githubusercontent.com/DB-Ducbao113/agent-company-os/main/dist/FULL-CONTEXT.md
```
with: *"Read this entire file, follow AGENTS.md inside it, and start at the orchestrator-intake skill. My task is: …"*
Or even simpler: attach `dist/FULL-CONTEXT.md` directly to the conversation — this works on every chat AI, even without web access.

## 4. Keeping a long session alive
When a chat gets long or its context is compacted, paste:
```
Summarize the current state of work following Agent Company OS's STATUS template:
which gates have PASSed, which artifacts exist, what is waiting for whose approval, which risks are open.
```
Keep that summary — start a new session with the §1 prompt + this summary to continue without losing work.
