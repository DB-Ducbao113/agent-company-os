# Release Engineering — Deep Dive

> Read this when "deploy it" stops being simple: multiple environments, real users who notice outages, money or data at stake. The basic playbook covers versioning, changelog, smoke tests, rollback. This file covers the engineering system around the release — strategies, flags, pipelines, observability, recovery, and incidents.

## 1. Deployment strategies compared

| Strategy | Mechanics | Cost | Rollback speed | Use it when |
|---|---|---|---|---|
| Rolling | Replace instances gradually with the new version | Lowest (no extra infrastructure) | Slow (re-deploy old version, minutes–tens of minutes) | Stateless services, low-risk changes, small scale |
| Blue-green | Two full environments; switch traffic atomically; old env kept warm | ~2× infrastructure during the switch | Fast (switch traffic back, seconds–minutes) | You need a clean, tested cutover and can afford duplicate capacity |
| Canary | New version gets a small % of real traffic (1→5→25→100%), promoted on metrics | Medium (traffic splitting + per-cohort metrics) | Fast for the canary cohort (route back), but bad data written by the canary stays written | High-traffic systems where real-user signal beats any staging test |
| Feature flags | One deployment; behavior toggled per user/cohort at runtime | Low infra, high discipline cost (§2) | Fastest for behavior (flip the flag, no deploy) | Decoupling deploy from release; gradual rollouts; kill switches for risky features |

**Decision rules:**
- Rollback speed only counts if the change is *reversible*: a canary that wrote a new data format has no fast rollback — schema changes need expand→migrate→contract across releases regardless of strategy.
- Blue-green's hidden trap: both colors share one database in most real setups, so "atomic switch" applies to code, not data. Say which one you actually have.
- Canary without per-cohort error/latency metrics is just a slow rolling deploy with extra steps. No cohort metrics → no canary.
- Strategies compose: canary the deploy *and* flag the risky feature inside it is normal for high-stakes changes.

## 2. Feature flag discipline

Flags are debt instruments: cheap to open, expensive to forget.

- **Naming:** `feature.area.name` style, e.g. `checkout.discount-codes`, created in a central registry — never invented inline in code. Every flag has an **owner** and a **created date** recorded at birth.
- **Types have lifetimes:** release flags (days–weeks, removed after full rollout), experiment flags (one experiment's life), ops/kill switches (may be permanent, reviewed quarterly), permission flags (entitlements — these are product data, not release tooling; don't manage them like release flags).
- **Cleanup debt:** a release flag older than its rollout + 2 weeks becomes a tracked cleanup task; the flag list is reviewed at every release. Stale flags are how "the code" stops describing what the system does — and how a forgotten `if` reactivates a dead feature in production.
- **Kill switches:** every risky feature ships with one, and the switch is *tested* (flipping it in staging is part of the release checklist). A kill switch first exercised during the incident it exists for is a hope, not a switch.
- **Defaults matter:** flag service unreachable → the code's default decides. For money/safety features the default is OFF; for cosmetic features, the last-known value. Decide per flag, in writing, at creation.

## 3. Environment management

**Parity checklist (dev / staging / prod)** — drift between staging and prod is why "worked in staging" is a meme:
- [ ] Same runtime versions (language, framework, DB engine + version), same OS family
- [ ] Same configuration *shape*: every env var that exists in prod exists in staging (values differ; a missing key is a deploy-day surprise)
- [ ] Same feature-flag set (values may differ; missing flags default differently per environment — see §2)
- [ ] Data *shape* parity: staging data anonymized from prod (§privacy) or generated to the same distributions — staging with 3 test users proves nothing about the 10k-user query
- [ ] Same external integrations in sandbox mode, with the sandbox-vs-prod divergences listed (Integration role's checklist)
- [ ] TLS, proxies, and network rules equivalent enough that headers/redirects behave the same

**Config vs secrets:** configuration (URLs, timeouts, flag defaults) may live in versioned files; secrets (keys, passwords, tokens) live only in the secret manager / platform env store, never in the repo, never in CI logs, never in screenshots. One rule covers most incidents: *if it would hurt pasted into a chat, it's a secret.*

**Drift detection:** the desired state is code (infrastructure/config as code where the platform allows); a scheduled job or pipeline step diffs actual environment config against the declared state and reports differences. Manual console changes are drift by definition — either back-port them into the declaration or revert them; "we fixed it in the console during the incident" must become a follow-up task the same day.

## 4. CI/CD pipeline design

| Stage | Runs | Blocks merge? | Blocks deploy? |
|---|---|---|---|
| Lint / format / typecheck | On every push | Yes | — |
| Unit tests | On every push | Yes | — |
| Build + artifact | On PR | Yes (a broken build merges nothing) | — |
| Integration / contract tests | On PR | Yes for contract-affecting changes | Yes |
| Security scans (deps, secrets, SAST) | On PR + scheduled full | Secrets findings: yes; others by severity policy | Critical findings: yes |
| E2E smoke on staging | After merge, on deploy to staging | — | Yes |
| Full E2E / regression | Nightly + pre-release | — | Yes, for release candidates |
| Manual approval | Before production | — | Yes — a named human, per this repo's gate law |

- **Artifact immutability:** the artifact built once from a commit is the artifact that travels staging → production (same binary/image, promoted, never rebuilt per environment). Rebuilding for prod means prod runs code that staging never tested.
- **SBOM per release:** every release generates a **Software Bill of Materials** (CycloneDX or SPDX format) from the actual build and archives it with the release record. The SBOM diff against the previous release is reviewed as part of the release check: an unexpected new component — especially a new transitive dependency nobody added deliberately — is a finding to explain before deploy, not a curiosity to notice after an incident. The SBOM is also the inventory the mobile-store privacy check (App Privacy / Data Safety vs. actual SDKs) is verified against.
- **Signing & provenance:** release artifacts are **signed** (keyless signing, e.g. Sigstore cosign, so no long-lived signing keys exist to leak) and ship with build **provenance** — target **SLSA Build Level 2** (signed provenance from a hosted build platform). Generating provenance is only half the control: at deploy time the pipeline **verifies** the signature and provenance of the exact artifact being promoted, and a verification failure blocks the deploy like a failed test. An unsigned or unverifiable artifact is treated as an unknown artifact, however it arrived.
- **Pipeline speed is a quality feature:** a 45-minute pipeline teaches developers to batch changes and skip runs. Keep the merge-blocking path under ~10 minutes; push slow suites to nightly/pre-release stages (and then actually gate on them there).
- **Flaky pipeline tests** follow the QA flaky protocol (quarantine with expiry) — a pipeline people habitually re-run is a pipeline that protects nothing.

## 5. Observability minimums

- **Structured logs:** JSON (or equivalent) with timestamp, level, service, request/trace ID, and the business identifiers that let you follow one user's one operation across services. Free-text logs are unsearchable at exactly the moment you need them. Secrets and personal data are never log fields (§3's rule applies).
- **The 4 golden signals** (per service, dashboarded): **Latency** (p50/p95/p99, successful vs failed separately), **Traffic** (requests/s), **Errors** (rate and count, by class), **Saturation** (CPU/memory/queue depth — how full the system is before it falls over).
- **Alert quality rules:** an alert must be **actionable** (a human can do something specific), **urgent** (it cannot wait for business hours), and **symptom-based** (users are affected) rather than cause-based (a disk *might* fill next week — that's a ticket). Every alert links its runbook (§7). An alert that fires and is ignored three times is deleted or fixed at the next review — alert fatigue is an outage you schedule for later.
- **The release connection:** every deploy is annotated on the dashboards. Half of incident diagnosis is "what changed?" — the annotation answers it in one glance.

**SLOs & error budgets — turning the golden signals into commitments:**
- For each user-facing service, define **1–3 SLOs** — no more; an SLO nobody would page over is decoration. Each SLO states: the **SLI** (a user-experience ratio from the golden signals, e.g. "share of checkouts completing without a 5xx or a timeout"), the **target** (e.g. 99.9%), and the **window** (rolling 30 days is the usual default).
- **Burn-rate alerting:** alert on how fast the error budget is being consumed, not only on raw error counts — a slow leak that will exhaust the budget in 3 days deserves a page-shaped ticket today; a brief spike that costs 0.1% of the budget does not deserve a 3 a.m. call. Multi-window burn-rate alerts (fast burn → page, slow burn → ticket) are the standard shape.
- **The error-budget policy (the part with teeth):** while budget remains, feature releases proceed normally. **When the budget is exhausted, feature releases freeze** — only reliability fixes and security patches ship — until the budget recovers. This rule is agreed with the gate approver *before* it first triggers; negotiating it during an outage means it does not exist.
- The go/no-go checklist (§9) therefore includes the budget's current status: shipping a feature release into an exhausted budget requires the same kind of written, named risk acceptance as any other gate override.

## 6. Backup & disaster recovery

- **Definitions with numbers, agreed before the incident:** **RPO** = how much data you may lose, measured in time (RPO 1h = backups at least hourly). **RTO** = how long recovery may take (RTO 4h = service restored within 4 hours of declaring disaster). "We have backups" without RPO/RTO is a sentiment, not a plan.
- **Backup types:** full (whole dataset, slow, simple), incremental/differential (changes since last full/incremental, faster, chain-dependent), and continuous (WAL/log shipping, PITR — point-in-time recovery, the strongest default for databases that support it). Choose by RPO: RPO of minutes requires continuous; nightly fulls give RPO 24h whether you admit it or not.
- **Restore TESTING schedule:** a backup that has never been restored is a hypothesis. Restore drill: quarterly at minimum (monthly for money/data-critical systems) — restore to an isolated environment, verify integrity (row counts, checksums, a real login + key query), time it against the RTO, record the result in the release/ops log. A failed drill is a P1 defect.
- **Backups are a security surface:** encrypted at rest, access-controlled separately from production (an attacker who owns prod must not be able to delete the backups — separate account/project, retention lock where available), and retention policy written down (e.g. daily 14d, weekly 8w, monthly 12m).
- **Scope honesty:** backups cover data. Recovery also needs the infrastructure/config declarations (§3), secrets (recoverable from the secret manager's own backup/escrow), and this runbook — store copies outside the system they recover.

## 7. Incident runbook template

```
INCIDENT: <title>            SEVERITY: S1–S4        STATUS: Investigating / Mitigating / Resolved
Incident lead: <name>        Comms lead: <name>     Started: <time, timezone>
Impact: <who/what is affected, since when, how measured>
Timeline: <timestamped entries, facts only>
Actions taken / next actions / owner of each
Links: dashboards, alerts, deploy annotation, provider status
```

- **Roles:** Incident lead (decides, coordinates — not necessarily the fixer), fixer(s), comms lead (updates stakeholders; on a small team one person may hold two roles, but the *jobs* stay distinct).
- **Severity ladder:** S1 = service down or data/money at risk → page now, all hands, updates every 30 min. S2 = major feature broken, workaround exists → page the owner, updates hourly. S3 = minor degradation → ticket, next business day. S4 = cosmetic → backlog. Severity is set by *user impact*, not by how embarrassed anyone is.
- **Comms cadence:** internal update at the cadence for the severity even if the update is "no change, still investigating" — silence reads as chaos. External/user-facing messages state impact and next update time, never speculation about cause.
- **Mitigate before diagnosing:** rollback, flag off, traffic shift — restore service first; root cause analysis happens after, with the evidence preserved (logs, snapshots) *before* the rollback destroys it where feasible.
- **Blameless postmortem** (within 3 business days for S1/S2): timeline from records, contributing factors (systems and processes, plural — never a single person's "carelessness"), what detected it / what should have, action items with owners and dates, shared with the team. The test of blameless: would people still report near-misses after reading it?

## 8. Release calendar hygiene

- **Freeze windows:** no non-emergency deploys during the business's peak-risk periods (biggest sales days, regulatory deadlines, the team's skeleton-crew holidays). Freezes are declared in advance on a shared calendar; emergency fixes during a freeze need the named approver and a written reason.
- **"Never deploy on Friday" is a risk heuristic, not a law:** the real rule is *never deploy what you cannot monitor and roll back with the people available*. A small, flagged, well-instrumented change on Friday morning with the team present can be safer than a huge change on Tuesday followed by a holiday. Decide by: change size, reversibility (§1), observability (§5), and who is actually on call — and write the reasoning in the release record when you deviate from the default.
- **Cadence beats size:** many small releases are individually safer and easier to roll back than monthly mega-releases; if releases feel scary, the fix is smaller releases and better gates, not more ceremony per release.
- **One calendar, visible to all:** planned releases, freezes, provider maintenance windows, and marketing/business events that spike traffic — most "surprise" collisions were on somebody's calendar, just not the shared one.

## 9. Go / no-go release readiness checklist

Run at the release gate; any unchecked box is either fixed or converted into a named, accepted risk in the release record.

- [ ] QA verdict PASS (or PASS WITH RISKS accepted by the named decision-maker) at 100% of the gate's test cases, per the Test-Case Gate law
- [ ] Version bumped per SemVer decision rules; changelog written for humans, not generated noise
- [ ] The exact artifact (SHA/image digest) that passed staging is the one being promoted (§4 immutability)
- [ ] Rollback plan written, and the rollback mechanism itself tested at least once before (a first-time rollback during an incident is a second incident)
- [ ] Migrations: reversible, or forward-fix plan written; backup verified restorable (§6 drill is current)
- [ ] Feature flags: states for launch set deliberately; kill switches for risky features tested (§2)
- [ ] Dashboards annotated; alerts for the golden signals active; on-call named for the monitoring window
- [ ] Error budget status checked (§5): budget not exhausted, or the feature release carries a written, named risk acceptance
- [ ] Comms ready: release notes for users/support, status-page draft if the change is user-visible
- [ ] Calendar check: no freeze window, no colliding business event, approver and fixer available for the window (§8)

## 10. Rollback decision rules

- **Pre-agree the triggers** in the release record, in numbers: e.g. "error rate >2× baseline for 10 min", "p95 latency >2× baseline for 15 min", "any confirmed money/data defect". Deciding thresholds mid-incident invites both panic rollbacks and stubborn delays.
- **Who decides:** the incident lead or the release approver — named in advance. Not a committee, not the loudest voice in the chat.
- **Data-aware rollback:** rolling back code does not roll back data. If the bad release wrote data in a new shape, the decision is rollback-code + forward-fix-data, or stay-and-fix — spell out which, and what happens to records created during the bad window, *before* executing.
- **The point of no return:** some steps (a destructive migration, a sent notification, a settled payment batch) cannot be undone. The release plan marks them explicitly; passing one is a deliberate, logged decision, not an accident of momentum.
- **After any rollback:** the release is not "done" — the defect goes back to the owning role with the incident timeline attached, the fix re-enters the pipeline through the normal gates, and the re-release re-runs the failed gate's full test suite.

## 11. On-call basics (the human layer of §5–§7)

- A named on-call rotation exists for anything users depend on; "the team" is not an on-call. Rotations are short enough to stay humane (≤1 week in 4 per person) and handovers are written, not verbal.
- On-call carries: the runbook (§7), dashboard/alert access, deploy/rollback permissions, and the authority to roll back without waking a manager. Authority without permissions, or permissions without authority, both fail at 3 a.m.
- Every page is logged with its outcome (action taken / false alarm / alert defect). The log feeds the alert-quality review (§5) — pages that repeatedly wake humans for nothing get fixed or deleted, because the alternative is humans ignoring the page that matters.
