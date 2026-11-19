# Playbook — Release / DevOps (deep reference)

Operational detail for the Release/DevOps `SKILL.md`: how to decide versions,
write changelogs, plan rollbacks, and handle the post-release phase.

## 1. SemVer — Rules for Choosing the Bump Level

Format: `MAJOR.MINOR.PATCH` (e.g. 2.3.1). Decide by the first question that
answers true:

| Question | If true | Bump |
|---|---|---|
| Will users/other systems break because of this change (API changed, a feature removed, a data format changed, environment requirements changed)? | Yes | **MAJOR** (2.3.1 → 3.0.0) |
| Is there a new feature/capability that is still backward compatible? | Yes | **MINOR** (2.3.1 → 2.4.0) |
| Is it only bug fixes and internal improvements, with no new feature and no compatibility break? | Yes | **PATCH** (2.3.1 → 2.3.2) |

Practical notes:
- Before 1.0.0 (the 0.x phase): anything may break; the convention is MINOR for
  features and PATCH for fixes, but breaking changes must be stated clearly in
  the changelog.
- A release containing several change types → take the highest level in the set.
- Changing behavior that users rely on (even without an API change) also counts
  as breaking in experiential terms — consider MAJOR, or at minimum highlight it
  prominently in the release notes.
- The release version must match everywhere it appears (the software package, the
  "about" screen, the release record) — a version mismatch between places is a
  record defect to fix before closing the release.

## 2. Changelog — Keep a Changelog Format

```markdown
# Changelog
All notable changes to this project are recorded here.
Format follows Keep a Changelog; versions follow SemVer.

## [Unreleased]

## [1.5.0] - 2026-01-15
### Added
- Export PDF reports from the monthly report screen.
### Changed
- The invoice list loads faster with large data sets.
### Fixed
- Wrong total displayed when an order had a 100% discount.
### Security
- Upgraded the image-processing library to patch a published vulnerability.
```

Writing rules:
- Fixed groups: Added / Changed / Deprecated / Removed / Fixed / Security. Omit
  empty groups.
- One line per item, written for a reader who is a colleague/technical user,
  stating the change and its effect — do not copy raw, cryptic commit messages.
- Removed items and breaking changes must stand out, with migration guidance if
  any exists.
- The `[Unreleased]` section collects changes during development; at release
  time it becomes a section with the version + date.

## 3. Rollback Plan — Template and Way of Thinking

```markdown
## Rollback plan — v1.5.0
- Rollback method: redeploy the v1.4.0 build through the standard pipeline.
- Estimated time: ~10 minutes. Performed by: the release operator on duty.
- Data: the migration only ADDS a new table; the old build does not read this
  table → rollback needs no data restore.
- Configuration: added the variable REPORT_STORAGE (already set in production).
  The old build does not use this variable → keep it in place on rollback.
- Rollback triggers: 5xx error rate > 2% in the first 15 minutes, or the report
  export flow fails completely, or corrupted data is detected.
- After rollback: keep the logs and any data generated, for investigation; do
  not rush to delete the new table.
```

Design principles for rollback-friendly migrations:
- **Expand first, contract later:** add the new column/table in release 1 (the
  old build can ignore it), move the data in between, and remove the old
  structure in a later release once the new build is stable. Avoid a migration
  that changes and deletes in a single release.
- A migration that renames/retypes a column holding data = high risk: a backup
  and a restore script are mandatory.
- Before a high-risk release, **test-restore** from the backup in a secondary
  environment — a backup that has never been test-restored is a belief, not a plan.

## 4. Designing the Smoke Test Set

A smoke test is the minimal check set that answers "is the system still alive and
are the main features still running" after each deploy. Selection criteria:
1. The main page/screen opens, with no blank error.
2. Login + logout (if there is auth).
3. The backbone value-creating flow — run one complete round with controlled data.
4. The feature just released — perform its main action once.
5. One important integration point (payment, notification, file upload…) at an
   alive/dead check level.
6. Reading old data from before this release (proves backward data compatibility).

Rules: the smoke set must finish within a few minutes; each item's result is a
clear pass/fail; the same set is used for staging and production (only the
URL/account differs); and **never** use real users' data for testing.

## 5. Post-Release Monitoring

| Item | How to monitor | Sample attention threshold |
|---|---|---|
| Error rate (5xx / application errors) | The platform's error logs/monitoring | A clear rise versus before the release, or exceeding the threshold in the rollback plan |
| Main flows | Periodic checks during the window + automatic alerts if available | Any backbone flow completely dead |
| Performance | Response times of the main pages/APIs | Sustained doubling versus the usual level |
| User feedback | The project's support/error-report channel | Multiple reports of the same symptom |

- Monitoring window: at minimum 30–60 minutes for a routine release; longer
  (several hours to a day) for a release with a migration or an infrastructure
  change. Record the chosen window in the record before deploying.
- The person monitoring must be someone with the authority and the ability to
  execute the rollback — monitoring without the ability to act does not count
  as monitoring.
- At the end of the window: record the summary result in the record, even when
  "nothing happened" (that is also a result).

## 6. Basic Incident Response

1. **Declare the incident:** record the detection time, the symptoms, and the
   estimated blast radius. Notify the stakeholders early, even before the cause
   is known.
2. **Prioritize restoring service:** if a rollback is feasible and the incident
   is serious → roll back first, investigate later. Do not debug on a burning
   production.
3. **Preserve evidence:** save the logs, timestamps, and related build identities
   before they are overwritten/deleted by their lifecycle.
4. **Timeline:** record the milestones (detected → declared → decision →
   restored) in the incident record.
5. **After the incident (post-incident):** analyze the root cause without blaming
   individuals; produce concrete remediation items (add tests through QA, add
   alerts, amend the release checklist) and record them in the release/incident
   record.
6. **Closing notification:** when the service is stable, notify the same parties
   who received the incident notice.

## 7. Light DORA (measure to improve, not to report)

Track only 2–4 numbers, recorded monthly, and watch the trend:
- **Deployment Frequency:** how many production releases in the month — steady,
  small, and frequent usually beats rare, huge batches for safety.
- **Lead Time for Changes:** from code approval to running in production — an
  abnormally long time usually comes from approval queues or environments, not
  from code.
- **Change Failure Rate:** the share of releases that cause an incident or need a
  rollback — the most important number for this gate; a continuous rise is the
  signal to tighten the checklist/smoke test.
- **Time to Restore:** from incident to restoration — measurable thanks to having
  a good rollback plan.

Never use these numbers to compare different projects against each other; only
compare against yourself over time.
