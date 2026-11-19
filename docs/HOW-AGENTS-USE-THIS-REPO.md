# How agents use this repo (for anyone curious about the mechanism)

1. **One entry point:** `AGENTS.md` — the file most coding agents (Codex, Copilot, Cursor, Claude Code via `CLAUDE.md`) read automatically when opening a project. It contains bootstrap rules that force the agent to check for a relevant skill before acting (a mechanism learned from Superpowers).
2. **Skills activate by description:** Each `skills/<role>/SKILL.md` has frontmatter whose `description` says "what it does + when to use it + trigger keywords". The agent loads every skill's description at very low cost and reads the full text only when a task matches — this is the Agent Skills standard (agentskills.io) that anthropics/skills uses.
3. **Each role answers four questions:** What to do (workflow) · What to use (tools, templates, external skills) · What to look up (sources/standards) · What to hand off (artifact + acceptance criteria). See `workflow/ROLE-CHAIN.md` for the full circulation map.
4. **Lazy, just-in-time reading:** An agent does not read the whole repo at once. For each gate it reads that role's skill plus the previous gate's artifact; `references/playbook.md` is opened only when the skill points to it. `PROJECT-PROFILE.md` and the task's spec are read every time.
5. **Artifacts are the memory:** Every decision lives in the task's files (`tasks/<slug>/`), not in chat — a new session or a different agent can pick up exactly where the last one stopped.
6. **External skills are a reference library:** `skills-index/` only points to the original repos; an agent uses an external skill once it has been installed per the instructions there.

## Why roles — and when NOT to split

An obvious question: if one agent wears all ten hats, why have roles at all?

**The roles are context partitions and check partitions, not a headcount.** By default, **one agent wears the hats in sequence**. Each role gets a fresh, bounded context (its SKILL.md + the incoming artifact, not the whole accumulated chat), and each role *checks* the previous role's work against written acceptance criteria — that is what maker ≠ checker means in a one-agent setup. The artifact handoffs exist precisely to stop the "telephone game" in which a long, unstructured session gradually loses the original requirements: what survives a context switch is the artifact, not the memory of having meant well.

This matches the current field evidence. Anthropic's Applied AI team reported (Oct 2026) that consolidated **single-agent + skills** setups matched or beat multi-agent fleets — at roughly **2× the speed** — in enterprise deployments, largely because every real agent-to-agent handoff loses context. Splitting into truly separate agents is justified **only** when at least one of these holds:

1. **Measurable context degradation** — the single agent's work demonstrably worsens as one session carries everything (lost requirements, confused state), even with artifact handoffs.
2. **True parallel isolation** — independent workstreams must proceed simultaneously without contaminating each other's context (e.g. a security audit that must not see the implementer's reasoning).
3. **An oversized tool library** — the available tools exceed roughly **30–50 definitions**, past which a single agent's tool selection measurably degrades; splitting by role gives each agent a small, relevant tool set.

Absent one of those, keep one agent and the ten hats. The gates, artifacts, and checklists are what produce the discipline — the number of processes wearing them is an implementation detail.
