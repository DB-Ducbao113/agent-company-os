# Review by Change Type — Deep Dive

> Read when: a diff arrives. Identify its type(s) below, then run those checklists on top of the general review order in `playbook.md`.
> A diff often has several types at once (a migration + an API change + a config change). Apply every matching section.

## Identify the change type(s) first

| Signal in the diff | Section |
|---|---|
| Files under a migrations folder, DDL, model/schema definitions | (a) |
| Endpoint signatures, request/response shapes, DTOs, API version folders | (b) |
| Middleware/guards, role checks, token/session logic, permission tables | (c) |
| Components, styles, tokens, layout, copy in UI files | (d) |
| Lockfile churn, package manifest version changes | (e) |
| `.env` examples, CI/workflow files, feature flags, infra config | (f) |
| Large deletions, moved files, "cleanup" in the description | (g) |
| Branch named hotfix, incident referenced, unusually small diff under time pressure | (h) — plus every other matching section, compressed |

## (a) DB Migration / Schema Change

Scrutinize:
- [ ] Reversibility: is there a working down-migration, or an explicit, approved "irreversible — backup taken at [time]" note?
- [ ] Data safety on EXISTING rows: new NOT NULL column without a default/backfill breaks or corrupts production data — the local empty-DB test proves nothing
- [ ] Lock behavior: does it rewrite/lock a large table during deploy? Is there a batched/backfill-offline plan?
- [ ] Expand–contract discipline: additive change first (new column/table), deploy code that tolerates both, backfill, then remove the old — in separate releases for anything risky
- [ ] Constraint intent: unique/FK/check constraints match the business rules in the BA artifact, not just the developer's model of them
- [ ] Index impact: new query patterns have indexes; dropped indexes are proven unused

Classic defects: migration that passes on an empty dev DB and fails on production data; a rename done as drop+add (data silently destroyed); backfill inside the migration transaction timing out; two migrations with the same version/timestamp from parallel branches.

## (b) API Contract Change

Scrutinize:
- [ ] Backward compatibility: every change classified — additive (new optional field/endpoint = compatible) vs. breaking (removed/renamed field, type change, new required field, changed error code/status, tightened validation)
- [ ] Breaking changes have a versioning/deprecation story and named consumers who agreed — "the frontend is ours too" still counts: old app versions in the wild consume this API
- [ ] The contract artifact (`02-api-contract.md`) was updated in the same change, or the diff and the contract now disagree
- [ ] Error format consistency: new endpoints return the shared error shape and stable codes
- [ ] Pagination, filtering, and idempotency conventions followed, not reinvented per endpoint

Classic defects: renaming a response field the mobile app already reads; changing a field's type (`"5"` → `5`) that strict clients reject; an error that used to be 404 becoming 403 and breaking client handling; a "small" validation tightening that rejects data existing clients legitimately send.

## (c) Auth / Permission Change

Scrutinize — this is the highest-blast-radius change type; slow down:
- [ ] The permission matrix (Gate 4 artifact) is updated and the diff implements exactly it — no extra grants "for convenience"
- [ ] Enforcement is server-side on every affected endpoint, including the boring ones (exports, history, search) — not only the endpoint named in the task
- [ ] Default is deny: new roles/permissions start with nothing and gain explicitly
- [ ] Negative cases are tested: the diff includes (or QA has) tests for the FORBIDDEN paths, not only the allowed ones
- [ ] Token/session implications handled: does a permission change take effect for already-issued sessions, and is that the intended behavior?
- [ ] Audit logging covers grants, denials of sensitive actions, and privilege changes

Classic defects: check added to the UI but not the API; admin check that trusts a client-sent role flag; permission added to the list endpoint but not the detail/export endpoints; tests that prove the allowed user succeeds and never prove the forbidden user fails.

## (d) UI / Visual Change

Scrutinize:
- [ ] Conformance to the design artifact: tokens (not raw hex/px), type scale, spacing — near-miss values are wrong values
- [ ] All states present: hover, focus-visible, disabled, loading, empty, error — not only the default state in the screenshot
- [ ] Accessibility: semantic elements, labels on icon-only controls, focus order sane, contrast in every state, touch targets sized per spec
- [ ] Numbers/labels use the right formatting (tabular figures where columns align, real data — never placeholder/fake data shipped as content)
- [ ] Responsive behavior at each range in the spec, checked at boundary ±1px
- [ ] No auto-detectable choice pushed onto the user (a manual toggle for something the app already detects is a design defect — flag it)

Classic defects: focus state removed because it "looked noisy"; loading state forgotten until the network is slow; error state styled but unreachable because errors are swallowed; a pixel-matched desktop view with a broken compact layout nobody opened.

## (e) Dependency Upgrade

Scrutinize:
- [ ] The changelog of the dependency was actually read: breaking changes, deprecations, and security fixes identified — "bump version" is not a review
- [ ] Scope discipline: one dependency (or one related family) per change; a diff that upgrades 14 packages hides which one broke things
- [ ] Lockfile changes are sane and included; no phantom upgrades of unrelated packages
- [ ] License and maintenance sanity for NEW dependencies: maintained? license compatible? could the standard library/existing deps already do this?
- [ ] Tests/build pass, and the risky surface the dependency touches was exercised (an auth library bump with only a build check is not verified)

Classic defects: major-version bump merged on a green build that fails at runtime; a new dependency duplicating an existing one; transitive dependency quietly changing behavior (date parsing, crypto defaults); abandonware added because it ranked first in search.

## (f) Config / Environment Change

Scrutinize:
- [ ] Which environments does this touch — dev only, or staging/production too? The diff must say, and prod changes get the same review weight as code
- [ ] No secrets in the diff (keys, tokens, passwords, connection strings) — a committed secret is an incident, not a comment thread
- [ ] Defaults are safe: if the new variable is missing in an environment, does the system fail closed or silently run in a degraded/insecure mode?
- [ ] Feature-flag changes state the rollout/rollback intent and the flag's owner + removal plan
- [ ] Region/timezone/locale assumptions made explicit (config that is correct in one region and wrong in another is a classic silent defect)

Classic defects: debug/verbose mode enabled in production config; a staging endpoint URL shipped in the prod config; timeout raised 100× to "fix" flakiness, masking the real bug; flag turned on for everyone at once with no rollback path rehearsed.

## (g) Deletion / Refactor

Scrutinize:
- [ ] **Dead-code proof:** for every deleted function/route/component — a search showing zero callers/references, including dynamic references (routes, config, templates, string-based lookups) that text search can miss
- [ ] Behavior preservation: characterization tests existed or were added before the refactor (see the Developer craft rules); the diff changes structure, not behavior — any behavior change hiding inside is split out and labeled
- [ ] No public surface removed silently: deleted endpoints/exports/events are breaking changes and follow section (b)'s rules
- [ ] Database/data touchpoints: deleted code that was the only writer/reader of a table or field is called out, with the data's fate decided explicitly

Classic defects: "unused" code that was invoked by a cron job, a webhook, or reflection; refactor that also "fixes" an undocumented quirk another feature depended on; deletion of the fallback path that production still needed twice a year.

## (h) Hotfix Under Time Pressure

The pressure is real; the review shrinks but never disappears.

May be deferred (recorded as follow-up tasks with owners):
- Refactoring for elegance, broader test coverage beyond the fixed path, documentation polish, non-critical performance tuning

May NEVER be deferred:
- A reproducing test (or at minimum a documented manual repro) for the bug being fixed
- The security check if the hotfix touches auth, permissions, money, or user data — pressure is exactly when these get broken
- A rollback path: how to undo this hotfix in minutes if it makes things worse
- Scope control: the diff fixes the incident and nothing else — no "while I'm here" changes riding along
- A second pair of eyes: hotfix review can be 10 minutes, but maker ≠ checker still applies

Classic defects: hotfix that fixes the symptom for one user cohort and breaks another (no regression check on adjacent paths); config hotfix applied to production by hand and never committed, so the next deploy resurrects the bug; the follow-up tasks never created, so "temporary" becomes permanent.

## Comment Bank — 10 Example Comments (label → location → consequence → suggestion)

1. **[BLOCKER]** `migration 0042, line 18` — Adding `NOT NULL` without a default will fail on the production table, which already has ~40k rows. → Add the column nullable, backfill, then set the constraint in a follow-up migration.
2. **[BLOCKER]** `POST /appointments, handler` — There is no ownership check before the update; any authenticated user can modify another user's appointment by ID (BOLA). → Enforce the Gate 4 permission check server-side and add the forbidden-path test.
3. **[BLOCKER]** `config/prod.yaml` — This diff contains a live-looking API secret. → Remove it, rotate the secret now (history keeps it), and load it from the environment instead.
4. **[SHOULD FIX]** `BookingList.tsx, render loop` — This issues one request per row (N+1); the page will degrade linearly as bookings grow. → Batch the fetch or include the relation in the list query.
5. **[SHOULD FIX]** `payment service, webhook handler` — The handler trusts the browser redirect to mark orders paid; a forged return marks unpaid orders as paid. → Treat only the signature-verified webhook as truth, per the security artifact.
6. **[SHOULD FIX]** `Button component` — The focus-visible state from the design spec is missing; keyboard users get no visible focus. → Restore the spec's focus token/styles before merge.
7. **[SHOULD FIX]** `user serializer` — The response now includes `internal_flags`, which the contract does not list and clients do not need. → Shape the response to the contract's field list.
8. **[NIT]** `utils/date.ts` — `fmt` is used in three files with three meanings. → Rename to `formatSessionTime` for the next reader.
9. **[NIT]** `test file` — This test's name says "rejects expired code" but it asserts the happy path. → Align the name with the assertion so failures are readable at 2 a.m.
10. **[QUESTION]** `session timeout change 24h → 30d` — This lengthens the session far beyond the Gate 4 decision; was that intentional and approved there? → If yes, link the updated security artifact; if not, revert to the agreed value.

## Severity Calibration

| Label | Meaning | Merge rule | Calibrating examples |
|---|---|---|---|
| **[BLOCKER]** | Will break production, lose/corrupt data, open a security hole, or violate the spec/contract | Must be fixed and re-reviewed before merge — no exceptions, including hotfixes | Unowned-object access allowed; migration destroys data; secret committed; contract field renamed silently |
| **[SHOULD FIX]** | Real defect or risk that will hurt soon: correctness edge case, missing required state, performance trap, missing negative test | Fix before merge, or merge only with a tracked follow-up + owner + reviewer agreement recorded | N+1 on a growing list; missing error state; forbidden-path test absent; response oversharing fields |
| **[NIT]** | Style, naming, readability — no behavioral impact | Author's choice; never blocks; keep them few and kind | Misleading variable name; test name/assertion mismatch; comment drift |
| **[QUESTION]** | Reviewer cannot tell intent from the diff | Blocks until answered — an unanswered question is an unreviewed area | Unexplained behavior change; config value changed with no reason; deleted fallback with no context |

Calibration rules:
- Severity is about **consequence if merged**, not about how wrong the author was. A one-line diff can be a BLOCKER; a 500-line diff can be all NITs.
- If everything is a BLOCKER, nothing is — inflating severity trains authors to ignore the label. Reserve it.
- A [QUESTION] that reveals a defect gets re-labeled to its real severity once answered.
- Disagreement on severity is resolved by evidence (reproduce it, measure it, cite the spec/contract line), not by seniority or stubbornness.

## Review Effort Calibration — How Deep to Go

Review depth scales with blast radius, not with diff size:

| Change profile | Minimum review depth |
|---|---|
| Copy/text, styling tokens, test-only changes | Fast pass: correctness of the text/values, no behavior change hiding inside |
| Standard feature code within one module | Full general order (playbook) + its change-type sections |
| Auth/permissions, money, migrations, config for production, public API surface | Deep pass: re-derive behavior from the artifacts, run or inspect the negative-path tests yourself, check every endpoint/object the change class touches — not only the ones in the diff |
| Hotfix | Compressed but complete on the never-defer list (section h); schedule the deferred remainder as a named follow-up review |

Two closing rules:
- **A review that found nothing is a valid outcome only if the review actually happened.** "LGTM" on a deep-pass change without evidence of the checks (tests run, artifacts compared) is an unverified claim — the verdict file should show what was examined.
- **Review the change that IS, not the change you wish it were.** Redesign suggestions beyond the task's scope go in as [QUESTION]/follow-up proposals, not as merge conditions — scope discipline protects the author's gate as much as rigor protects the product.
