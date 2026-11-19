# Third-Party Integrations — Field Guide

> Read this when the integration involves an external provider (identity, payments, messaging, maps, file feeds, partner APIs) rather than your own FE↔BE. Your own contract discipline still applies — the provider's API is a contract you did not write and cannot change, so verification shifts from "does it match the contract" to "do we survive the contract as it actually behaves".

## 1. Evaluating a provider BEFORE integrating (score it, don't vibes it)

| Criterion | What to check | Red flag |
|---|---|---|
| Docs quality | A working quickstart you can run in <30 min; full endpoint reference; a changelog with dates | Marketing-page "docs"; examples that don't run; no changelog |
| Sandbox parity | Sandbox mirrors production behavior (same error shapes, same limits semantics); test data generators provided | Sandbox that always succeeds; no way to trigger errors/declines |
| Versioning policy | Published policy: versioned URLs or headers, deprecation notice period (≥6–12 months is healthy), sunset headers | "We may change the API at any time"; breaking changes announced in a tweet |
| Status & incidents | Public status page with history; postmortems; measured uptime over 12 months | No status page; history wiped; every incident "resolved" in 5 minutes |
| Support | Named support channel with an SLA for paid tiers; a human reachable during an outage | Community-forum-only support for a money-critical dependency |
| Data terms | Where data is processed/stored (region), retention, deletion on contract end, sub-processor list | Vague DPA; data residency unanswerable |
| Exit cost | Data export in an open format; what breaks if they shut down or triple prices | Your core records exist only inside their system |

**Decision rule:** a provider failing sandbox parity or versioning policy is disqualified for money/auth-critical paths no matter how good the demo is — those two failures are the ones that hurt you at 2 a.m. six months later. Record the evaluation in the integration artifact; "we picked the famous one" is not an evaluation.

## 2. OAuth / OIDC integration checklist

- [ ] Use Authorization Code flow with **PKCE** for every client type, including confidential server clients (defense in depth, and some providers now require it).
- [ ] Generate `state` per request (cryptographically random, stored server-side, compared on callback); add `nonce` for OIDC and validate it in the ID token.
- [ ] **Redirect URI discipline:** register exact URIs only — no wildcards, no prefix matching, no open redirectors on your callback. One URI per environment (dev/staging/prod are separate client registrations).
- [ ] Validate the ID token fully: signature (provider JWKS, with key rotation handled), `iss`, `aud`, `exp`. Never trust claims from an unvalidated token or from the userinfo endpoint alone.
- [ ] **Token storage:** access/refresh tokens encrypted at rest, server-side only; never in localStorage, never in logs, never in URLs. Refresh tokens rotate where the provider supports it; a reused refresh token = treat as compromise and revoke the family.
- [ ] Request the minimum scopes; record which scope powers which feature so a scope removal is debuggable. Handle the user granting *fewer* scopes than requested.
- [ ] Handle the unhappy paths explicitly: user denies consent, account linking collision (same email, different provider), provider account deleted, token revoked while a background job is mid-flight.
- [ ] Clock skew: allow a small leeway (≤60s) on token time claims; sync server time via NTP — half of all "random" OIDC failures are clock drift.
- [ ] Logout is a feature: local session end, provider token revocation where supported, and a documented answer to "does logging out here log them out there?" (usually: no — say so in the UI).

## 3. Webhooks deep dive

Webhooks are an untrusted, unordered, at-least-once input stream. Build for exactly that.

- **Signature verification, always:** verify the provider's HMAC/signature over the *raw* request body (parse JSON only after verification — re-serialized JSON breaks signatures). Reject on mismatch with a generic 400; compare in constant time. Rotate signing secrets on the provider's schedule and support two active secrets during rotation.
- **Idempotent handlers:** providers retry, and retries duplicate. Store the provider's event ID in a unique column; a duplicate insert = acknowledge with 200 and do nothing. Business effects (charging, emailing, provisioning) must key off the event record, never run twice for one event ID.
- **Acknowledge fast, process async:** return 2xx within ~2–5s after persisting the raw event; do the work in a background job. A slow handler triggers provider retries, which trigger duplicates, which trigger load — the retry storm starts with your slow endpoint.
- **Ordering is not guaranteed:** a `updated` event can arrive before `created`. Handlers must tolerate out-of-order delivery: upsert by natural key, compare provider timestamps/versions, and never let an older event overwrite newer state (keep a `last_event_at`/version guard).
- **Replay window:** most providers let you (or an attacker with a leaked secret) replay old events. Reject events whose signed timestamp is outside a tolerance window (commonly 5 minutes) — this is part of the signature scheme on major providers; don't disable it.
- **Retry storms (inbound):** when your endpoint was down, the provider's backlog arrives as a burst. Rate-limit your own processing queue, not the receiver (rejecting with 5xx invites more retries); shed load by event type priority — money events first, analytics last.
- **Dead-letter handling:** events that fail processing N times go to a dead-letter store with the raw payload, the error, and a replay button/procedure. A dead-letter queue nobody inspects is a silent data-loss machine: alert when depth > 0 for critical event types, and review weekly.
- **Reconciliation backstop:** webhooks get lost even when everyone behaves. For anything money- or entitlement-shaped, run a periodic job that pulls the provider's current state and diffs it against yours. The webhook is the fast path; reconciliation is the truth path.

**Micro-example:** payment provider sends `payment.succeeded` twice (retry) and once more after a manual resend from their dashboard. Correct behavior: three deliveries, one event ID row, one fulfillment. If your fulfillment count is 3, your idempotency is decorative.

## 4. Payment gateway specifics

- **Never touch raw card data.** Use the provider's hosted fields/elements or hosted checkout so card numbers go from the customer's browser straight to the provider. The moment raw PAN data crosses your server, you inherit the heavy end of PCI DSS (SAQ D instead of SAQ A) — an audit program, not a feature.
- **3-D Secure flows:** expect a redirect or challenge step that can be abandoned, fail at the bank, or complete minutes later. The payment is not final at form submit: model states explicitly (`requires_action → processing → succeeded/failed`) and drive the UI and fulfillment off **webhook-confirmed** states, not off the browser's return URL (users close tabs; banks redirect late).
- **Amounts are integers** in the currency's smallest unit, with the currency code attached at every step. A float, or a missing currency, is a defect even if today's tests pass.
- **Reconciliation:** daily job comparing provider settlements/charges against your orders: every charge has an order, every order's amount matches, every refund links to a charge. Discrepancies go to a human queue with an aging report — unreconciled money older than 7 days is an incident, not a backlog item.
- **Refund paths are separate code:** full vs partial, refund to original method only, refund webhooks are also asynchronous (a refund can fail days later if the account closed). Test the refund path as thoroughly as the charge path; the first time you run it must not be for an angry customer.
- **Test cards ≠ sandbox money:** test cards exercise shapes (decline codes, 3DS challenges, insufficient funds). They do not exercise settlement timing, currency conversion, or payout behavior. Before launch, run at least one real micro-transaction end-to-end (charge → settlement → refund) in production with your own card.
- **Disputes/chargebacks:** the provider notifies via webhook; evidence submission has hard deadlines. Wire the webhook to a ticket with the deadline as its due date on day one.

## 5. File import / export integrations (CSV, SFTP drops, partner feeds)

- **Schema drift is the default:** partners add columns, rename headers, change date formats, switch encodings. Validate the header/schema against an expected contract *before* processing a single row; a drifted file is rejected whole and alerted, never "best-effort parsed".
- **Partial failures:** process row-wise with per-row results (accepted / rejected + reason). The import report is a deliverable: counts, rejection reasons grouped, and the rejected rows downloadable for the sender to fix. Never fail a 10,000-row file silently on row 9,999 — and never half-apply it without saying which half.
- **Idempotency & resumability:** key imports by (source, file hash or batch ID); re-delivering the same file is a no-op or an explicit re-run, never a duplicate insert. For large files, checkpoint progress so a crashed import resumes instead of restarting (and double-applying the first half).
- **Encoding & format traps:** pin the expected encoding (UTF-8), delimiter, quoting, decimal separator, and date format in the feed agreement; add a canary row count and total/checksum where the format allows it.
- **Exports are integrations too:** your consumers break when *you* drift. Version the export schema, announce changes, and keep the old version running through the announced window.

## 6. External API failure modes → required client behavior

| Failure mode | Detection | Required client behavior |
|---|---|---|
| Slow responses / timeouts | Per-call timeout budget (connect + total), p95 latency alarms | Set explicit timeouts on **every** call (no infinite waits); total budget per user request; fail with a mapped error, never hang the request thread |
| Rate limiting (429) | 429 status, `Retry-After` header | Honor `Retry-After`; exponential backoff **with jitter**; queue or shed non-critical calls; never tight-loop retry (you become the outage) |
| 5xx / partial outage | Error-rate alarms per endpoint | Bounded retries (e.g. 3) with backoff+jitter for idempotent calls only; circuit breaker opens after a failure threshold so you stop hammering a dying provider |
| Provider fully down | Circuit breaker open, synthetic check failing | Serve the degraded path: cached/stale data clearly labeled, or a honest "temporarily unavailable" state; queue writes for later sync where the domain allows |
| Silent data changes (same schema, different meaning) | Reconciliation diffs, canary records with known expected values | Contract tests in CI against the sandbox + a scheduled production canary; alert on semantic diffs, not just errors |
| Auth expiry mid-operation | 401s clustered by token age | Refresh proactively before expiry; on 401, refresh once and retry once — then fail, never loop |
| Duplicate delivery / replay | Duplicate event IDs | Idempotent handlers (§3); duplicates are normal traffic, not errors |
| Clock/timezone mismatches | Timestamp diffs vs provider | Store UTC instants end-to-end; convert only at display; log both raw and parsed timestamps when debugging |

**Circuit breaker, concretely:** closed (normal) → after e.g. 50% failures over 20 requests, open (fail fast locally for 30–60s, no provider calls) → half-open (one probe request; success closes, failure re-opens). Without it, your retry logic converts their 10-minute outage into your cascading failure.

**Backoff, concretely:** delay = min(cap, base × 2^attempt) + random jitter, e.g. base 200ms, cap 30s. Fixed-interval retries from many clients synchronize into thundering herds; jitter is not optional decoration.

## 7. Sandbox-vs-production divergence checklist

Run before go-live; every "unknown" is a launch blocker for money/auth paths.

- [ ] Error shapes: do sandbox errors match production error codes/formats for the cases you handle?
- [ ] Rate limits: sandbox limits are usually lower or absent — what are the *production* limits, and does your backoff handle them?
- [ ] Webhook signing: different signing secret per environment; production secret stored and rotatable?
- [ ] Data realism: sandbox data is clean; production has legacy states (old subscriptions, edge-case currencies, deleted-but-referenced entities). Which of your flows assume clean data?
- [ ] Feature flags on the provider side: is every feature you use enabled on the *production* account (many providers gate features per account, not per API key)?
- [ ] Money movement: settlement timing, payout schedule, minimum amounts — sandbox settles instantly; production does not.
- [ ] Compliance gates: provider may require business verification (KYC) before production charges/refunds work at all. Discovered on launch day = launch delayed.
- [ ] URLs & allowlists: production webhook endpoints registered, IP allowlists updated, redirect URIs registered for the production client (§2).

## 8. Monitoring an integration in production

- **Synthetic checks:** a scheduled job (every 1–5 min for critical paths) performs a harmless read against the provider (e.g. fetch a known object) and records success/latency. This detects provider outages before your users do and gives you the timeline evidence for support tickets.
- **Metrics per integration, minimum:** call volume, error rate by class (4xx yours / 429 / 5xx theirs / timeouts), p50/p95 latency, webhook lag (event time → processed time), dead-letter depth, reconciliation diff count.
- **Alert thresholds (starting points, tune to your traffic):** error rate >2% over 10 min → page; webhook lag >5 min → page for money events; dead-letter depth >0 for critical types → ticket same day; reconciliation diff ≠ 0 → ticket next business day, page if money-shaped; synthetic check failing 3 consecutive runs → page.
- **A status-page habit:** when your alerts fire, the first diagnostic step is the provider's status page + your synthetic timeline — record both in the incident note. "Provider acknowledged incident 14:02–14:47" closes arguments later.
- **Quarterly review:** re-run §1's evaluation against reality (their incident history vs. your experience, price changes, deprecation announcements). Integrations decay; the review is where you notice before the outage does it for you.

## 9. Outbound calls — retries, idempotency, and timeouts in your client

- **Idempotency keys on unsafe calls:** for any POST that creates or charges, generate a key per *business operation* (not per attempt) and send it on every retry. Without it, a timed-out request you retry becomes a duplicate charge/order — the timeout told you nothing about whether the provider processed it.
- **Retry only what's safe:** GETs and idempotency-keyed POSTs may retry; unkeyed POSTs may not. When an unkeyed call times out, the correct move is to *query* the provider for the operation's outcome, not to fire it again.
- **Timeout budget math:** your user's request cannot outlive its own deadline. If your API allows 10s total and the provider call takes 8s at p99, two retries do not fit — the budget decides the retry count, not optimism. Allocate: provider call ≤60% of the request budget, retries inside the remainder, and fail with a mapped, honest error when the budget is spent.
- **Connection hygiene:** reuse connections (keep-alive/pools), set connect and read timeouts separately, and cap concurrent calls per provider so one slow provider cannot consume every worker you own (bulkhead pattern).

## 10. Testing the integration before production

| Layer | What it proves | Where it runs |
|---|---|---|
| Contract tests against the provider sandbox | Your requests/response handling match the provider's actual shapes, incl. error bodies | CI, on every change to the integration |
| Negative-path drills | Declines, expiries, insufficient funds, revoked tokens, malformed webhooks all behave as designed | Sandbox, scripted — providers give test triggers; use every one |
| Webhook replay test | Replaying yesterday's captured events into staging changes nothing twice (idempotency proof) | Staging, pre-launch and after handler changes |
| Kill-switch drill | Disabling the integration degrades the product gracefully (no 500s, honest UI states) | Staging, pre-launch |
| Deprecation drill | You can name the provider's current API version, its sunset date if any, and the owner who watches the changelog | Process check, quarterly |

- **Record provider behavior you depend on** (quirks log in the integration artifact): undocumented limits, odd error shapes, sandbox-only behaviors. Providers change staff and docs; your quirks log is the memory.
- **Change management:** subscribe to the provider's changelog/status feed *as a team*, not as one person's inbox. An unannounced-to-you breaking change discovered by users is a monitoring failure on your side too.

## 11. Go / no-go checklist for launching a new integration

- [ ] Provider evaluation (§1) recorded; disqualifiers checked for money/auth paths
- [ ] OAuth/OIDC checklist (§2) complete, unhappy paths handled
- [ ] Webhooks: signature verified on raw body, idempotent handlers proven by replay test, dead-letter alert wired
- [ ] Failure-mode table (§6) reviewed; timeouts, backoff+jitter, circuit breaker implemented and load-tested at least once
- [ ] Sandbox-vs-prod divergence checklist (§7) has zero "unknown" on critical paths
- [ ] Reconciliation job running (money/entitlement data) with a human queue for diffs
- [ ] Synthetic check + §8 alerts live in production *before* real traffic arrives
- [ ] Rollback/disable plan: how the feature degrades with the integration off, and who may decide to turn it off
