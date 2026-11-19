# Operations & Maintenance — Deep Dive

> Read this when the release is done. The release gate gets a change safely
> into production; this file is the standing discipline that keeps the running
> system healthy *between* releases — dependencies, end-of-life components,
> patch cadence, technical debt, and the rhythm that makes all of it happen
> without relying on anyone's memory.

## 1. Dependency lifecycle automation

Dependencies rot on their own schedule, not yours. The choice is between many
small, boring updates and one terrifying one — automation is how you get the
boring kind.

- **Turn on an update bot** (Renovate or Dependabot) for every repository and
  every ecosystem in it (app dependencies, CI actions, container base images).
  Updates arrive as pull requests; nothing updates itself silently in the
  main line.
- **Group the PRs.** Patch/minor updates of one ecosystem arrive as one grouped
  PR on a schedule (weekly is a sane default), not as 30 individual PRs nobody
  can face. Major-version bumps stay individual — they deserve individual
  reading.
- **Release-age delay:** do not adopt a new dependency version the day it is
  published. Configure a minimum release age (a few days is typical) before the
  bot proposes it. This is supply-chain hygiene: a compromised release is
  usually detected and yanked within days; the delay keeps you out of the
  blast window at the cost of being slightly behind — a trade worth making
  everywhere except security patches (see §3).
- **Pin CI actions** to full commit SHAs (tags can be moved; SHAs cannot), and
  let the update bot propose the bumps — pinned *and* current, not pinned and
  fossilized.
- **Weekly triage slot:** a fixed, short slot (30–60 minutes) where the
  pending update PRs are reviewed and merged or explicitly deferred with a
  reason. An update queue nobody triages is just a slower way to fall behind.
- **Automerge, narrowly:** automerge is allowed only for **patch-level**
  updates with a fully green CI (tests + the security scans from the pipeline)
  and never for anything touching authentication, cryptography, payments, or
  the build itself. Everything else gets human eyes. If a patch update ever
  breaks production through automerge, automerge narrows further — that is
  the feedback loop, not a reason to abandon the system.
- **Reading an update PR** (the human part the bot cannot do): skim the
  changelog/release notes for breaking-change language even in minor bumps,
  check whether the update changes a transitive dependency you rely on
  directly, and confirm the lockfile diff contains only what the PR claims.
  Most supply-chain surprises are visible in the diff to anyone who looks;
  the discipline is looking, briefly, every time — which is exactly what the
  grouping and the weekly slot make affordable.

## 2. End-of-life (EOL) tracking

A runtime or framework past its end-of-life date receives no security patches.
Every day on it is borrowed time, and the borrowing is silent — nothing breaks
the day support ends.

- **Keep an inventory** of the runtimes, frameworks, databases, and base
  images the system runs on, each with its EOL date, checked against
  **endoflife.date** (which also offers an API for automation).
- **Alert ~6 months ahead** of each EOL date. Six months is the point where an
  upgrade is still a planned project; at six weeks it is an emergency, and
  after the date it is an unpatched exposure.
- **Every EOL (or approaching-EOL) item has three things:** a named **owner**,
  an **exit path** (upgrade to which supported version, migrate to what, or
  retire the component), and a **date** by which the exit happens. An EOL item
  with no exit path is recorded as an accepted risk with the gate approver's
  name on it — never as an unowned surprise.
- **CI fails on NEW EOL introductions:** adding a dependency or base image
  that is already EOL (or EOL before the project's planning horizon) blocks
  the change. Existing EOL is managed through the inventory; *new* EOL is
  simply not admitted.

## 3. Vulnerability patch cadence

Known vulnerabilities are patched on the risk-tiered SLA defined in the
release skill (`../SKILL.md`, "Standing duty — vulnerability patch SLA"):
actively exploited + internet-exposed ≤ 3 days, critical 14 days, high 30
days, everything else in the next regular cycle.

- The maintenance loop's job is to make the SLA boring: the weekly triage (§1)
  reviews scanner/advisory findings alongside update PRs, so most patches
  land as routine updates long before their deadline.
- The release-age delay (§1) does **not** apply to security patches — the SLA
  clock outranks it.
- A missed SLA is reported to the user like a gate failure (see the SKILL.md
  rule). The quarterly audit (§5) reviews SLA compliance as a trend: repeated
  misses in one tier mean the process, not the people, gets fixed.

## 4. Technical-debt management

Debt is not "code we dislike." It is work the system will force you to do
later, at a worse time, with interest. Managed debt is a financing tool;
unmanaged debt is a surprise.

- **One debt register** for the whole project (a file or tracker section —
  not scattered TODO comments). Every entry states: what the debt is, where
  it lives, what it costs (slower changes, incident risk, blocked features),
  and when it was taken on and why.
- **Classify each entry by type:** code/design debt, test debt, dependency
  debt (§1–§2), documentation debt, infrastructure debt. Classification is
  what makes the register sortable instead of a guilt list.
- **Estimate size simply:** a rough remediation cost in developer-days
  (0.5 / 1 / 3 / 10 — coarse on purpose). Precision is not the point;
  comparability is.
- **Order by hotspots first:** priority ≈ **complexity × change frequency**.
  Debt in code that is both tangled and touched every week charges interest
  daily; identical debt in code untouched for a year charges almost none.
  Pay down hotspots; let cold debt wait without guilt.
- **Standing paydown allocation:** reserve **15–20% of each cycle's capacity**
  for register items, chosen by the hotspot ordering. Debt work that waits
  for "a quiet period" waits forever — there is no quiet period. The
  allocation is small enough to survive busy cycles and large enough to
  compound.
- **Tag new debt at merge time:** reviewers (Gate 5b) name deliberate debt
  when they approve it — "this shortcut is acceptable if it enters the
  register today" — so debt is taken on as a recorded decision, never
  discovered later as an accident. Undocumented shortcuts found in the wild
  become register entries on discovery, without blame.

## 5. The periodic ops rhythm

Maintenance fails when it depends on remembering. It works when it is a
calendar. Minimum rhythm:

| Cadence | Ritual | Contents |
|---|---|---|
| **Weekly** | Dependency triage + error review | The §1 update queue merged or deferred with reasons; new vulnerability findings checked against the §3 SLA; the week's production errors/incidents skimmed for anything recurring that nobody filed |
| **Monthly** | Restore drill + cost review + access review | Restore the latest backup to an isolated environment and verify it (a failed drill is a P1 defect — see release-engineering §6); review cloud/service spend against last month and flag unexplained growth; review who/what still has access to production, admin panels, and secrets — remove what is no longer needed |
| **Quarterly** | DR test + dependency/EOL audit + SLO review | A fuller disaster-recovery exercise against the RPO/RTO commitments; the EOL inventory (§2) re-checked against endoflife.date with owners/dates confirmed; SLO targets and error-budget history reviewed — targets tightened, loosened, or re-instrumented deliberately, never by drift; patch-SLA compliance trend reviewed |

Every ritual produces a short written record (what was checked, what was
found, what became a task). A ritual with no record is assumed not to have
happened — the same evidence rule as every gate in this OS.

## 6. Feedback intake — the loop back to Gate 0

A running system generates work: user feedback, support reports, feature
requests, recurring complaints, your own monitoring insights. None of it
enters development by osmosis.

- **Collect in one place:** every signal lands in a single intake list,
  however it arrived (support channel, app-store review, user message,
  monitoring observation). Signals noted "somewhere in chat" are signals
  lost.
- **Triage on the ops rhythm:** the weekly slot (§5) also sorts new intake
  into: defect (route to the bug-fix path), small improvement (fast-lane
  candidate), real feature/change (→ Gate 0), or not-actionable (recorded
  with the reason — "won't fix" is a decision, not an omission).
- **Nothing bypasses the front door:** accepted feedback becomes work only
  by entering at **Gate 0** like any other task — clarified, specced, routed.
  A maintainer's favorite user request gets no shortcut past the gates; that
  is what keeps the feedback loop from becoming a second, shadow roadmap.
- **Close the loop with the source:** when feedback ships, note it in the
  release notes; when it is declined, the reason exists in the intake record
  if the user ever asks. People who report problems and hear nothing stop
  reporting — and their reports were free QA.
- **Watch the aggregate, not just the items:** the quarterly review (§5)
  also reads the intake list as data — the same complaint arriving ten times
  is a defect with ten reporters, and a theme across requests is product
  evidence for the BA's next discovery pass. Intake that is only ever
  processed item-by-item never gets to say the big thing it knows.
