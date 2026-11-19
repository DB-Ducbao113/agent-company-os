# SKILLS INDEX — External GitHub skills by role

> Curated 2026-11-19. Each entry: what the skill does · repo · install command · license/trust notes.
> Install with the skills CLI: `npx skills add <owner>/<repo> --skill <skill-name>`, or via your tool's plugin marketplace.
> ⚠️ **Safety:** A skill is instructions (sometimes with scripts) that runs with your agent's privileges. Always read a third-party skill's `SKILL.md` before installing it; prefer repos from the owning organizations (Anthropic, GitHub, Vercel, Sentry, Trail of Bits) and actively maintained, widely used repos. Never install an unknown skill into a project containing sensitive data without reading it first.

## ⭐ Foundations (every role should know these)
| Skill / Repo | Use for | Install |
|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) — Anthropic's official repo: `frontend-design`, `webapp-testing`, `skill-creator`, `mcp-builder`, document skills | The reference for how a skill should be written; `skill-creator` to author new skills | `/plugin marketplace add anthropics/skills` |
| [github/spec-kit](https://github.com/github/spec-kit) — GitHub's Spec-Driven Development toolkit (MIT): constitution → specify → clarify → plan → tasks → implement → converge | Gate 0 and this repo's whole spec philosophy | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git` |
| [obra/superpowers](https://github.com/obra/superpowers) — a complete methodology pack: brainstorming, writing-plans, TDD, systematic-debugging, code review, subagent-driven development | Developer + QA + the bootstrap-rule pattern | `/plugin install superpowers@claude-plugins-official` |
| [bmad-code-org/BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) — an agile team as agent personas: Analyst, PM, Architect, UX, Dev, QA (MIT) | A full "agent company" model to compare against | `npx bmad-method install` |
| Large collections for further discovery: [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (400+ skills across domains), [CODE-SAURABH/OpenSkills](https://github.com/CODE-SAURABH/OpenSkills) (49 role-based skills: system-design, security-engineer, qa-engineer, devops-platform, spec-author…) | When a role needs a specialist skill not listed above | `/plugin marketplace add alirezarezvani/claude-skills` |

## Gate 0 — Orchestrator / Intake
| Skill | Why |
|---|---|
| github/spec-kit (above) | The standard specify/clarify flow — the heart of Gate 0 |
| Superpowers `brainstorming` + `writing-plans` | Forces idea clarification before planning; plans broken into small, placeholder-free steps |
| BMAD Analyst (Mary) | A persona that asks "why" until the risks surface |

## Gate 1 — BA
| Skill | Why |
|---|---|
| BMAD Analyst + PM (John) | Product brief → PRD → stories, with an implementation-readiness gate |
| [business-analyst — Agentic Enterprises Skill](https://github.com/rade-nugroho/Agentic-Enteprises-Skill/blob/HEAD/business-analyst/SKILL.md) | Elicitation, MoSCoW, BRD/FRD, user stories + INVEST acceptance criteria |
| OpenSkills `spec-author`, `product-engineer` | Writing unambiguous specs/PRDs |

## Gate 2 — Architect
| Skill | Why |
|---|---|
| BMAD Architect (Winston) | Architecture + readiness check before development |
| OpenSkills `system-design` | Structured system design |
| alirezarezvani engineering — architecture skills | Architecture patterns, ADRs, design review |

## Gate 3 — UI/UX ⭐ (the strongest group in the ecosystem)
| Skill | Why | Install |
|---|---|---|
| [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — `ui-ux-pro-max` | Searchable design intelligence: 160+ reasoning rules, dozens of styles, 160+ palettes, 57 font pairings, UX guidelines, across 10–22 stacks (React, Next, Flutter, SwiftUI…) | `npx skills add https://github.com/nextlevelbuilder/ui-ux-pro-max-skill --skill ui-ux-pro-max` |
| [pbakaus/impeccable](https://github.com/pbakaus/impeccable) — `impeccable` (Apache-2.0, Paul Bakaus) | 24 named design commands (polish/audit/critique/bolder/quieter…), a 62-rule anti-AI-slop detector that runs without an LLM, and the PRODUCT.md mechanism for durable product truth | `npx impeccable install`, then `/impeccable init` |
| anthropics/skills — `frontend-design` | Deliberate aesthetic direction; fights the model's generic defaults | `npx skills add https://github.com/anthropics/skills --skill frontend-design` |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) — `web-design-guidelines` | Audits UI against 100+ Web Interface Guidelines rules (a11y, focus, forms, animation…) | `npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines` |

## Gate 4 — Security
| Skill | Why | Install |
|---|---|---|
| [trailofbits/skills](https://github.com/trailofbits/skills) (CC-BY-SA-4.0) | Audit skills from a real security firm: differential review, semgrep/codeql, sharp-edges, supply chain — including "rationalizations to reject" sections that fight sloppy conclusions | `npx skills add trailofbits/skills --skill <name>` |
| [getsentry/skills](https://github.com/getsentry/skills) — `security-review`, `find-bugs`, `gha-security-review` (Apache-2.0) | Security review that reports only high-confidence findings (injection, XSS, auth/authz); find-bugs sweeps diffs | `npx skills add https://github.com/getsentry/skills --skill security-review` |
| [github/awesome-copilot](https://github.com/github/awesome-copilot/blob/HEAD/skills/agent-owasp-compliance/SKILL.md) — `agent-owasp-compliance` | Checks agent systems against the OWASP Agentic Security (ASI) Top 10 | Per the awesome-copilot repo's instructions |

## Gate 5 — Developer + Code Review
| Skill | Why |
|---|---|
| Superpowers `test-driven-development`, `subagent-driven-development`, `systematic-debugging`, `verification-before-completion` | Working discipline: tests first, small tasks with reviews in between, systematic debugging, verification before claiming done |
| vercel-labs/agent-skills — `react-best-practices` (listed on skills.sh as `vercel-react-best-practices`) | 40+ React/Next.js performance rules from the Vercel team |
| getsentry/skills — `code-review` | Review following Sentry's engineering practices |
| Superpowers `requesting-code-review` / `receiving-code-review` | How to request a review properly + how to receive one with verification instead of blind agreement |

## Gate 6 — Integration
| Skill | Why |
|---|---|
| Spec Kit `analyze` + `converge` | Cross-checks spec↔plan↔tasks consistency and audits finished code against the spec |
| anthropics/skills — `mcp-builder` | When the integration is building a bridge/API/MCP to an external system |
| OpenSkills `api-design` | Standardizing the contract between parties |

## Gate 7 — QA / Tester
| Skill | Why | Install |
|---|---|---|
| anthropics/skills — `webapp-testing` | Playwright: opens the real app, screenshots, reads console logs, debugs UI behavior | `npx skills add https://github.com/anthropics/skills --skill webapp-testing` |
| BMAD Test Architect (TEA module) | Risk-based test strategy and quality gates |
| OpenSkills `qa-engineer`, `test-writer`, `benchmark` | Test-case design + performance checks |
| Superpowers `test-driven-development` + `verification-before-completion` | Evidence discipline behind any "it passes" conclusion |

## Gate 8 — Release / DevOps
| Skill | Why |
|---|---|
| Superpowers `finishing-a-development-branch` | Disciplined branch closing: verify tests, choose merge/PR/keep/discard |
| alirezarezvani — DevOps skills | CI/CD, pipelines, operations |
| OpenSkills `devops-platform` | Deployment/platform engineering |
| getsentry/skills — `gha-security-review` | Audit GitHub Actions before trusting the pipeline |
