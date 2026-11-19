# Security Playbook — Deep Reference

> Read while working Gate 4 and the re-check after Integration. SKILL.md gives the workflow; this file gives the lookup tables.

## 1. OWASP Top 10 — Review Checklist (common web/API edition)

| # | Risk class | What to check in your project |
|---|---|---|
| A01 | Broken Access Control | Does every endpoint check permissions on the server? Is there IDOR (changing an ID to see someone else's data)? Vertical/horizontal privilege escalation? Are directory listings/debug endpoints exposed? |
| A02 | Cryptographic Failures | Is sensitive data encrypted in transit (TLS) and at rest? Are passwords hashed with a dedicated algorithm (bcrypt/argon2…)? Is there any home-grown or weak cryptography? |
| A03 | Injection | Are all DB queries parameterized? Is any string concatenated into SQL/commands/templates? Is reflected input escaped against XSS? |
| A04 | Insecure Design | Does the threat model exist before the code? Are business limits (attempt counts, quotas, link expiry) designed in? |
| A05 | Security Misconfiguration | Is debug mode off in production? Is CORS restricted to the correct origins? Are security headers + cookie flags (HttpOnly, Secure, SameSite) correct? Do error messages leak stack traces? |
| A06 | Vulnerable & Outdated Components | Are there dependencies with unapplied patches? Any unmaintained library in the path of sensitive data? |
| A07 | Identification & Authentication Failures | Password policy, brute-force protection (rate limit/temporary lockout), do sessions/tokens expire and can they be revoked? Does the password-reset flow resist account takeover? |
| A08 | Software & Data Integrity Failures | Is data received from third parties/webhooks verified for signature/integrity? Does CI/CD run untrusted code? Is deserialization of foreign data controlled? |
| A09 | Logging & Monitoring Failures | Are security events (failed logins, permission changes, denied access) logged (redacted) and actually reviewed by someone? |
| A10 | Server-Side Request Forgery (SSRF) | Does the server fetch URLs supplied by users? If so: host allowlist, block internal addresses, limit redirects. |

**OWASP API Security — 3 failures to sweep separately for every API:**
1. **BOLA/IDOR** — an object identified by a client-supplied ID without an ownership check. The #1 API flaw.
2. **Broken Authentication / Excessive Data Exposure** — weak/non-expiring tokens; responses returning surplus fields.
3. **Mass Assignment** — accepting a whole object from the client and writing it straight to the DB, allowing forbidden fields (role, balance, status) to be modified.

## 2. ASVS Levels — Which Level to Choose

| Level | When | Characteristics |
|---|---|---|
| L1 | Every application with real users — the floor | Basic controls: HTTPS, input validation, per-request permission checks, correct password hashing, no internal error leakage |
| L2 | User accounts, personal data, or money | Adds: strict session/token policy, brute-force protection, security-event logging, disciplined secret management, data-level access control (anti-IDOR) with tests |
| L3 | Very high-risk systems (core finance, healthcare, infrastructure) | Adds: deep verification, architecture review, strict cryptographic and operational requirements — usually needs outside specialists |

Record the chosen level in `04-security.md` with the reason. Choosing a lower level than the situation
requires must be signed by the approver.

## 3. STRIDE per Component — Sample Table

| Component | Group | Scenario | Mandatory countermeasure |
|---|---|---|---|
| Public API | Spoofing | Using someone else's stolen token to call the API | Short-lived + revocable tokens; bind to device/session when risk is high |
| Public API | Tampering | Modifying price/quantity in the request before sending | The server recomputes price from source data; never trust client-sent numbers |
| Business service | Repudiation | A user denies having performed an important action | An audit log with actor, time, and action — tamper-resistant at the application level |
| Database | Information Disclosure | An internal response/API returns surplus personal data | Field allowlist on responses; masking in logs and admin screens |
| Whole system | Denial of Service | Flooding an expensive/heavy endpoint with requests | Rate limits, size/quantity limits, timeouts, queues |
| Authorization | Elevation of Privilege | A regular user calls an admin endpoint | Role checks on the server for every endpoint; deny by default |

How to work: copy this table for each real component of the feature — never submit the sample table as-is.
A component claimed to have "no threats" must record the reason for believing so.

## 4. Method for Building the Permission Matrix

1. List the actors from the BA (including "unauthenticated guest" and "third-party system").
2. List actions by data, not by screen: read / create / update / delete / export / approve —
   one screen can contain several actions with different permissions.
3. Fill each cell: Allow / Deny / Conditional (write the condition as a verifiable sentence,
   e.g. "only when the record belongs to the actor themselves").
4. Mark the high-risk cells: every "Allow" over someone else's data, every action involving money/state.
5. For each high-risk cell: record the server-side enforcement point + the corresponding QA test.
6. Cross-check against the API contract: any endpoint in the contract that does not appear in the matrix
   is a gap — add it immediately.

## 5. Secret & Data Rules (the hard version)

- Secrets live only in: backend environment variables, the platform's secret manager/vault, or an approved credential store.
- Secrets never appear in: source code, config files committed to the repo, client bundles/JS,
  screenshots, logs, or chat/ticket content.
- Each environment (dev/staging/production) uses its own secrets; production secrets are never used for testing.
- A leaked secret = an incident: rotate it immediately, then investigate the exposure scope. Deleting the
  line containing the secret from a file does not make the secret "never leaked".
- Personal data in test environments must be fake or anonymized — never copy raw production data down to dev.
- Backups are data too: backups containing sensitive data must be encrypted and access-restricted just like the originals.

## 6. Security Test List Handed to QA (mandatory; select by scope)

- [ ] **Wrong permission:** an actor without the permission invokes the action → denied (403), including when calling the API directly
- [ ] **IDOR/BOLA:** change the ID of another user's record in a read/update/delete request → denied
- [ ] **Vertical escalation:** a regular account calls an admin endpoint → denied
- [ ] **Excessive data:** the response contains no sensitive fields beyond the agreed allowlist
- [ ] **Expired / revoked / tampered token:** all denied; after logout, the old token cannot be reused
- [ ] **Malicious input:** basic injection/XSS payloads into every main input field → not executed, data not corrupted
- [ ] **Rate limits:** repeated failed logins / repeated calls to an expensive endpoint → blocked or slowed as designed
- [ ] **Sensitive flows:** password reset / email change / permission change — links expire as designed, cannot be reused, and the account owner is notified
- [ ] **Upload (if any):** a disguised wrong-type file, an oversized file, a file containing malicious code → rejected or quarantined
- [ ] **Webhook (if any):** a forged webhook call without a valid signature → rejected

Every test in this list must appear in the QA report with a pass/fail result and evidence.

## 7. Finding Severity Levels

| Level | Definition | Example |
|---|---|---|
| Critical | Exploitable right now, broad impact or sensitive data/money | IDOR that reads every user's data; a leaked production secret |
| High | Exploitable under common conditions, large impact | A missing permission check on one important endpoint; passwords stored unhashed |
| Medium | Limited impact, or requires harder conditions | Logs containing unmasked personal data; a cookie missing a flag |
| Low | Small risk, mostly defense-in-depth hardening | A missing security header; a slightly too-detailed error message |

Severity is judged by *impact × exploitability in the project's real context* — never copy generic
scoring scales wholesale.

## 8. Quick Check of Session & Cookie Configuration (when sign-in exists)

- Session cookies: `HttpOnly` (blocks script access), `Secure` (HTTPS only), appropriate `SameSite` (Lax is a good default).
- Sessions/tokens: a clear expiry; logout and password change must revoke old sessions.
- Tokens stored in a place appropriate to the app model; client-stored tokens need corresponding XSS mitigations.
- CSRF protection for state-changing operations using session cookies: a CSRF token, or SameSite + Origin checks.
- Failed login attempts are rate-limited; login error messages do not reveal whether the account exists.

## 9. When Integrating Third Parties / Webhooks

- Webhooks: verify the signature with a dedicated secret; add replay protection (timestamp/nonce) if the platform supports it.
- A third party's API key lives only on the backend; if a key has ever appeared on the client, treat it as public and have it re-issued.
- Data sent out: send only the fields the other side truly needs; record it in the data flow so later reviews can see it.
- A third party's errors must not leak internal information in messages returned to users.
