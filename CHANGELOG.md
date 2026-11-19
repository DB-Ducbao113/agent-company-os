# Changelog

All notable changes to this project are documented here.
The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

## [3.6.0] — 2026-11-19
### Fixed — workflow logic (internal audit + GitHub benchmark vs BMAD / Spec Kit / Superpowers)
- Integration can no longer issue a "conditional PASS" (it contradicted the Test-Case Gate law); conclusions are PASS/FAIL, with only a user-written override in STATUS.md as exception. Integration must also verify Code Review APPROVE before starting.
- Routing deadlocks removed: when routing skips a role, downstream input tables accept the recorded substitution (Gate 0 spec / release plan) instead of stopping (Developer, UI/UX, Release input rules + a substitution rule in the routing matrix). UI/UX arch input is now conditional.
- STATUS.md verdicts are recorded only by the Orchestrator; STOP now has a closure path; BLOCKED is a recognized test-case result (never PASS); routing Tool A vs Tool B conflicts resolve to the stricter requirement; ADRs live in the project repo; PROJECT-PROFILE has a named maintainer (the Orchestrator).
### Added — workflow mechanisms
- **Pre-Implementation Consistency Audit** after Gate 4 (read-only cross-check of the whole planning set, modeled on Spec Kit `analyze` / BMAD readiness gate); **work units + TDD + baseline check inside Gate 5**; **two-stage code review** (spec compliance before code quality); **Correct-course** protocol for mid-flight requirement changes; **Retrospective** after Gate 8; **Resume protocol** for new sessions; **mid-task approval law** (architecture changes, data deletion, risky DB changes, paid services, disruptive changes — one decision per approval); **GATE-REPORT template** and a 6-level completion vocabulary; roadmap section in the SPEC template; greenfield project setup in the Developer skill; minimal-change rule for bug fixes; condensed-BA rule.
### Added — AI-era discipline
- Security: app type (i) **AI / LLM ## [3.5.0] — 2026-11-19 agentic features** (OWASP LLM Top 10 2025 + ASI themes, 8 mandatory tests); Gate 0 AI classification + disclosure routing. BA: rate-based acceptance criteria + golden sets for probabilistic features. QA: evals as the AI test artifact + discipline for AI-generated tests and self-healing tools. UI/UX: new `ai-feature-ux.md` playbook (patterns, autonomy tiers, AI states, disclosure as a design deliverable).
### Added — operations ## [3.5.0] — 2026-11-19 reliability
- **operations-maintenance.md** (dependency automation, EOL tracking, patch cadence, tech-debt register, ops rhythm, feedback intake); **vulnerability patch SLA** (exploited+exposed ≤3 days, critical 14d, high 30d); **SLOs ## [3.5.0] — 2026-11-19 error budgets** with a release-freeze policy; **SBOM per release + artifact signing / SLSA Build L2 provenance verified at deploy**; mobile-store release checklist.
### Changed — standards currency
- OWASP Top 10 table rewritten to the **2025 edition**; **ASVS pinned to 5.0.0** with version-prefixed citations; authentication baseline per **NIST SP 800-63B-4**; zero-trust minimums for admin tooling; platform citations updated (**Material 3 Expressive**, **Apple Liquid Glass**) with a version/date rule; DORA refreshed to five metrics + AI capabilities note; Spec Kit index entry updated to v1.4.x.
### Added — self-maintenance
- **docs/UPSTREAM-WATCH.md** (the OS update mechanism: every upstream standard, its current version, and its update trigger) and **docs/EVALS.md** (WT-01…WT-10 as a versioned regression suite that blocks releases); "Why roles — and when NOT to split" (Anthropic field evidence) + harness/context-engineering vocabulary; third-party skill vetting checklist.

## [3.5.0] — 2026-11-19
### Added
- **Native ChatGPT install packages** in `dist/` (built by `scripts/build-chatgpt-packages.py`): `agent-company-os-plugin.zip` (portable Agent Plugins layout: `plugin.json` + all 10 skills, Orchestrator as onboarding skill) for Plugins → Add → Upload plugin ZIP; and `chatgpt-skills/` + `chatgpt-skills-bundle.zip` with one upload-ready ZIP per role for Plugins → Skills → Add → Upload from your computer. Every skill ZIP bundles `references/os-core.md` (AGENTS + Constitution + workflow + routing + all templates) so the system holds together when skills are installed one by one, plus an `agents/openai.yaml` display file.
- `chat/CHATGPT-SETUP.md` rewritten around the native routes (plugin ZIP → skill ZIPs → Project fallback).

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
