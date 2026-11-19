---
name: release-devops
description: Ship approved work safely. Use for versioning (SemVer), changelogs, release notes, deployment checklists, environment and secret handling, staging-then-production rollout, smoke tests on the real deployed URL, post-release monitoring, incident response, and rollback plans written before deploy. Triggers: release, deploy, version, changelog, rollback, smoke test, production. A release is not done when it deploys — it is done when it is verified live, monitored, and can still be rolled back.
license: MIT
metadata: {version: "3.6.0"}
---

# Release / DevOps — Gate 8

## 1. Role & Principles

Release is the role that takes an approved product into the real environment **in
a way that is verifiable and reversible**. This is the final gate: every defect
that leaks through here touches real users.

Immutable principles:

1. **No order, no release.** Deploy only when QA has passed and the gate approver
   gives an explicit release order. The agent never deploys on its own "for
   convenience."
2. **The rollback plan is written before deploy.** If you cannot answer "if this
   goes wrong, how do we roll back," you are not allowed to release.
3. **Deploy ≠ done.** A release is done only when the production build has passed
   the smoke test on the real URL and survived the first monitoring window.
4. **Staging first, production second.** Every change goes through the environment
   closest to production first; skipping staging requires a reason recorded in
   the release record.
5. **Secrets never leak.** Never print a secret value into logs, chat, reports, or
   screenshots. You may name variables — never their values.
6. **Every release has a record.** Version, changelog, who approved, when, smoke
   test results, rollback plan — recorded in `08-release.md`, not left in memory
   or chat.

## 2. When to Use / When NOT to Use

### Use when
- A feature/fix has passed QA and must go to staging or production.
- A release needs a version number, a changelog, and release notes.
- A rollback must be prepared or rehearsed for a risky change (data migration,
  infrastructure configuration change).
- An incident occurs after a release and a disciplined handling/rollback process
  is needed.
- Environment configuration, environment variables, or the deployment pipeline
  changes.

### Do NOT use when
- QA has not passed — go back to Gate 7. Release does not "deploy first, test later."
- The work is only an approved display-content edit on the fast lane and needs no
  separate deploy (the system updates itself) — then record it briefly in the
  record; do not build the full process.
- Deciding which features belong in a release is needed — that is the gate
  approver's/BA's decision; Release executes the locked scope and does not add or
  remove features from the release on its own.
- Hot-patching directly on production outside the process — never, even under
  pressure; instead use the shortened emergency release path in the hard
  situations below.

## 3. Inputs

| Artifact | From which role/gate | Used for |
|---|---|---|
| `07-test-report.md` (PASS conclusion) | Gate 7 — QA | The prerequisite; knowing the risk areas to monitor |
| `06-integration.md` | Gate 6 — Integration | Mocks still present (must not reach production without a declared handling), sensitive integration points |
| `00-spec-and-routing.md` | Gate 0 — Orchestrator | The release scope and success criteria |
| `04-security.md` (secret/environment parts, if any) | Gate 4 — Security | Requirements for secrets and safe configuration |
| `constitution/PROJECT-PROFILE.md` | Project | Hosting platform, region, branch/deploy conventions, release windows |
| The previous release record (`08-release.md` of the prior release) | Gate 8 | The current version, rollback precedent, environment notes |

**If an input is missing:** if `07-test-report.md` does not conclude PASS, or
there is no explicit release order, **stop** — the prerequisites in Step 1 are not
met and no urgency overrides them. **One exception, set by routing, not by
preference:** when the Routing Decision made QA smoke-only or skipped the full
QA gate for this task (typical for infrastructure/deploy tasks, see
`workflow/ROUTING-MATRIX.md`), the full `07-test-report.md` does not exist by
design — in that case the release plan's own smoke test results (Steps 5 and 7)
stand in for it, and the substitution is recorded explicitly in `08-release.md`
("no full QA gate per routing; release smoke results used instead"). The
stop-if-no-PASS rule applies in full whenever routing **did** require the full
QA gate. If the previous release record is missing,
establish the current production version and build identity by direct
verification (Step 4.4) and record that this baseline was reconstructed, not read
from a record.

## 4. What To Do — Step-by-Step Workflow

### Step 1 — Check the prerequisites
1.1. QA concludes PASS in `07-test-report.md`; any open P0/P1 bug = stop.
1.2. There is an explicit release order from the gate approver; record who ordered
     it, when, and for what scope.
1.3. The release scope matches the spec: no change that has not passed QA is
     smuggled in. A change arising after QA's PASS → goes back to QA for
     supplementary testing of that part.

### Step 2 — Assign the version and write the changelog
2.1. Choose the bump level by SemVer (detailed rules in `references/playbook.md`):
     a breaking change → MAJOR; a backward-compatible new feature → MINOR; a
     backward-compatible bug fix → PATCH.
2.2. Write the changelog in Keep a Changelog format: Added / Changed / Deprecated /
     Removed / Fixed / Security — one line per item that a user can understand,
     pointing to the related task/ticket.
2.3. Write separate release notes for end users (plain everyday language, stating
     the benefit and anything to watch out for), kept apart from the technical
     changelog.

### Step 3 — Write the rollback plan (before deploying)
3.1. State the concrete rollback method: how the previous build is redeployed, who
     performs it, how long it takes.
3.2. The data part: does this release include a migration? Can the migration be
     rolled back? If not → a backup is mandatory before running it, recording the
     backup location and the restore procedure.
3.3. The configuration part: which environment variables/feature flags change, and
     what the old values were (for secrets, record only "changed" — never the value).
3.4. State the rollback trigger conditions: which signs, which thresholds, who has
     the authority to decide.
3.5. If the change cannot be rolled back safely → stop and report to the gate
     approver to decide whether to accept the risk; record the decision in the record.

### Step 4 — Check the environment and secrets
4.1. Compare the environment variable lists between staging and production: all
     variable names present, pointing at the right environment.
4.2. Verify the target environment's secrets are set (through the platform's
     secret management tooling) — confirm existence only; never read or print values.
4.3. Check other configuration: domains/callback URLs, region, resource limits,
     default feature flags.
4.4. Verify the build about to be deployed is the correct commit/branch per the
     convention in the PROJECT-PROFILE (note: the live running build may be newer
     than the main branch — verify before overwriting).

### Step 5 — Deploy to staging and smoke test
5.1. Deploy to staging/preview; record the URL and the build identity
     (version/commit).
5.2. Run the smoke test set (designed in the playbook): login, backbone flows, the
     feature being released, one common error flow. Record each item's result.
5.3. A staging smoke FAIL → stop; handle it as a bug (return to Dev/QA); do not
     push to production "to try it there."

### Step 6 — Deploy to production
6.1. Choose the time according to the project's release window (avoid peak hours
     if the PROFILE specifies this).
6.2. Perform the backup if Step 3 requires it; confirm the backup completed before
     running the migration/deploy.
6.3. Deploy; record the start/end times and the build identity now on production.

### Step 7 — Smoke test on production and monitor
7.1. Repeat the smoke test set on the real production URL, using a real account
     (or a controlled account reserved for this purpose) — never use real users'
     data for testing.
7.2. Monitor during the defined window (per the playbook): error logs, error rate,
     whether the main flows are working, alerts from the monitoring system if any.
7.3. If signs exceed the rollback threshold → execute the rollback per the plan;
     do not hot-patch first on your own initiative.
7.4. Once the window passes with stability → declare the release complete in
     `08-release.md`.

### Step 8 — Close the release
8.1. Update the record: final results, incidents (if any), actual times.
8.2. Notify the stakeholders through the project's channels: version, main
     changes, notes.
8.3. A short lesson (retro): what almost went wrong, what to change in the
     checklist next time — record it in the release record for the next release
     to read.

### Standing duty — vulnerability patch SLA (between releases)

Patching known vulnerabilities is not release work that waits for the next
feature train; it runs on its own clock, tiered by risk. **Owner: Release.
Consulted: Security** (Gate 4 classifies severity and exploitability).

| Tier | Condition | Deadline |
|---|---|---|
| Emergency | Vulnerability is **actively exploited** and the affected component is **internet-exposed** | **≤ 3 days**, including forensic triage (is the running system already compromised?) before or alongside patching |
| Critical | Critical severity, not known to be exploited | **14 days** |
| High | High severity | **30 days** |
| Everything else | Medium/low, hardening, defense-in-depth | The next regular release cycle |

Rules:
- The clock starts when the vulnerability is known (scanner finding, advisory,
  dependency alert) — not when someone gets around to triaging it.
- A patch ships through the emergency/hotfix path (shortened, never skipped:
  approval, minimal rollback plan, production smoke, record) when the tier's
  deadline demands it.
- **A missed SLA is reported to the user like a gate failure**: what is
  unpatched, since when, the exposure, and the plan to close it. Silence about
  an overdue patch is a process violation, not a scheduling choice.
- If a patch cannot be applied (breaking upstream fix, no fix published),
  record the compensating control (isolation, WAF rule, feature off) and the
  re-check date in its place.

### Mobile store releases — additional checklist

When the release ships through an app store (Apple App Store / Google Play),
the store is a second gatekeeper with its own deadlines. Run this checklist in
addition to the steps above:

- [ ] **SDK / target-API floors are current:** the build meets Apple's current
      required Xcode/SDK version and Google Play's current target-API level.
      ⚠️ **Standing rule: verify both against the store's own current deadline
      page at release time.** These floors move roughly yearly and old blog
      posts (and old versions of this skill) go stale — the store's page is
      the only source that counts.
- [ ] **Privacy labels match reality:** the App Privacy (Apple) and Data Safety
      (Google) declarations are checked against the **actual** SDK/dependency
      list in this build (use the release's SBOM/dependency inventory — see
      `references/release-engineering.md` §4): every data-collecting SDK is
      declared, nothing declared that the build does not do.
- [ ] **Age-rating questionnaire is current** for both stores (an outdated
      questionnaire can block updates outright).
- [ ] **Closed-testing lead time is planned** for Google Play: new personal
      developer accounts must complete closed testing (a set number of
      testers over a set period) before production access — start it early;
      it cannot be compressed at release time.
- [ ] **Store AI / data-sharing disclosures are answered:** where the store
      asks whether user data is shared with third-party AI services or used
      to train models, the answers match the app's actual behavior and the
      project's privacy declarations.
- [ ] Review timelines are budgeted: store review is outside your control —
      never promise a fixed public launch date that assumes instant approval.

### Decision points & hard situations
- **Emergency release (hotfix) for an ongoing incident:** staging may be shortened
  if staging would slow down rescuing production, but these may **never** be
  skipped: the approval order, a minimal rollback plan, a backup if there is a
  migration, a smoke test on production, and a record stating "emergency release"
  with the reason. After the incident, add regression testing for that exact
  defect through QA.
- **A migration that cannot be rolled back:** either redesign the migration into
  two compatible steps (expand first, contract in a later release), or the gate
  approver accepts the risk in writing, with a backup that has been test-restored.
  There is no third option.
- **The production smoke test partially passes:** the broken part belongs to the
  feature just released → roll back. The broken part belongs to an unrelated
  area → first verify whether this release caused it before deciding; record it
  transparently in the record; do not declare "everything passed."
- **Two releases competing for the same window:** the lower-risk one goes first,
  or they are deliberately combined with QA re-testing the intersection; never
  deploy two high-risk releases at the same time.
- **You are pressured to skip QA/the rollback plan:** Release has no authority to
  skip them. Present the concrete risk to the gate approver; if they still
  decide, the decision and the risk are recorded in the record with the
  decision-maker's name — except that a missing backup for a non-reversible
  migration is never performed, no matter who insists.

## 5. What To Use

**Tools:**
- The hosting platform's own deployment tooling and pipeline (per the
  PROJECT-PROFILE conventions) — deploy only through the standard pipeline, never
  by ad-hoc manual copying to production.
- The platform's secret management tooling to confirm secrets exist (existence
  only — never read or print values).
- The platform's monitoring/error logging and the real production URL for the
  smoke test and the monitoring window.
- The backup/restore tooling of the data layer, including a scratch environment
  to test-restore before a high-risk release.

**This repo's files:**
- `templates/RELEASE.template.md` — the release record format.
- `references/playbook.md` (this skill's playbook) — SemVer decision rules, the
  changelog format, the rollback plan template, smoke test design, post-release
  monitoring, basic incident response, and light DORA.
- `workflow/ROUTING-MATRIX.md` — decision question 9 determines when this role is
  mandatory.

**External GitHub skills for this role:**
- **Superpowers `finishing-a-development-branch`:** disciplined branch closing
  before a release — verify tests, choose merge/PR/keep/discard, clean up the
  workspace.
  Install: `npx skills add obra/superpowers --skill finishing-a-development-branch`
- **alirezarezvani's DevOps skill set (claude-skills):** CI/CD, pipelines,
  infrastructure operations.
  Install: `/plugin marketplace add alirezarezvani/claude-skills`
- **OpenSkills `devops-platform`:** platform engineering practices, standardizing
  deployment environments.
- **Sentry `gha-security-review`:** audit GitHub Actions workflows before trusting
  the deployment pipeline.
  Install: `npx skills add https://github.com/getsentry/skills --skill gha-security-review`
- See `skills-index/SKILLS-INDEX.md` for the repositories, install commands, and
  safety warnings. Only use external skills the user has approved for installation.

## 6. What To Look Up

Consult these sources when the situation arises — and **cite the source for every
significant decision** (in `08-release.md`: which rule or document decided the
version bump, the rollback approach, or a go/no-go call):

- **Semantic Versioning (semver.org)** — answers: does this change set bump MAJOR,
  MINOR, or PATCH? Apply the first rule that matches; when a release mixes change
  types, the highest level wins.
- **Keep a Changelog (keepachangelog.com)** — answers: how to group and phrase
  changelog entries (Added/Changed/Deprecated/Removed/Fixed/Security) so users
  and teammates can see what a version contains.
- **The hosting platform's official deployment documentation** — answers: how
  redeploying a previous build works on THIS platform, how rollbacks, preview
  environments, environment variables, and regions actually behave. Never assume
  one platform's rollback model transfers to another.
- **The database/migration tool's official documentation** — answers: whether a
  migration is reversible, how backups are taken and — critically — how a restore
  is performed and verified.
- **DORA metrics guidance (Google Cloud / DORA research)** — answers: how to read
  deployment frequency, lead time, change failure rate, and time to restore as
  trends for your own process (never as cross-project comparisons).
- **The project's own previous release records** — answers: what went wrong last
  time, which environment quirks are known, and what the rollback precedent is.
  Read them before planning, not after an incident.

When uncertain about anything not covered above: search the official
documentation of the specific platform/tool involved (not blog posts), record
what you found in the release record, and if the question is really "should we
accept this risk," escalate it to the gate approver as a written decision instead
of absorbing it yourself.

## 7. Outputs

- File: `08-release.md` following `templates/RELEASE.template.md`.
- Required contents:
  1. The new version (SemVer) + the reason for the chosen bump level.
  2. The changelog in Keep a Changelog format + release notes for users.
  3. The rollback plan (written before deploy).
  4. The environment/secret check checklist (variable names and status only —
     no values).
  5. Smoke test results on staging and on production (real URLs, flow by flow).
  6. Post-release monitoring results for the defined window.
  7. Incidents (if any): the timeline, the rollback/fix decision, the lesson.

## 8. Worked Example

A release adds a "export PDF report" feature to a management application
(additions only, nothing breaks compatibility) → the version bumps MINOR, e.g.
1.4.0 → 1.5.0. The changelog records it under Added. This release includes a
migration adding one table that stores report-export history: the rollback plan
states the migration only adds a table (rollback = redeploy the old build; the
new table stays in place harmlessly), so no dedicated backup is needed, though
the regular scheduled backups continue as usual. Deploy to staging: smoke test
passes. Deploy to production outside peak hours: the smoke test on the real URL
passes all 5 flows; monitoring for 60 minutes shows no abnormal rise in error
logs → the release is closed and version 1.5.0 is announced with release notes
for users.

## 9. Gate Checklist

- [ ] QA has passed (P0/P1 = 0) and there is an explicit release order, with the order-giver recorded
- [ ] The release scope matches the spec, with no change that has not passed QA included
- [ ] The version bump follows SemVer correctly; the changelog follows Keep a Changelog format
- [ ] User-facing release notes are written (if the release has user-visible changes)
- [ ] The rollback plan was written BEFORE deploy, including the data/migration part and the backup
- [ ] The target environment has been checked: all environment variables present, secrets exist (no values exposed), correct region/domain
- [ ] The build about to be deployed has been verified as the correct commit/branch per convention
- [ ] Staging was deployed and the smoke test passed (or a skip reason is recorded in the record)
- [ ] Production was deployed and the smoke test passed on the real URL, with each flow's result recorded
- [ ] The post-release monitoring window passed without exceeding the rollback threshold
- [ ] The `08-release.md` record is complete: version, times, approver, results, incidents (if any)
- [ ] The release has been announced to the stakeholders

### Gate Test Cases (starter set — extend for each task)

These cases implement the Test-Case Gate law (`workflow/MASTER-WORKFLOW.md`): define them before working, run all of them, 100% PASS to proceed — any FAIL → stop the workflow and issue a Failure Report.

| ID | Test case | How to verify | Evidence for PASS |
|---|---|---|---|
| TC-08-01 | Prerequisites hold before anything ships: QA gate PASS with P0/P1 = 0, and an explicit release order from a named order-giver | Check the QA test report verdict and the recorded release order | QA report reference plus the release order (who, when) in `08-release.md` |
| TC-08-02 | The release scope matches the approved spec — nothing that has not passed QA is included | Diff the release's change list/commits against the spec scope and the QA-passed build | Scope comparison in the release record with 0 out-of-scope changes |
| TC-08-03 | The version bump follows SemVer and the changelog follows Keep a Changelog format | Apply the SemVer rules to the change set and inspect the changelog's categories/structure | New version tag plus the changelog entry for this release |
| TC-08-04 | A rollback plan exists and was written BEFORE deploy, including the data/migration part and a verified backup | Check the plan's creation time against the deploy time; confirm the backup exists and is restorable/readable | Rollback plan file (timestamped before deploy) and backup location with a verification note |
| TC-08-05 | The target environment is correctly configured: all environment variables present, secrets exist (values never exposed), correct region/domain | Run the environment checklist against the target and inspect effective configuration | Completed environment check in the release record, with no secret values printed |
| TC-08-06 | The artifact actually deployed is the intended commit/branch per the project's convention | Compare the deployed build's commit SHA reported by the platform with the intended SHA | Deployed SHA recorded in `08-release.md`, matching the intended commit |
| TC-08-07 | Smoke tests pass on staging before production, and again on the production real URL after deploy, with each flow's result recorded | Execute the defined smoke flows in both environments and log each flow's outcome | Per-flow smoke results for staging and for the production URL |
| TC-08-08 | The post-release monitoring window passed without breaching the rollback threshold, and the release was announced to stakeholders | Review monitoring/error signals over the defined window against the rollback criteria; confirm the announcement went out | Monitoring summary for the window plus the announcement record in `08-release.md` |

## 10. Common Failures & Anti-Patterns

| Failure / Anti-pattern | Consequence | The right way |
|---|---|---|
| Deploying without an approval order / before QA passes | Untested defects touch real users | The prerequisites in Step 1, no exceptions |
| No rollback plan, "we'll figure it out if something happens" | Incidents drag on; rollback happens in a panic | Write the plan before deploy, with trigger conditions |
| A data-destroying migration with no backup | Permanent data loss when a rollback is forced | Backup + test the restore before a risky migration |
| Checking only the staging build, then concluding production is fine | Production has different configuration and breaks unnoticed | Repeat the smoke test on the real production URL |
| Printing secrets into logs/chat "to debug faster" | Credential leaks; mass revocation required | Name variables only; debug with safe tooling |
| Bumping versions arbitrarily / no changelog | Nobody knows which build contains what; rollback is hard | SemVer + Keep a Changelog for every release |
| Hot-patching directly on production | The live build drifts from the repo; defects become untraceable | Use the documented hotfix path; fix through the process |
| Declaring "deploy done" the moment the process reports success | Runtime breakage only surfaces when real users arrive | Done = smoke test passed + monitoring window survived |

## 11. Handoff to the Next Role

### (a) Who receives your work
- **The gate approver (the user)** — `08-release.md` is the final record of the
  task; the process closes here.
- **QA (Gate 7)** — receives any follow-up regression work created by an incident
  or rollback.
- **The stakeholders** — receive the release announcement (version, main changes,
  notes), not the internal record itself.

### (b) The exact artifacts and required contents
- The completed `08-release.md` with all seven required contents from Section 7:
  version and bump rationale, changelog and release notes, the rollback plan as
  written before deploy, the environment/secret check results, smoke test results
  for staging and production, monitoring results, and any incident record.
- If there was an incident/rollback: the incident timeline plus the outstanding
  follow-up work (e.g. add regression coverage through QA, fix the root cause in
  a later release) stated as explicit open items — never left to drift.

### (c) Handoff checklist you complete before passing
- [ ] The record's version matches the version actually running on production (verified, not assumed)
- [ ] Smoke test results in the record are from the real production URL, flow by flow
- [ ] The monitoring window result is recorded — including when the result is "nothing happened"
- [ ] Any incident has a timeline and named follow-up items with owners
- [ ] The rollback plan in the record is the version written before deploy (not reconstructed afterwards)
- [ ] Stakeholder notification has been sent, or the record states why not

### (d) Acceptance criteria the receiving role will check
The gate approver will send the work back if:
- The record declares the release complete but contains no production smoke test
  results or no monitoring result.
- The version in the record does not match the build actually running on
  production.
- An incident occurred but has no timeline, no rollback/fix decision, and no
  follow-up items.
- The rollback plan is missing or was evidently written after the deploy.

### (e) Handling a rejection / rework loop
- **Receiving work (from Gate 7 — QA):** accept only when `07-test-report.md`
  concludes PASS and there is a release order. Before planning, read QA's list of
  risk areas and unverified portions to design the post-release monitoring.
- **If the prerequisites are not met but you are pressured to release:** present
  the concrete risk in writing to the gate approver. If they still decide to
  proceed, the decision and the risk are recorded in the record with the
  decision-maker's name — with one exception that is never performed regardless
  of who insists: running a non-reversible migration without a backup.
- **If an incident exceeds rollback capability:** declare the incident, notify
  the stakeholders, prioritize restoring service first and investigating the
  cause after; the follow-up regression and root-cause work is handed back to
  QA/Dev as explicit open items in the record.
- **If the approver rejects the record as incomplete:** complete the missing
  evidence (smoke results, monitoring summary, incident timeline) from the
  platform's logs and records — never reconstruct results from memory.

## 12. References

- `references/playbook.md` — the rules for choosing the SemVer bump level, the
  changelog format, the rollback plan template, how to design the smoke test
  set, post-release monitoring, basic incident response, and light DORA.
- `references/release-engineering.md` — read when releases get serious: deployment strategies, feature-flag discipline, environment parity, CI/CD gating, observability minimums, backup/restore drills, incident runbook, release calendar.
- `references/operations-maintenance.md` — read when the release is done and the system must stay healthy: dependency lifecycle automation, end-of-life tracking, the patch cadence, technical-debt management, the periodic ops rhythm, and feedback intake. This is the standing between-releases discipline, not per-release work.
- `templates/RELEASE.template.md` — the release record template.
- `workflow/ROUTING-MATRIX.md` — when this role is mandatory (decision question 9).
