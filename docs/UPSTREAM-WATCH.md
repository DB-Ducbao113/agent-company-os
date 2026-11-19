# UPSTREAM WATCH — the standards this OS stands on, and when they force an update

> **Purpose.** Agent Company OS is built on upstream standards, toolkits, and
> research that keep moving. This file is the OS's **update mechanism**: the
> single list of everything the OS depends on, the state each item was in when
> last checked, and the trigger that turns an upstream change into an OS
> update. Without this list, the OS silently ages — a skill citing last year's
> standard is misinformation with good formatting.
>
> **Review cadence:** this list is reviewed on the cadence the owner sets.
> **Last full review: 2026-11-19.**
>
> **The rule:** when any row changes materially — a new major version, a
> renamed or removed practice, a deprecated mechanism the OS recommends, a
> changed deadline — **open an OS update task at Gate 0, like any other
> work**: clarify what changed, spec the update, route it to the affected
> roles, and run the evals (`docs/EVALS.md`) before the update is called
> done. Upstream drift is work, and work enters through the front door.

| Upstream source | State at last review (2026-11-19) | Official source | What it affects in this OS | Update trigger |
|---|---|---|---|---|
| **GitHub Spec Kit** | v1.4.x — Extensions, Presets, skills-mode installs; fast-moving | github.com/github/spec-kit | Gate 0's specify/clarify philosophy; the skills-index foundation entry | New major/minor line, changed workflow order, or a deprecated command the index cites → refresh the index entry and Gate 0's references |
| **Agent Skills spec** | Open standard, governed by the **Agentic AI Foundation (AAIF)** since Oct 2026 (donated by Anthropic) | agentskills.io | The format of every `skills/*/SKILL.md` (frontmatter, progressive disclosure) | Any spec change to required frontmatter, folder layout, or activation semantics → audit all 10 skills against it |
| **MCP (Model Context Protocol)** | Spec **2026-07-28**: stateless core; **Sampling, Roots, and Dynamic Client Registration are deprecated** | modelcontextprotocol.io | Integration role's guidance on building/consuming tool bridges (`mcp-builder` pointers) | New spec revision, or a mechanism the OS recommends entering deprecation → update integration guidance |
| **A2A protocol** | v1.0 — **watch-only**; the OS does not depend on it yet | a2a-protocol.org / AAIF | Nothing yet; candidate for future multi-agent handoffs between separate agents | A2A reaches mainstream agent-framework support, or the OS splits roles into truly separate agents → evaluate adoption at Gate 0 |
| **OWASP Top 10** | **2025 edition** is current | owasp.org/Top10 | Security playbook §1 risk table; security-by-app-type checklists | A new edition (historically ~4-year cycle) → rewrite the playbook table and re-check every app-type row |
| **OWASP ASVS** | **5.0.0** (requirements renumbered vs 4.x — cite clause IDs with the version) | owasp.org/ASVS | Security skill's level selection (L1 floor / L2) and SEC-REQ citations | New ASVS release → re-pin the version everywhere it is cited and re-map clause references |
| **OWASP LLM Top 10 + Agentic ASI Top 10** | LLM Top 10 **2025**; Agentic Security (ASI) Top 10 published **Dec 2025** | owasp.org — GenAI Security Project | The AI/LLM app type in `security-by-app-type.md`; AI-feature security tests | New editions or new agentic threat classes → refresh the AI app-type threats, controls, and mandatory tests |
| **NIST SP 800-63 (Digital Identity)** | **SP 800-63-4 final, Jul 2025** (password length ≥15, no forced rotation, phishing-resistant option at AAL2) | nist.gov — SP 800-63-4 | The authentication baseline in the security playbook; architect's auth decision table | A new revision (-5) or changed AAL requirements → refresh the auth baseline |
| **WebAuthn / Passkeys** | **WebAuthn Level 3** is a W3C Recommendation (Aug 2026) | w3.org/TR/webauthn-3 | Passkeys as an evaluated option in the architect's auth table; security's auth baseline | Level 4 work or changed platform passkey behavior → re-verify the option's trade-offs |
| **DORA research** | **No 2026 annual report**; the **2025 "State of AI-assisted Software Development"** report (AI Capabilities Model; AI as amplifier) is the latest benchmark | dora.dev | Release playbook's Light DORA section (five metrics, AI-capabilities note) | A new DORA report or revised metric set → refresh the Light DORA section and its claims |
| **W3C Design Tokens (DTCG)** | **Format Module 2025.10** — the first stable specification (`*.tokens.json`, `$value`/`$type`) | designtokens.org | UI/UX design-systems guidance (token format and tooling) | A new stable DTCG version → re-check the mandated token format and examples |
| **WCAG** | **WCAG 2.2** is the build target; **WCAG 3.0 is a Working Draft — watch-only**, referenced by no law | w3.org/WAI | UI/UX accessibility floor (2.2 AA) and QA's accessibility workflow | WCAG 3.0 reaching Recommendation, or a law adopting it → re-plan the accessibility target; a 2.2 errata/revision → verify the floor text |
| **Apple HIG (Liquid Glass) / Material 3 Expressive** | Current platform design languages (iOS 26 era / Android 16 era) | developer.apple.com/design · m3.material.io | UI/UX Tier-1 source citations; platform rules in the playbook | **Re-verify at every major platform release** (each WWDC / Google I/O cycle) — citations carry version/date and go stale yearly |
| **SLSA** | **v1.2** (Build track L1–L3; L2 = signed provenance from a hosted builder is this OS's target) | slsa.dev | Release-engineering §4 signing & provenance requirements | A new SLSA version or changed level definitions → re-check the L2 target and the verification step |
| **CISA SBOM minimum elements** | **2026 update** of the minimum-elements baseline (SPDX / CycloneDX formats) | cisa.gov/sbom | Release-engineering §4 SBOM-per-release requirement | A revised elements list or a mandate change in a market the user ships to → refresh the SBOM requirement |

## How a review works

1. Walk the table row by row; for each, check the official source (never a
   blog's summary of it) and compare against the "State at last review"
   column.
2. Unchanged rows: update nothing but your confidence. Changed rows: apply
   the rule above — an OS update task at Gate 0, scoped to the "What it
   affects" column.
3. Update this file in the same task: the row's state, and the "Last full
   review" date in the header.
4. Record the review itself (date, rows checked, tasks opened) — a review
   with no record is assumed not to have happened, the same evidence rule as
   every gate in this OS.
