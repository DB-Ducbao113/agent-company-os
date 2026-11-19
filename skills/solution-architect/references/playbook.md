# Playbook — Solution Architect (deep reference)

> The extension of `SKILL.md`: C4 in detail, ADRs, the API contract rule set, data modeling & migration safety.

## 1. The C4 Model — When to Use Each Level

| Level | Name | What it draws | When it is needed | When you may stop |
|---|---|---|---|---|
| 1 | System Context | The system in the middle, the actors and external systems around it, and the relationships between them | The task adds a new actor/external system; non-technical people need the big picture | Small system, external relationships unchanged |
| 2 | Container | The independently running/storing blocks: web app, mobile app, API, worker, DB, cache, external services + the protocols between them | **The default for most tasks with structural change** | — (this is Gate 2's minimum level) |
| 3 | Component | Inside one container: its main components and their relationships | A container changes heavily, several teams work inside one container, internal boundaries are contested | Small container / one person builds it, boundaries already clear |
| 4 | Code | Class diagrams / code detail | Almost never drawn by hand — let the code and in-code documentation speak | Skipped by default |

Rule: a diagram must state its date + the task scope; a diagram drawn for this task does not automatically become "the whole system's architecture" unless it truly covers everything — state the coverage clearly so later readers do not misread it.

## 2. ADRs — Writing Guide

**An ADR is mandatory when:** choosing/changing an external service or vendor · the authentication/authorization mechanism · the primary data-storage strategy · splitting/merging a module or service · deviating from the stack/design system settled in PROJECT-PROFILE · any decision that would be "expensive to change later".

**The structure of a good ADR:**
1. **Context:** the facts and constraints that force a decision *now* (never write generic background).
2. **Decision:** 1–3 sentences, in the present tense, with no vague conditions ("We use X for Y").
3. **Alternatives considered:** each alternative in 2–4 lines: pros/cons against this project's own criteria + the reason it was rejected. An ADR with no rejected alternative is usually an ADR written to rubber-stamp.
4. **Consequences:** what is gained, what price is paid, what extra work follows, and the **revisit condition** (the threshold/event at which this decision should be reopened).

**Lifecycle:** Proposed → Accepted / Rejected. When an Accepted ADR is replaced, the new ADR states "Supersedes ADR-xxxx" and the old one changes status to Superseded (only the status line changes — its content is never edited).

**Numbering:** continuous per project (ADR-0001, 0002, …), never renumbered per task; one registry/index lists every ADR + its status for quick lookup.

## 3. API Contracts — The Design Rule Set

### 3.1 Global conventions to settle once in the contract
| Topic | Rule |
|---|---|
| Error format | Every error uses one frame: `{ error: { code, message, details? } }`. `code` is a stable constant (SCREAMING_SNAKE); `message` is human-readable and **its wording may change** |
| HTTP status | Use the true meanings: 400 malformed · 401 unauthenticated · 403 not permitted · 404 not found (or deliberately not revealing existence) · 409 state/data conflict · 422 well-formed but violates a business rule · 429 rate-limited · 5xx server-side fault |
| Time | Store and transmit absolute UTC instants (ISO-8601 with offset/Z). Rendering in the user's timezone is the display side's job; never transmit a local-time string without its timezone |
| Naming | Fields use one consistent convention across the whole API (usually camelCase in JSON); a field name never changes meaning between endpoints |
| Null vs. absent | Settle it explicitly: a non-applicable field is absent or null — consistently, and recorded in the contract |

### 3.2 Versioning
- Default: version in the path (`/api/v1/…`) for an API under development with several consumers.
- A **breaking** change (removing/renaming a field's meaning, changing an error code, tightening validation) = a version bump or a deprecation path with dates; a **compatible** change (adding an optional field, adding an endpoint) does not bump the version.
- The contract contains a "Versioning policy" section + how end-of-support for old versions is announced.

### 3.3 Pagination, filtering, sorting
- Lists are always paginated: prefer **cursor-based** pagination for large/fast-changing data; offset-based is acceptable for small, slowly changing lists — pick one style and record the reason.
- List responses have one consistent structure: `{ items: [...], nextCursor | total, pageSize }`.
- Filter/sort parameters are listed explicitly in the contract (never "filter by any field"); the default sort must be stable (with a unique tie-breaker, e.g. id).

### 3.4 Idempotency & operations that are unsafe to retry
- Every operation that creates an important record or deducts money/quota: requires an `Idempotency-Key` (client-generated; the server stores the result under the key for a settled time window); re-sending the same key → returns the original result, never creates a second record.
- "Set the target state" updates (PUT/PATCH with the target value) are naturally idempotent — prefer this style over "increment/decrement" operations without conditions.
- The contract must state the behavior when the client times out and retries: is the retry safe, and by what mechanism?

### 3.5 Auth & permissions in the contract
- Every endpoint states: whether authentication is required, which role/permission, and the permission over *the data* (own records only / same organization / everything) — data-level permission is the part most often missed.
- Errors distinguish 401 (unauthenticated) from 403 (authenticated but not permitted); consider 404 instead of 403 when the existence of a resource must not be revealed — this decision is recorded in the contract and kept consistent with Security.

### 3.6 Pre-sign-off contract review (quick scan)
- [ ] Does every BA acceptance criterion have an endpoint serving it, including error cases?
- [ ] Does every endpoint have: auth, validation, a success response, error responses + codes?
- [ ] Is any error code used with two different meanings on two endpoints?
- [ ] Is there a field the FE needs that the response lacks (or conversely, a sensitive field exposed unnecessarily)?
- [ ] Do create/deduct operations have a duplicate-protection mechanism?

## 4. Data Modeling & Migration Safety

### 4.1 Modeling principles
- Every entity: a primary key, and its integrity constraints (unique, not null, foreign keys) declared in the design from the start — "must not duplicate / must not be missing" rules belong to the DB; code is only the friendly layer.
- State (per the BA's state model) is stored in one explicit field; invalid transitions are blocked at the business layer **and** considered for a DB constraint when the rule is absolute.
- Index against the known main queries (list the queries at design time); do not index speculatively in bulk.
- Deletion: settle hard delete vs. soft delete against the project's business/legal requirements; this decision affects every query — record it in the arch file, never leave it for each developer to choose.
- Money fields: store integer minor units or the system's standard decimal type — never floating point; state the unit explicitly in the contract and the model.

### 4.2 Safe migration — the expand → migrate → contract pattern
| Phase | What happens | Why |
|---|---|---|
| 1. Expand | Add the new tables/columns in a backward-compatible form (nullable or with defaults); the old code still runs | New and old code can deploy side by side without breaking |
| 2. Migrate | Move/backfill the old data into the new structure in batches, with before/after counts | Errors surface in the data early, before users are affected |
| 3. Switch | Code reads/writes move to the new structure; monitor | There is still a path back to the old structure if a defect appears |
| 4. Contract | Only a later release removes the old columns/tables and tightens not-null | Deletion is irreversible — keep it separate from the behavior change |

### 4.3 Checklist before running a migration on real data
- [ ] A backup exists and **the backup has been test-restored** (a backup never restore-tested = no backup)
- [ ] Estimated affected row count + run time; does a long migration need batching / an off-peak window?
- [ ] Is the script idempotent (running it twice does not corrupt data)?
- [ ] A post-run verification step exists: row counts, before–after totals (sum/count) reconciled, random sampling checked
- [ ] Rollback for each step is written as concrete commands, not a generic "restore the backup if needed"
- [ ] The deployment order of code ↔ migration is recorded: which goes first, and how long the incompatibility window lasts

### 4.4 Common edge cases
- **Two app versions writing data simultaneously** during the deployment window: the new structure must accept both old and new writes, or there is an approved short write-freeze plan.
- **Dirty legacy data** (duplicates, missing values, malformed formats): the backfill needs a rule for bad records — count them, quarantine them, report them — instead of halting mid-way or silently skipping them.
- **Clocks & timezones:** timestamps generated on the client are untrustworthy; business-critical moments use server time, stored as UTC.
- **Growth scale:** estimate the data volume after 12 months for a new table; if it grows fast, settle the storage/partitioning strategy in the design now instead of leaving it to become an operations incident.

## 5. NFRs — Turning Non-Functional Requirements into Design Decisions

| NFR | The question that must have a (numeric) answer before designing | The decisions it drives |
|---|---|---|
| Performance | What response time is acceptable, at which percentile (p50/p95)? Measured where? | Caching, indexes, pagination, synchronous vs. asynchronous |
| Load | Expected concurrent users/requests; how many times normal is the peak? | Queues, rate limits, read/write splitting |
| Data volume | Current volume + 12-month growth? | Data model, storage, cold storage |
| Availability & recovery | How much downtime is acceptable, and how much data loss at most (RTO/RPO)? | Backups, multi-region deployment, rollback |
| Security & privacy | Which data types are sensitive, which compliance requirements apply? | Encryption, permissions, audit logs (handed to Security) |
| Operating cost | Monthly infrastructure/external-service budget? | Choosing services; how much to build vs. buy |

Rule: an NFR without a number is recorded as an `[ASSUMPTION]` together with the chosen default number and how it will be verified at Integration/QA — NFRs never remain as adjectives ("fast", "stable", "flexible") in the arch file.
