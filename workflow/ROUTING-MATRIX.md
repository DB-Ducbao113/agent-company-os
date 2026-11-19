# ROUTING MATRIX — Route to the right roles, and enough of them

**Precedence rule:** when Tool A (the questions) and Tool B (the task types) disagree, the **stricter requirement wins** — a role marked mandatory by either tool is mandatory.

## Tool A — The 12-question decision tree (the Orchestrator answers these for every task)
| # | Question | If YES → activate |
|---|---|---|
| 1 | Is the business logic ambiguous, open to multiple interpretations, or does it involve money / states / multi-step processes? | BA mandatory |
| 2 | Does it change system structure, the layout system, shared components, routing, or state — or must it comply with an existing architecture/design system? | Architect mandatory, goes first |
| 3 | Will users see or touch the change? | UI/UX mandatory |
| 4 | Is there new or changed server-side logic / APIs? | Architect BE + Developer BE |
| 5 | Does it change the DB (tables/columns/migrations/existing data)? | Architect BE mandatory + Release must include data backup/rollback |
| 6 | Login, permissions, sensitive data, money/payments, file uploads, or API keys? | Security mandatory — no exceptions |
| 7 | Must FE↔BE (or your system ↔ a third party) be joined or re-joined? | Integration mandatory |
| 8 | Will real users use it (not a throwaway prototype)? | QA mandatory (prototype: reduced QA) |
| 9 | Does it go to production / real users? | Release mandatory |
| 10 | Is it a bug fix? | Bugfix branch: QA reproduces first → Developer fixes → QA regression |
| 11 | Content/text/data only, no behavior or layout change? | Fast lane + QA still verifies against the official source |
| 12 | Open creative work (video, 3D, motion, brand)? | UI/UX research first + a prototype approved before production |

**Trigger — AI features:** does the product include AI features that interact with users or generate content? → Security (Gate 4) must apply the AI/LLM checklist, and the spec must include AI disclosure items: users are told they are interacting with AI, and AI-generated content is marked as such. Classify the feature during intake (see the AI rows of the NFR catalog in `skills/orchestrator-intake/references/elicitation-deep-dive.md`): does it consume a third-party model or provide/host one, and is the use case high-risk (e.g. hiring, credit, education)?

## Tool B — Routing by task type
✅ mandatory · ◐ conditional · — skipped (state the reason in the Routing Decision)

| Task type | BA | Arch | UI/UX | Sec | Dev | Integ | QA | Release |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| UI redesign | ◐ if flows change | ✅ FE first | ✅ | ◐ auth/data screens | ✅ FE | ◐ API usage changes | ✅ | ◐ |
| New feature, FE+BE | ✅ | ✅ | ✅ | ◐ Q6 | ✅ | ✅ | ✅ | ✅ |
| FE-only feature (existing API) | ◐ | ◐ FE | ✅ | — | ✅ FE | ◐ | ✅ | ◐ |
| BE/API-only feature | ✅ | ✅ BE | — | ✅ | ✅ BE | ✅ | ✅ | ✅ |
| Bug fix | — | ◐ architectural bug | — | ◐ permission/data bug | ✅ | ◐ | ✅ | ◐ |
| Content/data update | — | — | — | — | ◐ | — | ✅ verify vs source | ◐ |
| Security work | — | ◐ | — | ✅ leads | ◐ | ◐ | ✅ re-test | ◐ |
| Performance optimization | — | ✅ measure first | ◐ | — | ✅ | ◐ | ✅ re-measure | ◐ |
| Prototype/demo | ◐ | — | ✅ | — | ◐ | — | ◐ | — |
| Infrastructure/deploy | — | ◐ | — | ◐ env/secrets | — | ◐ | ◐ smoke | ✅ leads |
| Documentation/report | ◐ | — | — | — | — | — | ◐ check figures | — |

> **Substitution rule (no deadlocks):** when routing skips a role, downstream input tables treat the missing artifact as substituted — the Gate 0 spec stands in for the BA document (see the Orchestrator's condensed-BA rule in `skills/orchestrator-intake/SKILL.md`, Step 7.6), and the release plan stands in for a full QA report on smoke-only routes. The substitution is recorded in STATUS.md. A skipped role's artifact must never deadlock a routed task.
