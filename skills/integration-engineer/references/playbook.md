# Playbook — Integration Engineer (deep reference)

This document adds detail to the Integration Engineer's `SKILL.md`:
the method behind each technique, table formats, and how to handle specific situations.

## 1. The Contract Verification Matrix — Method

### 1.1. How to build the matrix
Each endpoint occupies one block. Each row is an independent check point with its
own result. Do not merge "check the response" into one generic row — merging loses
the trail when a deviation appears.

| Endpoint | Check point | Expected (per contract) | Observed in reality | Result | Evidence |
|---|---|---|---|---|---|
| POST /appointments | Status on valid create | 201 | 201 | PASS | resp #12 |
| POST /appointments | Field `starts_at` | UTC instant, ISO-8601 with `Z` | local string, no timezone | FAIL | resp #13 |
| POST /appointments | Double-booked slot | 409, `error_code=SLOT_TAKEN` | 400, generic message | FAIL | resp #15 |
| POST /appointments | Missing required field `service_id` | 422, names the field | 422, names the field | PASS | resp #16 |
| GET /appointments | Default pagination | 20 items, includes `total` | 20 items, includes `total` | PASS | resp #21 |

### 1.2. Check order within one endpoint
1. The success path (happy path) first — to confirm the integration point is alive.
2. Every field of the response — name, type, nullable, format.
3. Every error case in the contract — actually trigger it; never infer it from code.
4. Auth and authorization.
5. Boundary behavior: pagination, sorting, filtering, empty data, unusually large data.

### 1.3. The "classic" deviations to always scan for
- Subtly different field names: `userId` vs `user_id`, `createdAt` vs `created_at`.
- Data types: numbers returned as strings, booleans returned as `0/1`, null returned
  as an empty string.
- Date/time: local vs UTC, seconds present or not, a format other than ISO-8601.
- Money/measurements: different units on the two sides (currency units vs thousands,
  seconds vs milliseconds).
- Enums: one side adds a new value the other does not know → there must be a safe
  default behavior.
- Errors: correct status but wrong/missing `error_code`, or the reverse.
- Pagination: convention mismatch (pages starting at 0 vs 1), missing total count.

## 2. Mock Inventory — Format and How to Hunt Mocks

### 2.1. Table format
| # | Location | What is being faked | How it was detected | Owner | Deadline to replace with the real thing | Risk if it reaches production |
|---|---|---|---|---|---|---|
| M1 | List screen (client) | Hardcoded sample data in code | Changed data on the server; the client did not change | Dev FE | Before Gate 7 | Users see fake data |
| M2 | Notification endpoint | Returns success but does not actually send | Checked the test inbox; nothing arrived | Dev BE | Before Gate 8 | Users never receive notifications |

### 2.2. Mock-hunting techniques (do not just ask)
- **Change the source:** modify data in the source system and observe the display side.
- **Cut the source:** disable/block one endpoint and watch whether the consuming side
  reports a real error or keeps "running smoothly" (running smoothly while the source
  is dead = it is using fake data or swallowing errors).
- **Trace the network:** inspect the real requests generated during an action — is
  the called endpoint the one in the contract, or a mock/sandbox address?
- **Read the configuration:** feature flags, environment variables pointing at a
  sandbox, sample data sets inside the code.

## 3. Selecting the Backbone E2E Flows

### 3.1. Selection criteria (in priority order)
1. The main value-creating flow the feature exists to serve (successfully creating
   one primary entity).
2. The flow that reads/displays the just-created result somewhere else (proves the
   data travels the full round trip).
3. The login/token-refresh flow, if the feature sits behind auth.
4. The most important business error flow (duplicate, out of permission, quota exceeded).
5. The cancel/delete/undo flow, if any — because the reverse direction is often
   never verified.

### 3.2. Count and depth
- Usually 3–7 flows are enough for one task. More → you are duplicating QA's work;
  fewer → you miss the data lifecycle.
- Each flow runs from the real UI/client to real persisted data, then is verified
  through an independent path (open another screen, call the read API, check the
  notification was sent).

### 3.3. Test data for E2E
- Use data created specifically for the verification session, with identifiable
  markers (a name prefix, a dedicated test account).
- Record the IDs of the data you created so QA/Release can trace it; clean it up,
  or state clearly why it is kept.

## 4. Common Environment Pitfalls

| Group | Pitfall | Symptom | How to check |
|---|---|---|---|
| Environment variables | Client points at the dev API URL while running the staging build | "Ghost" data, appears and disappears | Print/log the actual configuration of the build under test (never print secrets) |
| Environment variables | A secret exists only on the dev machine, missing in staging | Secondary features die silently, scattered 500s | Compare the list of variable names between environments |
| CORS | Server only allows the dev domain | Browser blocks calls while a native app works fine | Test from a browser on the real domain, not only with an API tool |
| Cookies | SameSite/Secure/Domain wrong after a domain change | Logged in, then immediately kicked out | Test on the real domain with a real browser |
| Timezone | Server stores local time, client interprets it as UTC | Every time is off by exactly the timezone offset | Create data at a day boundary; view it in two different timezones |
| Date format | The two sides use different day/month conventions | Wrong data on days ≤ 12 | Test with a date like 05/06 and verify both the write and read directions |
| Region | An external service only serves certain regions / its sandbox differs from production | Tests pass, production gets rejected | Confirm the target environment's region config and account type |
| Rate limits | The real environment has lower limits than the test environment | Single runs pass; bulk runs fail with 429 | Check the provider's documented limits; run the main flow repeatedly |
| Cache/CDN | The old build is cached at the distribution layer | "Fixed, but the old bug is still visible" | Verify with a version marker (build id) displayed on the client |
| System clock | The test machine's clock is off, making tokens look "falsely expired" | Strange auth errors that do not reproduce on other machines | Compare the system clock against a standard time source when token errors look odd |

## 5. Handling Deviations — The Full Procedure

1. **Record immediately when found**, before any verbal discussion ends: expected,
   actual, evidence.
2. **Assign the right owner:**
   - Implementation differs from the contract → the owner is that implementation side.
   - Contract is missing/contradictory/infeasible by itself → the owner is the Architect.
   - Contract is correct but a security requirement is violated → the owner is the
     violating side, with a copy to Security.
3. **Blocking or not:** a deviation that corrupts data, breaks a backbone flow, or
   exposes data = blocking (the gate does not PASS). A small presentation deviation
   with a safe workaround and no data corruption = non-blocking, but it must still
   have a fix deadline.
4. **Re-verify after the fix:** check the exact deviating point + the neighboring
   check points in the same endpoint + the related backbone flow. Do not re-verify
   everything from scratch unless the change touched a shared foundation.
5. **Close a deviation:** only close it when re-verification evidence passes; record
   the closing date in the log. A deviation re-opened a second time → escalate to
   the gate approver with its history.

## 6. Verifying Third-Party Integrations — Specific Notes

- Clearly separate three layers of faults: your own fault (wrong signature/wrong
  format), account configuration faults (not activated, wrong account type), and
  the provider's faults (an incident on their side). Each layer has a different remedy.
- Webhooks: verify the signature/source authentication, the case where the provider
  retries delivery multiple times (your system must handle duplicates safely), and
  the case where the webhook arrives before your side's data is ready.
- Always keep a set of sample request/response logs (with secrets redacted) for
  each integration type, to compare against when an incident occurs.
