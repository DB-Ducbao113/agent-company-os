# Security Policy

## What this repo is
Agent Company OS is a set of instruction files (Agent Skills) — it contains no executable code of its own beyond a text-concatenation shell script (`scripts/build-full-context.sh`). The security surface is therefore mostly about **the instructions themselves and the third-party skills they point to**.

## Reporting a problem
- Found an instruction in this repo that could make an agent do something unsafe (leak data, skip a safety gate, run untrusted code)? Open a GitHub issue with the file and line, or contact the maintainer privately via their GitHub profile if the issue is sensitive.
- Found a problem in a **third-party skill** listed in `skills-index/`: report it to that skill's own repository. If it is serious, also open an issue here so the entry can be annotated or removed.

## Standing guidance for users (also in the skills index)
- A skill runs with your agent's privileges. **Read any third-party skill's SKILL.md (and its scripts, if any) before installing it.** The full pre-install routine — reading SKILL.md and scripts, checking requested permissions, preferring official sources, pinning source + version, and re-vetting on every update — is the **"Before you install any third-party skill" checklist at the top of `skills-index/SKILLS-INDEX.md`**. Run it for every install and every update.
- Prefer official organizations and actively maintained, widely used repos.
- Never install unknown skills into an environment holding production credentials or sensitive data without review.
- This repo's own workflow assumes the same caution internally: the Security role's gates (Gate 4, and the mandatory security tests handed to QA) exist precisely because agent-written code needs independent checking.
