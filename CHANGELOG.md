# Changelog

All notable changes to this project are documented here.
The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [3.4.0] — 2026-11-19
### Added
- **A second deep-dive playbook for every role** (in each skill's `references/`): Orchestrator → elicitation deep dive (5 Whys, laddering, NFR catalog, vague-word translation table); BA → domain modeling (data dictionary, decision tables, WSJF/Kano, AC quality rubric); Architect → architecture patterns catalog (use/avoid/cost, sync-vs-async, multi-tenancy, tech-selection matrix); UI/UX → design systems (3-layer tokens, type scale, 12-part component spec anatomy, theming, icon construction, design QA); Security → security by application type (web, API, mobile, multi-tenant SaaS, payments, file-upload, realtime, admin tools — threats, controls, mandatory tests per type); Developer → engineering craft; Code Review → review checklists by change type + comment bank; Integration → third-party integration field guide (OAuth, webhooks, payments, failure modes); QA → test design deep dive (risk-based testing, charter library, flaky protocol, regression selection); Release → release engineering (deployment strategies, flags, observability, DR, incident runbooks).
- The FULL-CONTEXT build script now concatenates every file in each skill's `references/` folder.

## [3.3.0] — 2026-11-19
### Added
- `chat/CHATGPT-SETUP.md` — how to "install" the OS on ChatGPT web: Route A via a ChatGPT Project (instructions + FULL-CONTEXT.md as a project file), Route B via a Custom GPT, with a ready-to-paste Bootstrap Instructions text (under the GPT instructions character limit) and honest platform limits.

## [3.2.0] — 2026-11-19
### Added
- **Gate Test Cases starter set in every skill** (TC-00…TC-08, 8 cases per gate): each role now ships concrete, verifiable test cases — derived from its own checklist — with verification method and required PASS evidence, operationalizing the Test-Case Gate law.
- `LICENSE` (MIT), `CONTRIBUTING.md`, `SECURITY.md` — the standard repo files.
- `docs/GLOSSARY.md` (every term defined once), `docs/FAQ.md` (usage Q&A + troubleshooting), `docs/USER-PROMPTS.md` (ready-made owner commands: approve/rework/stop, respond to a Failure Report, resume a session).
- `examples/example-project-profile.md` (a complete filled PROJECT-PROFILE) and `examples/example-feature-end-to-end.md` (a feature through all 8 gates, including a Gate 6 FAIL + Failure Report + fix + full re-run).
### Changed
- Code Review's verdict now always lives in its own file `05-code-review.md` (naming unified across AGENTS.md, ROLE-CHAIN, and the developer/code-review skills).
- Versions synchronized at 3.2.0 (skill metadata, plugin marketplace, changelog).

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
