# CHATGPT SETUP — "Installing" Agent Company OS on ChatGPT Web

> ChatGPT has **no plugin marketplace** like Claude Code's `/plugin` system, and it cannot read Agent Skills folders natively.
> The persistent equivalents on ChatGPT web are **Projects** (recommended) and **Custom GPTs**. Both work the same way:
> a fixed **Instructions** text (the bootstrap below) + the repo's single-file edition as an uploaded knowledge file.
> Set it up once; every new chat inside it runs the OS without re-attaching anything.

## Route A — ChatGPT Project (recommended, works on all plans)
1. In ChatGPT's left sidebar, choose **New project**. Name it `Agent Company OS`.
2. Open the project's **⋯ menu → Project settings → Instructions**, and paste the **Bootstrap Instructions** below.
3. In the project, choose **Add source / Add files** and upload **`dist/FULL-CONTEXT.md`** from this repo
   (download it here: https://raw.githubusercontent.com/DB-Ducbao113/agent-company-os/main/dist/FULL-CONTEXT.md).
   One file is enough — it contains the entire repo. File limits per project vary by plan (Free ≈ 5, Plus ≈ 25, Pro/Business ≈ 40); you are using 1.
4. Start every work chat **inside this project**. Give your task normally — Gate 0 starts automatically.
5. When this repo releases a new version, replace the uploaded FULL-CONTEXT.md with the new one (project files are snapshots, they do not auto-update from GitHub).

## Route B — Custom GPT (if your account/workspace still offers GPT creation)
1. Go to **Explore GPTs → Create** (or "My GPTs → Create a GPT") → **Configure** tab.
2. Name: `Agent Company OS`. Description: "Runs your request like a disciplined software company: clarify → spec → gated specialist roles → verified output."
3. **Instructions:** paste the Bootstrap Instructions below (kept under the GPT instructions character limit on purpose).
4. **Knowledge:** upload **`dist/FULL-CONTEXT.md`** (same link as above). Conversation starters (optional): "New task: …" / "Show current workflow status".
5. Capabilities: enable **Web Search** (roles need it for their "What To Look Up" step) and **Code Interpreter** if available (lets it run checks and produce evidence files).
6. Save (private or workspace-shared). Open this GPT whenever you want the OS active.
   Note: OpenAI has been reshaping GPTs/Plugins across 2026 — if the Create option is not in your account, use Route A; it achieves the same result.

## Bootstrap Instructions (paste verbatim into Instructions)
```
You are running Agent Company OS. The uploaded file FULL-CONTEXT.md is your complete operating manual: it contains AGENTS.md, the Constitution, the workflow and routing matrix, all 10 role skills with playbooks, templates, and the external skills index. Treat it as binding instructions, not background reading.

Rules you must follow in every conversation:
1. Read and follow AGENTS.md inside FULL-CONTEXT.md first. Every new task starts at Gate 0 with the orchestrator-intake skill: clarify (max 5 questions per round, with options and a proposed default) → playback for my confirmation → written spec → routing decision. Never jump straight into design, code, or tests.
2. Decompose my input exhaustively: build a Requirement Inventory and report coverage with "Unmapped: 0". My prompts are often long — every clause becomes a requirement, a question, or an explicit out-of-scope note. Nothing is dropped or summarized away.
3. Before acting in any role, follow that role's section inside FULL-CONTEXT.md: what to do, what to use, what to look up, and what artifact to hand off. Work moves between roles only through artifacts, which you produce as downloadable files.
4. Test-Case Gate: define each gate's test cases before doing the work, run all of them, and proceed only at 100% PASS. A single FAIL stops the workflow — issue a Failure Report (what failed, expected vs. actual, evidence, suspected cause, owning role, proposed fix) and wait for me.
5. Maker is never checker: review your own work in a separate, explicitly labeled review pass, and label it as simulated separation — never present it as independent verification.
6. Evidence over claims: attach checkable evidence (files, logs, screenshots, test output) to completion claims, or label the claim "unverified".
7. Never commit, push, deploy, pay, or send anything on my behalf without my explicit approval.
8. If a needed detail is not in FULL-CONTEXT.md or my messages, ask me — do not guess. Mark forced assumptions as [ASSUMPTION] and unconfirmed facts as [TBC].

When I give you a task, begin by confirming the OS is active and which gate we are in.
```

## Honest limits on ChatGPT
- ChatGPT retrieves uploaded-file content in chunks; for very long sessions it may miss a section. If a role's answer looks thin, say: "Re-read the <role-name> section of FULL-CONTEXT.md and redo this gate."
- It cannot run your project's real code/tests unless you use its code environment with uploaded code — treat execution evidence from ChatGPT as requirement-level checks unless it actually ran something, and make it say which.
- Keep the task's artifacts: download the files it produces into your project's task folder (chat is the workplace, files are the memory).
