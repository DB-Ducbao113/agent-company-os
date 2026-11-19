# CHAT GUIDE — Using Agent Company OS on a chat AI (no coding agent needed)

## Why a separate chat mode?
A coding agent (Claude Code, Codex, Cursor…) reads the repo from disk and loads skills automatically when a task matches.
A chat AI cannot: it only knows what you bring into the conversation. So on chat, **you** act as the skill loader: bring the right file in, at the right time. This repo supports three levels:

| Level | Method | When to use |
|---|---|---|
| 1 — Repo link | Paste the GitHub link + the starter prompt (`START-PROMPTS.md` §1) | Chats with web browsing (Muse, ChatGPT, Gemini…) |
| 2 — Single file | Paste the raw link of, or attach, `dist/FULL-CONTEXT.md` | The chat reads links poorly, or you want to be sure it reads everything |
| 3 — One skill at a time | Paste/attach exactly one `SKILL.md` + the previous gate's artifact | Small jobs, calling a single role, saving context |

## Working on chat (the gates stay the same)
1. Open a new chat → use the starter prompt → the AI runs Gate 0 (clarify → playback → spec → routing) right in the chat.
2. You approve the spec/routing in chat (reply PASS / REWORK / STOP).
3. Each next gate: either say "continue with role X" in the same session (the AI already has context), or open a new session and use the single-role prompt (START-PROMPTS §2) with the previous gate's artifact attached.
4. Save every artifact the AI returns as a file in your project's task folder (structure in AGENTS.md). Chat is the workplace; **files are the durable memory** — never let an artifact live only in chat.
5. Long sessions: use the STATUS summary prompt (START-PROMPTS §4) before switching sessions.

## Honest limits of chat mode
- A chat AI cannot run code/tests on your machine unless that platform provides execution tools — "evidence" (logs, screenshots) may need to come from you or a coding agent at the Developer/QA gates.
- The GitHub link must point to a **public** repo, or you must attach files directly, for a chat AI to read it. Private repo → use levels 2/3 with file attachments.
- Chat context is finite: for large tasks, run one gate per session instead of stuffing a whole project into one session.
