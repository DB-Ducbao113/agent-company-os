# Changelog

All notable changes to this project are documented here.
The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [3.1.0] — 2026-11-19
### Added
- **Test-Case Gate law** (Constitution §11–12, MASTER-WORKFLOW, AGENTS.md rule 10): every gate defines its test cases up front; the next gate starts only at 100% PASS; a single FAIL stops the workflow and requires a written Failure Report before anything continues; fixes are verified by re-running the failed case and the full suite.
- `templates/FAILURE-REPORT.template.md` — what failed, expected vs. actual, evidence, suspected cause, owning role, proposed fix, user decisions.
- **Long-Input Decomposition Protocol** (Orchestrator Step 1b + playbook §6): long/detailed user instructions are segmented, inventoried, and coverage-checked with a zero-drop rule; the SPEC template gains §12 Requirement Inventory & Source Coverage.
- `docs/TESTING-GUIDE.md` — the owner's verification manual: the Test-Case Gate explained, plus a 10-case workflow test suite (WT-01…WT-10) with exact prompts, expected behavior, PASS/FAIL signs, and a score sheet.
### Changed
- TEST-REPORT template states the zero-fail rule and PASS/FAIL counts; QA skill's gate checklist carries the rule inline.

## [3.0.0] — 2026-11-19
### Changed
- **The entire repo is now standardized in English** (README, AGENTS, constitution, workflow, templates, all skills and playbooks, skills index, examples, docs, chat guides).
- Every SKILL.md restructured into one uniform role format whose core is the repo's purpose: **What To Do** (workflow) · **What To Use** (tools, templates, external skills) · **What To Look Up** (sources/standards, what to search for) · **Handoff to the Next Role** (artifact, required contents, sender checklist, receiver acceptance criteria, rework loop).
### Added
- `workflow/ROLE-CHAIN.md` — the one-page circulation map: what each role receives, produces, and hands to whom.
- AGENTS.md bootstrap rule #9: handoff discipline (work moves only through artifacts; receivers may reject incomplete handoffs with specific reasons).

## [2.0.0] — 2026-11-19
### Added
- A deep `references/playbook.md` for every skill (progressive-disclosure tier 3).
- `.claude-plugin/marketplace.json` with 3 plugins: full / front (Gates 0–3) / delivery (Gates 4–8).
- A `chat/` folder: CHAT-GUIDE + START-PROMPTS for use on ordinary chat AIs.
- `dist/FULL-CONTEXT.md` + `scripts/build-full-context.sh`: the single-file edition for chat AIs.
### Changed
- All 10 SKILL.md files rewritten in detail (~190–230 lines each): when to use / not use, input/output contracts, step-by-step workflow, hard cases, examples, gate checklists, anti-patterns, handoff protocol. Frontmatter gained `license` + `metadata.version`.
- README: installation matrix by platform (plugin marketplace, skills CLI, manual copy, Claude.ai zip, chat) + how to invoke skills.

## [1.0.0] — 2026-11-19
- First release: AGENTS.md bootstrap, constitution + PROJECT-PROFILE template, 10 role skills, workflow + routing matrix, 8 templates, skills index (external GitHub skills by role), worked example.
