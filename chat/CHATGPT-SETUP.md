# Using Agent Company OS on ChatGPT (web)

ChatGPT now supports the same open Agent Skills standard as this repo: skills are
installed natively from the **Plugins → Skills** tab, and whole plugin packages can be
uploaded as a ZIP. No copy-pasting of the full manual is needed anymore. There are two
native routes — try Route 1 first (one file), fall back to Route 2 (ten files).
Route 3 (Project) remains as a fallback for plans without skill upload.

Everything you need is pre-built in this repo under `dist/`:

- `dist/agent-company-os-plugin.zip` — the whole system as one plugin package.
- `dist/chatgpt-skills-bundle.zip` — one download containing the 10 individual skill
  ZIPs (unzip it once on your computer, then upload the 10 ZIPs inside).
- Each skill ZIP contains the skill's `SKILL.md`, its deep-dive playbooks, a ChatGPT
  display file (`agents/openai.yaml`), and `references/os-core.md` — the shared
  operating law (AGENTS.md + Constitution + workflow + routing + templates) bundled
  into every skill, so the system holds together even when skills are installed
  one by one.

---

## Route 1 — Upload the plugin ZIP (try first)

1. In ChatGPT, open **Plugins** (sidebar).
2. Click **Add ▾** (top right) → **Upload plugin ZIP** ("Tải lên tệp nén plugin").
3. Choose `dist/agent-company-os-plugin.zip`. Do not unzip it first.
4. Wait for the automated checks. If it is accepted, all 10 role skills appear,
   with the Orchestrator as the onboarding skill.

If this route rejects the file (the plugin-package format is newer and stricter than
skill upload), use Route 2 — it is the officially documented skill path.

## Route 2 — Upload the 10 skills (documented path)

1. Download `dist/chatgpt-skills-bundle.zip` and unzip it once — you get 10 files
   like `orchestrator-intake.zip`, `business-analyst.zip`, …
2. In ChatGPT, open **Plugins** (sidebar) → the **Skills** tab (top of the page).
3. Click **Add ▾** → **Upload from your computer**.
4. Choose one skill ZIP (do NOT unzip the skill ZIP itself). Repeat for all 10.
5. ChatGPT scans each upload; most become available immediately. A skill marked
   **Needs Review** asks you to open and confirm it; **Blocked** means the scan
   stopped it — re-download the ZIP unchanged and try again.

### Using the installed skills

- In any chat, type `@` and pick a skill explicitly, or just describe the task —
  ChatGPT invokes the skill whose description matches.
- Start every new task with the **Orchestrator / Intake** skill (Gate 0). As work
  moves through the gates, invoke the matching role skill (or let the description
  matching do it) — each role's handoff tells you which skill comes next.
- Uploaded skills do not auto-update: when this repo releases a new version,
  re-download the ZIPs and upload them again (rebuild them any time with
  `python3 scripts/build-chatgpt-packages.py`).

## Route 3 — ChatGPT Project (fallback, works on every plan)

Use this when your plan has no skill upload.

1. Sidebar → **New project**, name it `Agent Company OS`.
2. Project menu (⋯) → **Project settings → Instructions** → paste the Bootstrap
   Instructions below.
3. **Add files / sources** → upload the single file `dist/FULL-CONTEXT.md`
   (build it with `bash scripts/build-full-context.sh`, or download the raw file
   from the repo). One file is deliberate: project knowledge is retrieved in
   chunks, and a single complete manual keeps cross-references intact.
4. Do all Agent Company OS work in chats inside this project.
5. On every new repo version, replace the uploaded file — project files are
   snapshots; they do not sync from GitHub.

## Bootstrap Instructions (for Route 3 — paste as-is)

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

- **Skills are invoked per role, not as one program.** The discipline comes from
  the Orchestrator skill and the bundled `os-core.md`; if a chat drifts, say:
  "Re-read the orchestrator-intake skill and os-core.md, and redo this gate."
- **Retrieval is chunked** on the Project route: the model may not hold all
  ~6,500 lines at once. Same remedy: name the role/section to re-read.
- **Execution evidence** is requirement-level unless ChatGPT actually ran
  something (e.g. via code interpreter). Treat "verified" claims accordingly.
- Custom GPTs are being retired by OpenAI in favor of skills/plugins — prefer
  Routes 1–2 over building a new Custom GPT.
