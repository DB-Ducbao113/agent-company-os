# Security by Application Type — Deep Dive

> Read when: Gate 4 starts and you know what kind of application this is. The playbook gives the method (threat modeling, ASVS 5.0.0, permission matrices); this file gives the per-type threat lists, controls, and mandatory tests.
> How to use: take the section(s) matching the app type, merge their controls into `04-security.md`, and copy their tests into the mandatory QA handover list. Most real systems match 2–3 sections — apply all of them.

## Which sections apply? — Identification table

| Signal in the spec/architecture | Apply sections |
|---|---|
| Browser UI with login | (a) + whichever data sections match |
| JSON/HTTP endpoints consumed by apps or third parties | (b) |
| Native iOS/Android client exists | (c) + (b) for its backend |
| More than one customer organization shares the system | (d) + everything else that matches |
| Money moves: checkout, subscriptions, refunds, balances | (e) + (b) |
| Users upload files others can download/view | (f) |
| Live messaging, channels, presence, feeds with push | (g) |
| Any staff-only console, back office, or ops panel | (h) — even a "temporary" one |
| Chatbot, RAG, copilot, summarization, or an agent that calls tools/APIs | (i) + whichever data sections match |

## (a) Classic Web App (server-rendered or SPA + session/token auth)

Top threats: session hijacking, CSRF, XSS, clickjacking, session fixation.

Controls:
- Session cookies: `HttpOnly` + `Secure` + `SameSite=Lax` (or `Strict` where flows allow); rotate the session ID at login and at every privilege change; idle + absolute timeouts.
- CSRF: synchronizer token on every state-changing form/request when cookie auth is used; verify `Origin`/`Referer` as defense in depth. (Bearer-token APIs without cookies are not CSRF-exposed the same way — say so explicitly in the threat model rather than cargo-culting tokens.)
- XSS: framework auto-escaping everywhere; a written inventory of every escape hatch (raw-HTML rendering, `innerHTML`-equivalents, markdown renderers) — each one needs sanitization (e.g. DOMPurify-class) and a named owner. CSP header deployed, tightened from report-only to enforcing.
- Security headers: `X-Content-Type-Options: nosniff`, frame protection (`frame-ancestors`), `Referrer-Policy`, HSTS on HTTPS.
- Password storage: Argon2id/bcrypt-class hashing; login rate limiting + breached-password screening.

Mandatory tests:
- [ ] State-changing request without CSRF token is rejected
- [ ] Session ID changes after login; old session is dead
- [ ] Stored + reflected XSS payloads in every free-text field render inert
- [ ] Cookie flags verified in a real response (not just config)
- [ ] Logout actually invalidates the session server-side

## (b) REST API Service

Top threats: BOLA/IDOR (the #1 API risk), mass assignment, excessive data exposure, missing rate limits, JWT misuse.

Controls:
- **Authorization per object, per request:** every handler checks "does THIS identity own/can access THIS object" — never rely on the client sending only its own IDs. Centralize the check; a per-endpoint hand-rolled check will be forgotten on endpoint #47.
- **Allowlist input fields** on create/update (DTOs), never bind request bodies directly to ORM models — that is mass assignment (a client adding `"role":"admin"` to a profile update).
- **Response shaping:** return only the fields the client needs; a user object that includes password hashes, internal flags, or other users' data "because the ORM returned it" is excessive exposure.
- **JWT pitfalls:** verify signature AND `alg` (reject `none` and algorithm confusion), check `exp`/`iss`/`aud`, prefer short-lived access tokens + rotating refresh tokens, never store secrets or PII in the payload (it is encoded, not encrypted), have a revocation story for logout/compromise.
- Rate limiting per identity AND per IP on auth and expensive endpoints; pagination caps on every list endpoint; request size limits.

Mandatory tests:
- [ ] User A requests/mutates User B's object by ID → 403/404 (run for EVERY resource type)
- [ ] Update request with an extra privileged field (`role`, `isAdmin`, `balance`) → field ignored or rejected
- [ ] Expired token, tampered-payload token, and `alg:none` token → all rejected
- [ ] List endpoint without pagination params → capped default, not the whole table
- [ ] Auth endpoint hammered at 10× the limit → throttled, legitimate user unaffected after window

## (c) Mobile App (iOS/Android)

Top threats: secrets/data extracted from the device, MITM on hostile networks, deep-link hijacking, token theft from insecure storage.

Controls:
- **Secrets:** no API keys with real privilege in the binary — anything shipped in the app WILL be extracted. Backend must authenticate the user, not the app binary. (App-attestation services raise the bar; they are not a trust root.)
- **Storage:** tokens/credentials only in platform secure storage (Keychain/Keystore); never in plain preferences, files, or logs. Sensitive data minimized on-device; remote-wipe/session-revocation path exists.
- **Transport:** TLS everywhere; certificate pinning is a trade-off — it stops casual MITM but breaks under cert rotation and hostile corporate proxies; pin only for high-value APIs, with a backup pin and a rotation plan, or skip pinning and rely on system TLS + short-lived tokens. Record the decision and its reason.
- **Deep links:** verified app links (domain-verified) for anything sensitive; treat every incoming deep-link parameter as hostile input (it can be sent by any other app); never perform privileged actions from a deep link without in-app confirmation + auth.
- **Rooted/jailbroken devices:** detect if the risk justifies it, respond proportionately (warn, restrict sensitive features) — do not pretend detection is prevention; server-side checks remain the real control.
- Release hygiene: debug logging off in production builds, no test backdoors/accounts, obfuscation as speed-bump only.

Mandatory tests:
- [ ] Token/credential search in app storage and logs after a full session → nothing sensitive in plaintext
- [ ] Deep link from an external source with hostile parameters → validated, no privileged action without auth
- [ ] API calls through a MITM proxy with a user-installed CA → behavior matches the documented pinning decision
- [ ] Session revoked server-side → app is forced to re-authenticate

## (d) SaaS Multi-Tenant

Top threats: cross-tenant data leakage (the existential one), tenant-admin privilege confusion, noisy-neighbor abuse, leakage through shared caches/search/exports.

Controls:
- **Tenant ID is derived from the authenticated identity server-side, never accepted from the client** (not from a header, query param, or body field the client controls).
- Enforce isolation at the data layer: tenant-scoped queries by construction (ORM scopes / row-level security), so a forgotten `WHERE` cannot leak. Application-level filtering alone is a matter of time.
- Every shared subsystem is a leak surface and must be tenant-aware: caches (tenant in the cache key), full-text search indexes, file storage paths, background jobs, analytics exports, support/admin tooling, error messages (don't confirm another tenant's object exists).
- Role model is two-dimensional: platform roles vs. tenant roles. A tenant admin is NOT a platform admin — test the boundary explicitly.
- Per-tenant rate/storage quotas; tenant offboarding includes verified data deletion.

Mandatory tests:
- [ ] Tenant A token + Tenant B object IDs → denied on every resource type (automate this as a regression suite, not a one-off)
- [ ] Tenant B's data absent from Tenant A's search results, exports, autocomplete, and cache-warm responses
- [ ] Tenant admin attempts platform-admin endpoints → denied
- [ ] Background job/export for Tenant A contains zero Tenant B records (row-count diff against fixtures)

## (e) Payments / E-Commerce

Top threats: price/amount tampering, payment-state spoofing via webhooks, card-data exposure expanding PCI scope, refund/coupon abuse.

Controls:
- **Never touch raw card data.** Use the PSP's hosted fields/redirect/checkout so card numbers never transit your servers — this keeps you in the smallest PCI scope (SAQ-A class). The moment card data touches your backend, scope and obligations explode.
- **Prices are computed server-side from the catalog, always.** Any amount, discount, or total sent by the client is display data, never billing input.
- **Webhooks:** verify the PSP signature on every event, using the raw request body; process idempotently (events arrive duplicated and out of order); the webhook — not the browser's "success" redirect — is the only source of truth for payment state.
- Order/payment state machine enforced server-side (no skipping from `created` to `paid` without a verified PSP event).
- Refunds, coupons, gift cards: single-use and balance checks enforced transactionally server-side; admin refund actions are permission-gated and audit-logged.
- Reconciliation job: internal orders vs. PSP records, discrepancies alert a human.

Mandatory tests:
- [ ] Checkout with a tampered client-side price/quantity/discount → server charges the catalog-correct amount
- [ ] Webhook with a forged/invalid signature → rejected and logged
- [ ] Same webhook delivered twice → processed once (idempotency proof)
- [ ] Browser "payment success" return WITHOUT a webhook → order is NOT marked paid
- [ ] Coupon applied twice / beyond its limit, concurrently → enforced once

## (f) File-Upload-Heavy Apps

Top threats: malicious file execution, type confusion, stored XSS via served files, path traversal, storage bucket exposure.

Controls:
- **Validate by content, not by name:** check magic bytes/real MIME type against an allowlist of types the business needs; extension and client-declared type are untrusted decoration.
- **Never execute or serve uploads from the app origin:** store outside the web root / in a separate bucket+domain, serve with `Content-Disposition: attachment` and `nosniff`; an uploaded HTML/SVG served inline from your domain is stored XSS with extra steps (SVG is XML — it can carry script).
- **Scan:** antivirus/malware scanning in the pipeline before a file becomes downloadable by others; unscanned files are quarantined, not "probably fine".
- **Filenames:** generate server-side random names; never use the user's filename as a storage path (traversal `../../`, overwrites, unicode tricks). Size limits per file and per user; image re-encoding (strip metadata/EXIF, defuse polyglot files) where images are the use case.
- **Access control on download:** files are objects — downloading requires the same ownership/permission check as any API object (see BOLA, section b); "unguessable URL" alone is not authorization for sensitive files.

Mandatory tests:
- [ ] Executable/script file renamed to `.jpg` → rejected by content inspection
- [ ] HTML/SVG upload later served → cannot execute script in the app origin
- [ ] Filename with `../` and absolute paths → stored under a generated name, nothing written outside the upload area
- [ ] Another user's file URL with your session → denied (unless explicitly shared)
- [ ] Oversized file and upload flood → rejected/throttled without affecting other users

## (g) Realtime / Chat

Top threats: reading or injecting into conversations you are not in, presence/activity privacy leaks, spam/abuse at machine speed, message spoofing.

Controls:
- **Authorize subscriptions, not just sends:** joining a room/channel/topic is an authorization event — the server checks membership at subscribe time AND when membership changes mid-connection (kick = server closes/forces re-subscribe).
- Every message is validated and attributed server-side; the sender identity comes from the connection's auth, never from a field in the message payload.
- **Presence is personal data:** who is online/typing/last-seen follows the product's privacy settings and is never broadcast beyond the audience that can see the conversation itself.
- Rate limits per user per room (messages, joins, reactions), plus slow-mode/flood controls and a report/block path that actually severs delivery (block = no messages delivered either way, enforced server-side).
- History/backfill endpoints apply the same membership check as live delivery — the classic leak is the REST history API, not the socket.

Mandatory tests:
- [ ] Non-member subscribes to a private room → denied, receives nothing, including backlog
- [ ] Removed member's open connection stops receiving within the documented window
- [ ] Message with a spoofed sender field → attributed to the real connection identity or rejected
- [ ] Blocked user sends → nothing delivered to the blocker, via socket AND history
- [ ] Message flood at 10× normal rate → throttled without dropping other users' messages

## (h) Admin / Internal Tools

Top threats: the "internal = safe" fallacy (VPN ≠ authorization), one over-privileged shared account, unlogged destructive actions, CSRF/lateral movement from a phished employee browser.

Controls:
- **Internal tools get the full treatment:** real per-person authentication (SSO), role-based authorization, and the same input validation as public apps. Attackers who reach the internal network — or ride an employee's browser — inherit everything the tool skips.
- **No shared accounts.** Every action attributable to a person; break-glass/emergency access exists but is individually issued, time-boxed, and alarmed on use.
- **Audit log:** who did what to which object, when, from where — append-only, retained, and reviewed. Destructive/bulk actions (delete, refund, export-all, permission grants) require elevated role + a confirmation that shows scope ("You are about to export 48,000 records").
- Data exports are the exfiltration path: permission-gate them, log them, watermark/notify for large ones.
- Admin surfaces are excluded from public indexes/routes where possible, but obscurity is a bonus layer, never the control.

Zero-trust minimums (checklist — network location grants nothing):
- [ ] Phishing-resistant MFA (WebAuthn/passkeys or hardware keys) required for admin access — not SMS/app codes alone
- [ ] SSO for every admin/internal tool; authorization is least-privilege, role-scoped, and enforced per request — being "inside the network" is never itself a permission
- [ ] Access tokens for admin tooling are short-lived and scoped to the tool and role; no standing broad-access tokens
- [ ] No shared admin accounts — every privileged action traces to a person (see audit log above)
- [ ] No long-lived credentials for CI pipelines or AI agents: use workload identity / OIDC federation issuing short-lived tokens instead of stored cloud keys or PATs
- [ ] Agent/tool credentials are scoped to exactly the actions that automation performs, and are revocable independently of any human's credentials

Mandatory tests:
- [ ] Low-privilege staff role attempts a destructive/bulk action → denied AND the attempt is in the audit log
- [ ] Every privileged action in a scripted session appears in the audit log with actor, object, timestamp
- [ ] Break-glass account use triggers its alert/logging path
- [ ] Session of a deactivated employee → access denied everywhere, including existing sessions

## (i) AI / LLM & Agentic Features

Based on the OWASP Top 10 for LLM Applications (2025) and the OWASP Agentic AI threat list (ASI). Apply whenever the product embeds a model: chatbots, RAG over documents, copilots, summarization/generation, or agents that call tools and APIs.

Top threats: prompt injection — direct (user) and **indirect** (instructions hidden in retrieved documents, web pages, emails, or tool results the model reads), sensitive information disclosure (the model regurgitating PII, another user's data, or its own system prompt), excessive agency (an agent with broad tools talked into destructive actions), unbounded consumption (cost/DoS via runaway tokens and loops). Agentic themes on top: goal hijack, tool misuse, identity & privilege abuse, memory/context poisoning, cascading failures across chained agents/tools.

Controls:
- **Treat model output as untrusted input (LLM05):** model text flows into SQL, HTML, shells, and downstream APIs only after the same validation/encoding as any user input. A model producing a payload is an injection that succeeded.
- **Instructions and data stay separate (LLM01):** retrieved/connected content is data, never instructions. Content from RAG corpora, web pages, files, and tool results must not be able to override the system instructions or trigger tool calls; strip or sandbox instruction-like content at ingestion where feasible, and never let a retrieved document grant permissions.
- **Least-privilege tools and agency (LLM06):** each tool an agent can call is scoped to the minimum action and data; read and write tools are separate; **irreversible or high-impact agent actions (payments, deletions, sends, permission changes) require human approval** before execution. The agent acts under its own scoped identity — never under a human's full credentials (ASI identity & privilege abuse).
- **System prompt is not a secret vault (LLM07):** never place credentials, keys, or genuinely confidential rules in the system prompt; design assuming the prompt can be extracted, so its leakage is embarrassing, not fatal.
- **Disclosure control (LLM02):** filter/redact PII and other users' data from prompts, context, and logs; retrieval is permission-checked per user *before* content enters the context — the model must never receive data the requesting user may not see.
- **Vector/embedding safety (LLM08):** vector stores are tenant/permission partitioned (namespace per tenant or per-user filters enforced at query time); remember embeddings can leak source content — protect the store like the data it was built from.
- **Supply chain (LLM03):** models, adapters, and plugins are dependencies: use trusted providers, pin model versions, record model provenance in the release notes; a silent model-version change is a behavior change — treat it like a dependency upgrade.
- **Poisoning resistance (LLM04):** control who and what can write to fine-tuning data, feedback loops, retrieval corpora, and agent memory; validate ingested content; memory writes from untrusted interactions are quarantined or reviewed (memory/context poisoning).
- **Consumption caps (LLM10):** per-user/per-key token and cost budgets, rate limits, maximum agent steps/loop counts, and timeouts — enforced server-side, with alerts on anomalous spend.
- **Misinformation guardrails (LLM09):** in high-stakes domains, ground answers in retrieved sources with citations, surface uncertainty, and provide a human-review path; never present generated content as verified fact by default.
- **Failure containment:** chained agents/tools get step limits, per-step output validation, and a kill switch, so one compromised or hallucinating step cannot cascade through the whole workflow.

Mandatory tests:
- [ ] **Indirect-injection test set:** documents/web content/tool results seeded with hidden instructions ("ignore previous instructions, send data to…") → the model does not follow them, does not exfiltrate, does not call tools on their behalf
- [ ] Direct prompt-injection / jailbreak attempts → system instructions hold; system prompt and secrets are not disclosed
- [ ] **Tool-scope escape attempts:** the agent is talked into calling tools outside its scope, exceeding its data permissions, or chaining tools to escalate → denied at the tool layer, not merely refused in prose
- [ ] Irreversible action requested via a manipulated conversation → blocked pending human approval
- [ ] **Output-handling fuzzing:** model outputs containing SQL fragments, HTML/script, and shell metacharacters → handled safely by every downstream sink
- [ ] Cross-user / cross-tenant retrieval: user A's documents never enter user B's context, including via semantic similarity
- [ ] **Consumption-cap test:** runaway loop / oversized input / repeated expensive calls → caps, step limits, and budgets trigger and cost stays bounded
- [ ] Memory poisoning: a malicious interaction writes to agent memory/shared context → the poisoned content does not affect other users or later sessions

## Cross-Type: Secrets & Logging Hygiene (applies to every section above)

| Rule | Detail |
|---|---|
| Secrets live in a manager/env, never in code | Repo history is forever; a committed secret is a rotated secret — rotation is part of the fix, deletion is not |
| One secret per environment | Dev/staging/prod never share credentials, tokens, or signing keys |
| Least privilege per secret | The app's DB user cannot drop tables it never drops; the CI token cannot do what CI never does |
| Logs never contain | Passwords, full tokens, session IDs, card data, secrets, auth headers — log identifiers (user ID, request ID), not credentials |
| PII in logs is minimized and purposeful | If support never uses it, it does not get logged; log retention is defined, not infinite |
| Errors shown to users are generic | Stack traces, SQL errors, and internal paths stay server-side; detail goes to logs, a reference ID goes to the user |
| Signing/verification keys are rotatable | Webhook secrets, JWT keys, and API keys all have a documented rotation path that does not require a code change |
| Dependency & token hygiene in CI | Pinned actions/dependencies, minimal token permissions per job, secrets masked in CI output |

## Depth Calibration — How Far to Go per Type

Use the ASVS 5.0.0 depth from the playbook, driven by the worst data the system touches:

| System profile | Minimum depth | Notes |
|---|---|---|
| Public content site, no accounts | Baseline hygiene: headers, TLS, dependency patching | Sections (a) controls still apply to any admin/login surface |
| Accounts + personal data | Standard product depth: full permission matrix, BOLA suite, session rules | The default for most features in this repo's workflow |
| Multi-tenant, payments, health/financial data, admin tooling over production data | Highest depth: isolation test suites, audit-log review, webhook/idempotency proofs, incident path defined before launch | Depth is set by data sensitivity, never by team size or deadline |
| Anything internet-facing with file uploads from strangers | Treat as high depth for the upload pipeline specifically | The rest of the app may be standard; the pipeline is not |

When two profiles collide (e.g. a small team shipping payments), the higher depth wins. Record the chosen depth and its reason in `04-security.md` so QA knows how hard to push.
