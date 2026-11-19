# Architecture Patterns — Catalog, Trade-offs, and Selection

> Companion to `references/playbook.md` (C4 levels, ADR guidance, API contract rules, data & migration safety).
> This file is the pattern catalog: what to choose, when, and at what cost — plus the selection method
> and the checks later roles use to verify the architecture actually held.

## 1. Structural patterns

| Pattern | Use when | Avoid when | Cost |
|---|---|---|---|
| **Layered monolith** (UI → service → data in one deployable) | Small team, one product, unclear domain boundaries, speed matters most | Independent scaling of parts is a proven need today | Lowest build/ops cost; risk: layers erode into a big ball of mud without module discipline |
| **Modular monolith** (one deployable, hard module boundaries, modules talk via interfaces/events only) | Default for most growing products: real domain structure, team of 2–15, future extraction possible | The organization cannot enforce boundaries (no review discipline) | Slightly more design effort than layered; buys the option to extract a module later at known seams |
| **Microservices** | Independent deploy/scale/team-ownership needs are **demonstrated**, different parts genuinely evolve at different speeds, org has platform capacity | As a starting point; small teams; unclear domain; no observability/CI maturity | Highest: distributed failure modes, eventual consistency, deployment & debugging overhead, data ownership splits |
| **Serverless functions** | Spiky/event workloads, glue between services, low steady traffic, per-invocation cost model fits | Long-running work, strict latency (cold starts), deep local state, vendor lock-in unacceptable | Cheap at low volume, expensive at sustained volume; debugging and local testing are weaker |
| **BFF (Backend for Frontend)** | Two+ clients (web/mobile/TV) with genuinely different data shapes; client teams blocked by generic API shape | One client, or differences are cosmetic (solve with query params/fields) | One more deployable per client; risk of business logic leaking into the BFF — keep it shaping/aggregation only |
| **Event-driven** | Loose coupling needed, reactions to facts ("order placed") fan out, audit trail valuable, load is bursty | The flow is fundamentally request/response and ordering is strict; team cannot operate brokers/dead-letter handling | Async debugging, ordering & duplicate-delivery handling, eventual consistency in UIs |
| **CQRS-lite** (separate read model, same service/DB) | Read patterns diverge hard from write patterns (complex reporting on transactional data) | Ordinary CRUD — a few indexed queries solve it | A read model to keep in sync (lag must be designed for); full CQRS with separate stores is a last resort, not a default |

**Why the default is NOT microservices.** Microservices trade code complexity for organizational complexity: network failure modes, distributed transactions, versioned contracts between every pair, per-service pipelines and observability. A monolith's failure modes are visible in one codebase and one deploy. The burden of proof sits on distribution: name the concrete force (independent scaling measured, team contention measured, compliance isolation required) — if the force is hypothetical ("we might need to scale"), build a modular monolith whose module seams are exactly where services would later split. Extract when the force is real; the seams make it a refactor, not a rewrite.

## 2. Integration patterns

**Sync vs. async decision table** — decide per interaction, not per system:

| Question | Points to sync (request/response) | Points to async (queue/event) |
|---|---|---|
| Does the caller need the result to continue? | Yes — user is waiting on it | No — fire-and-confirm is enough |
| Must failure be known immediately? | Yes (payment authorization) | Tolerable to learn later (email, indexing) |
| Is the downstream slow or unreliable? | It is fast and owned by us | Third-party, bursty, or flaky — buffer it |
| Ordering strict end-to-end? | Yes | Per-entity ordering suffices, or none needed |
| Volume pattern | Steady | Spiky — a queue absorbs the spike |

- **Queues** when: work must survive downstream outages, spikes need absorbing, or retries are natural. Always design: max retries, dead-letter queue + who inspects it, idempotent consumers (delivery is at-least-once in practice).
- **Webhooks** when: a third party must notify you of events. Always design: signature verification, idempotency on event ID, respond fast and process async, a reconciliation job for the notifications that never arrived.
- **Polling** when: the other side offers no push mechanism, or volumes are tiny. Poll with backoff, store a cursor/watermark, and treat polling as a deliberate cost (rate limits), not a default. Prefer push; poll as the fallback with a stated interval and owner.

## 3. Data patterns

- **Caching layers** — cache at the cheapest layer that solves the problem, in order: in-process memory (fastest, per-instance) → shared cache (Redis-class) → CDN/edge for static and public content → database query cache/materialized views. **Invalidation strategies**, pick per data type: TTL (staleness tolerable, simplest), write-through/invalidate-on-write (correctness matters, you own the writes), event-driven invalidation (multiple writers), cache-aside with versioned keys (safe default for mixed cases). Rule: every cache entry in the design names its invalidation strategy and its acceptable staleness — "we'll cache it" without both is a bug scheduled for later (see the classic stale-slot failure: a write path that forgot to invalidate).
- **Read replicas** — when read load measurably hurts the primary or reporting queries contend with transactions. Design for replication lag: route reads that must be fresh (read-your-own-write) to the primary; show the lag budget in the design.
- **Soft delete** — when recovery, audit, or legal holds matter. Costs: every query must filter, unique constraints need care (deleted rows still occupy values), and "deleted" must be defined for exports/backups. Hard delete when regulation demands erasure or the data has no recovery value — and record which rule applies per entity.
- **Audit tables** — append-only record of who/what/when for sensitive entities (money, permissions, health). Write audit rows in the same transaction as the change; never update or delete audit rows; decide retention up front.
- **Optimistic locking** — a version column checked on update ("UPDATE … WHERE version = ?"); a mismatch returns 409 and the user re-loads. Use for human-edited records with low contention. Pessimistic locks only for short, high-contention critical sections (inventory decrements) — and prefer atomic conditional updates at the DB level over application locks.

## 4. Auth architecture options

| Option | Shape | Use when | Watch out for |
|---|---|---|---|
| **Server session** (opaque ID in an HttpOnly cookie) | Server stores session state; instant revocation | Classic web apps, one backend, revocation matters | Needs shared session store when scaled horizontally; CSRF protection required |
| **JWT access token** (short-lived, stateless) | Client holds a signed token; APIs verify without a lookup | Multiple services/APIs verifying independently | Revocation is hard before expiry — keep lifetimes short, pair with a refresh token, plan a denylist only if truly needed |
| **OAuth 2.0 / OIDC** (delegate to an IdP) | Authorization-code flow (+PKCE for public clients) for login via Google/Microsoft/etc. or your own IdP | Social/enterprise login, SSO, not storing passwords yourself | Never use implicit flow; validate issuer/audience; account-linking rules (same email, two providers) are a BA question, not a library default |

**Where tokens live:** browser apps → HttpOnly, Secure, SameSite cookies for refresh/session (not `localStorage` — any XSS reads it); access tokens in memory for SPAs if tokens are unavoidable; mobile → OS secure storage (Keychain/Keystore). State the choice and its XSS/CSRF consequence in the design — "we use JWT" without a storage decision is an unfinished design.

## 5. Multi-tenancy models compared

| Model | Isolation | Cost shape | Use when |
|---|---|---|---|
| **Shared schema + tenant_id column** | Logical only — one wrong query leaks across tenants | Cheapest; one schema to migrate | Default for most SaaS; requires tenant scoping enforced in the data layer + tests (Gate 4 owns the leak tests) |
| **Schema per tenant** (one DB) | Medium — misrouting harder, migrations fan out | Medium; migration × N tenants | Tenants need some isolation or per-tenant restore, counts are modest |
| **Database per tenant** | Strongest — blast radius is one tenant | Highest ops cost; connection/fleet management | Regulated data, enterprise contracts, very large tenants |

Decide by the strongest tenant's requirement, not the average: one regulated tenant forces the model (or a hybrid: default tenants shared, regulated tenants isolated — with the routing rule written down).

## 6. Scalability levers — in order of cost

Pull levers in this order; measure before and after each one; stop when targets hold.
1. **Fix the query** — indexes, N+1 elimination, payload trimming. Cheapest by far; most "scale problems" die here.
2. **Cache** — per §3, with a named invalidation strategy.
3. **Scale the app tier vertically, then horizontally** — stateless app servers are the easy axis (which is why session/state placement in §4 matters).
4. **Async offload** — move non-critical work (emails, reports, indexing) to queues.
5. **Read replicas / read models** — split read pressure from the write primary.
6. **Partition/shard data** — expensive and hard to reverse; only with measured need and a shard key proven by access patterns.
7. **Split services** — the last lever, pulled for organizational or isolation forces (§1), not as a performance first resort.

## 7. Technology selection method

Never select by familiarity or hype alone. Run a criteria matrix:
1. List **hard constraints** first (existing stack, hosting, licenses, team skills, compliance) — a candidate failing a hard constraint is out regardless of score.
2. Score the survivors 1–5 on weighted criteria. Weights are set per project *before* scoring, and recorded.
3. Score with evidence: a spike/prototype for any criterion scored on a claim ("fast", "easy") that the decision depends on.

**Worked example** — choosing a job queue (weights: fit 3, ops burden 3, team familiarity 2, cost 1, ecosystem 1):

| Candidate | Fit ×3 | Ops ×3 | Familiarity ×2 | Cost ×1 | Ecosystem ×1 | Total |
|---|---|---|---|---|---|---|
| Managed cloud queue | 5→15 | 5→15 | 3→6 | 3→3 | 4→4 | **43** |
| Self-hosted broker (RabbitMQ-class) | 5→15 | 2→6 | 4→8 | 4→4 | 5→5 | 38 |
| DB-backed job table | 3→9 | 5→15 | 5→10 | 5→5 | 2→2 | 41 |

Managed queue wins narrowly; the matrix also shows the honest runner-up (the DB-backed table — nearly as good, zero new infrastructure), which the ADR records as the fallback if managed costs grow. Record the matrix inside the ADR: a decision whose alternatives and scores are visible can be revisited rationally; a bare "we chose X" cannot.

## 8. Architecture fitness checks — how later roles verify it held

Architecture decays silently unless each later gate checks its slice:
- **Developer (Gate 5):** module boundaries respected — no cross-module reach-around imports; contract conformance tests run against the signed API contract; new dependencies appear in the dev notes with a reason.
- **Code Review (Gate 5b):** diffs checked against the ADR list — any decision contradicted by code is either fixed or escalated into a superseding ADR; never let code silently overrule a recorded decision.
- **Integration (Gate 6):** the deployed shape matches the C4 diagram (components, data stores, external calls) — diagram updated in the same task if reality legitimately changed; cache invalidation paths exercised, not just happy-path reads.
- **QA (Gate 7):** the NFRs the architecture promised become tests — the performance target measured, the forbidden state transitions attempted, tenant-isolation cases run, token-storage rules verified in the built client.
- **Release (Gate 8):** rollback actually exercises the architecture's assumptions (data migrations reversible or compensated, feature flags present where the design promised them).

Any fitness check that fails follows the standard rule: stop, Failure Report, fix at the owning role — an architecture quietly not holding is a defect like any other, and the ADR/diagram is updated in the same change whenever the fix alters the design.

## 9. API style selection

| Style | Use when | Avoid when | Cost / note |
|---|---|---|---|
| **REST (resource-oriented)** | Default for CRUD-shaped domains; cacheability and tooling maturity matter | Clients consistently need many resources per screen (over-fetching churn) | Verbose for graph-shaped queries; versioning discipline required (see playbook) |
| **GraphQL** | Multiple client types with divergent, evolving data needs; a schema team exists to govern it | Simple CRUD; strict HTTP caching is a core lever; team cannot operate query-cost controls | Powerful but moves complexity server-side: query depth/cost limits, persisted queries, and authorization per field are mandatory design work |
| **RPC-style (action endpoints / tRPC-class)** | Internal APIs between your own services/apps; actions don't map to resources ("cancel", "re-price") | Public APIs consumed by third parties who expect resource conventions | Honest about actions; weaker standardization and external tooling |
| **Events only (no API)** | The interaction is genuinely one-way notification | Any caller needs confirmation, a result, or an error | Pair with a status/read endpoint — pure fire-and-forget hides failures from users |

Mixed styles are normal (REST for resources, RPC for actions, events for notifications) — the contract must say which style governs which surface, per endpoint, not leave it to each developer's taste.

## 10. Consistency and failure patterns for distributed data

- **Transactional outbox** — when a state change and an event publication must succeed or fail together: write the event to an outbox table in the same DB transaction, publish from there. This is the default answer to "the order saved but the event never fired". Cost: a publisher process and deduplication downstream.
- **Saga (compensating actions)** — multi-step processes spanning services/data stores: each step has a compensating action ("release reservation" compensates "reserve stock"). Prefer choreography for simple flows, orchestration when the flow needs visibility/control. Never reach for distributed two-phase commit across services — design compensation instead.
- **Idempotency everywhere money or inventory moves** — client-supplied idempotency keys on writes, unique constraints at the DB as the backstop, and consumers that tolerate duplicate delivery. (Contract-level rules are in the playbook; this is the architectural consequence.)
- **Retry discipline** — retries only for idempotent operations, exponential backoff with jitter, a stated max, and a circuit breaker when a dependency is down so retries don't become a self-inflicted outage. Every retry policy in the design names its numbers; "we retry on failure" is not a policy.
- **Timeouts are architecture, not tuning** — every cross-boundary call gets a timeout budget derived from the user-facing budget (e.g. 2 s total → API 800 ms → DB 300 ms). A call without a timeout is an unbounded wait that will eventually hold threads/connections hostage.

## 11. Observability as an architectural requirement

Designs must state, not imply, how the running system will be understood:
- **Structured logs** with a correlation/request ID propagated across every boundary in §9–§10 — without it, distributed debugging is guesswork.
- **Metrics that map to the NFRs** — the performance and error-rate targets from the spec each name the metric that proves them in production; if no metric exists, the NFR is unverifiable after release.
- **Health/readiness endpoints** per deployable, distinguishing "process is up" from "dependencies are reachable".
- **Audit vs. debug separation** — audit records (§3) are business evidence with retention rules; debug logs are operational and short-lived. Never let one substitute for the other.
- **Alerting ownership** — each critical metric names who gets paged and the runbook's first step; an alert with no owner is noise the design created.

## 12. Pattern selection — the 60-second path

When a structural decision is needed fast, walk these questions in order and stop at the first decisive answer:
1. Is there a **demonstrated** force for distribution (measured scaling need, measured team contention, compliance isolation)? No → modular monolith (or layered, if tiny). Yes → continue.
2. Is the force about **one hot module** only? Yes → extract that module as a service; keep the monolith for the rest. No → continue.
3. Is the workload **event-shaped and bursty** with tolerant latency? Yes → serverless functions or event-driven components for those flows. No → conventional services.
4. Do **multiple dissimilar clients** drive the API shape? Yes → add a BFF per client class. No → one API.
5. Do **reads diverge hard** from writes? Yes → CQRS-lite read model. No → single model.
Record the walk (question, answer, evidence) in the ADR — the path is the rationale, and it tells a future architect exactly which changed fact should reopen the decision.

## 13. Architecture failure modes — the pre-mortem table

Before finalizing any design, scan it against the failure modes that most often invalidate architectures after launch. For each row: if the design has no answer, the design is not finished.

| Failure mode | How it shows up | Design-time counter |
|---|---|---|
| Distributed monolith | Services that must deploy together; a change ripples across repos | Module/service boundaries drawn at domain seams (§12 Q1–Q2); contract tests per boundary |
| Shared-database coupling | Two services reading/writing the same tables directly | One writer per table; cross-service reads go through APIs/events or a named read model |
| Chatty boundaries | A screen needs 40 calls; latency multiplies | Aggregate at the BFF/API layer; batch endpoints; measure calls per user action in the design |
| The god service / god table | One component owns everything; every change queues behind it | Split by domain capability; the C4 diagram makes the imbalance visible — look at it |
| Premature distribution | Ops burden of §1 paid before any force exists | The §12 walk, answered with evidence, recorded in the ADR |
| Consistency surprises | Users see stale or contradictory data; "it saved but shows old value" | Per-flow consistency stated explicitly (strong vs. eventual + where the user notices), cache staleness budgets (§3) |
| Vendor gravity | A provider's limits/pricing silently become the architecture's limits | Hard-constraint list in the selection matrix (§7) names exit cost for each managed dependency |
| Unowned operations | Nobody can answer "is it healthy, and who acts when it isn't" | §11 observability + alerting ownership completed before the gate passes |
