# Engineering Craft — Deep Dive

> Read when: you are structuring, debugging, refactoring, or reviewing your own implementation choices inside Gate 5.
> Companion: `playbook.md` covers the TDD cycle, slicing, and evidence standards; this file covers the craft underneath them.

## 1. Structuring Code

Two organizing schemes; pick per codebase and be consistent:

| Scheme | Shape | Fits | Failure mode |
|---|---|---|---|
| By layer | `controllers/`, `services/`, `models/` | Small apps, frameworks that enforce it, teams fluent in the stack | A feature change touches 6 folders; related code is scattered |
| By feature | `features/billing/`, `features/booking/` (each with its own UI/API/data) | Growing products, multiple devs/agents, clear ownership | Shared utilities get duplicated per feature if extraction is lazy |

Rules that hold in both:
- **Dependency direction points inward/downward:** UI depends on domain logic; domain logic depends on nothing framework-specific; data access is at the edges. A business rule that imports an HTTP request object is a rule you cannot test or reuse.
- **No circular dependencies.** If A imports B and B needs A, the boundary is drawn wrong — extract the shared piece or invert with an interface/event.
- **A module's public surface is small and named.** Everything not exported is private by default. "Import anything from anywhere" is how codebases become unchangeable.
- **Shared code is earned:** extract on the third genuine use (rule of three), not the first imagined one — premature shared abstractions couple features that should evolve separately.
- New code goes where a reader would look for it, following the existing structure — even if you'd structure it differently greenfield. Local consistency beats imported elegance.

## 2. Error Handling Patterns

- **Typed errors, not strings.** Errors carry a category (validation / not-found / permission / conflict / upstream / internal) plus a stable code. Callers branch on category, never on message text.
- **Fail at the right layer:** domain code signals errors (returns/throws typed errors); the boundary layer (HTTP handler, UI) translates them into responses/messages. A domain function that returns an HTTP status has leaked the boundary inward.
- **Error boundaries in UI:** a failing widget/section shows its own fallback; one broken panel must not white-screen the page. Log the error with context, show the user something honest and recoverable.
- **Never swallow.** An empty catch / ignored error return is a defect even if "it works" — at minimum log with context; usually propagate or convert to a typed error. Silent failure today is an undebuggable incident later.
- **Retry with backoff + jitter, only where safe:** retries are for idempotent operations or operations carrying an idempotency key. Retrying a non-idempotent POST (payment, order create) without a key manufactures duplicates. Cap attempts, cap total time, and log each retry.
- **Timeouts everywhere a network is involved.** A call without a timeout is a hang waiting for its moment; set connect + total timeouts deliberately.
- **User-facing messages** are written for the user (what happened, what they can do), mapped from the error code at the boundary — never raw exception text, never stack traces.

| Situation | Pattern |
|---|---|
| Expected failure (bad input, not found) | Typed error → boundary maps to 4xx + user message |
| Upstream flaky, operation idempotent | Retry ≤3, exponential backoff + jitter, then typed upstream error |
| Upstream flaky, operation NOT idempotent | No blind retry; idempotency key or fail + surface for user retry |
| Bug (invariant broken) | Fail fast, log loudly with context; do not "recover" into a corrupt state |
| Partial failure in a batch | Report per-item results; never report total success |

## 3. Input Validation Layering

| Layer | Responsibility | Examples |
|---|---|---|
| Client (UX validation) | Fast feedback, format hints, preventing obviously-wrong submits | Required-field prompts, format masks, length counters |
| Server (the actual validation) | ALL rules that matter: types, ranges, enums, ownership, business invariants | Reject negative quantities, foreign object IDs, illegal state transitions |
| Database (last line) | Constraints that must hold even if app code has a bug | Unique constraints, foreign keys, check constraints, NOT NULL |

Rules:
- **Client validation is a UX feature, never a security/correctness control.** Anything enforced only on the client is unenforced.
- Server validates every field of every request as if it came from an attacker with curl — because QA and Security will test it exactly that way.
- Validate types strictly (a string "5" is not the number 5 unless you deliberately coerce), reject unknown fields on sensitive inputs, and return field-level errors the client can display.
- Business invariants that two requests can race (last seat, last item, double-spend) belong in transactions/DB constraints, not in check-then-act application code.

Validation defects QA/Security find most often (pre-empt them):

| Defect | Example |
|---|---|
| Validating presence but not range/shape | `quantity = -3` accepted; a 40,000-character "name" stored |
| Validating on create but not on update (or vice versa) | The PATCH endpoint accepts what POST rejects |
| Trusting a client-computed value | Total price, discount, or role taken from the request body |
| Inconsistent rules between client and server | Client allows what the server rejects, discovered by the user as a dead end |
| Error responses that leak internals | Raw DB constraint names or stack text returned to the client |

## 4. The Developer's Own Testing Pyramid

Dev writes tests that protect the implementation; QA owns independent verification against acceptance criteria. Both are required; neither replaces the other.

| Level | Dev writes | QA owns |
|---|---|---|
| Unit (many, fast) | Business rules, calculations, edge/boundary cases of own functions, state transitions | Reviews coverage of AC-critical rules; adds cases Dev didn't think of |
| Integration (some) | Own API endpoints vs. contract, DB queries, service-to-service calls in the slice | Cross-feature flows, contract conformance of the assembled system (with Integration role) |
| E2E (few) | Smoke of the critical path of own slice (it boots, the main flow completes) | Full user journeys traced to AC, negative paths, regression suites |

Rules:
- A bug fix without a reproducing test is unfinished — the test is the proof and the regression guard (see playbook's TDD cycle).
- Tests must be deterministic: no dependence on test order, wall-clock time, or live third-party services (fake/stub them at the boundary).
- Flaky tests are bugs. Quarantine + fix or delete; a suite the team ignores is worse than a smaller suite it trusts.
- Dev's completion evidence includes the test run output (see playbook) — "tests pass" without the run is an unverified claim.

## 5. Safe Refactoring Protocol

Refactoring = changing structure without changing behavior. The protocol keeps that true:

1. **Characterize first:** if the code lacks tests, write characterization tests that pin down CURRENT behavior (including quirks) before touching anything. You cannot prove "behavior unchanged" against a baseline you never recorded.
2. **One axis at a time:** don't rename, restructure, and optimize in the same change. Each step should be independently revertible.
3. **Small steps, green between steps:** run the tests after each micro-change; a red suite mid-refactor means stop and fix that step, not press on.
4. **No behavior changes smuggled in.** If you spot a bug while refactoring, note it and fix it in a separate change with its own reproducing test — mixing the two makes both unreviewable.
5. **Refactor toward the task:** clean the area you are already changing (boy-scout rule); a wholesale rewrite of working code needs an ADR-level justification, not enthusiasm.

## 6. Debugging Method

Discipline, in order. Skipping to step 4 is how hours disappear.

1. **Reproduce** — a bug you cannot reproduce on demand is not yet debuggable. Find the minimal input/state that triggers it; record it exactly.
2. **Minimize** — strip the repro down: smallest data, fewest steps, one variable at a time, until removing anything makes the bug vanish.
3. **Hypothesize** — write down 1–3 candidate causes, ranked, each with a prediction ("if X, then changing Y removes it").
4. **Instrument** — test the top hypothesis with the cheapest probe: a log line, a debugger breakpoint, a bisect, a diff between working and broken cases. Change ONE thing per experiment.
5. **Fix** — fix the root cause, not the symptom; check whether the same cause exists elsewhere (search for the pattern).
6. **Regression test** — turn the minimal repro into an automated test that fails before the fix and passes after. Then run the surrounding suite.

Worked micro-example:
> Report: "Users occasionally see another user's name in the greeting after logging in."
> Reproduce: fails only when two logins happen in quick succession in the same browser session flow. Minimize: two accounts, one shared test browser, login A → logout → login B fast. Hypothesize: (1) cached profile response, (2) session not rotated, (3) greeting renders before profile fetch resolves using stale state. Instrument: network log shows B's profile request returns B's data, but the greeting renders 200ms earlier from a cached A response — hypothesis 1 confirmed, cache key is the endpoint URL without identity. Fix: scope the cache per identity + clear on logout; search finds the same cache used for the avatar (same fix applied). Regression test: automated A→B login sequence asserting the greeting text; fails on the old code, passes on the fix.

Anti-patterns: changing several things and re-testing ("shotgun debugging"), fixing where the error *appears* instead of where it *originates*, and declaring victory after one manual pass without a regression test.

**Minimal-change rule for bug fixes:** fix with the smallest reasonable diff. Never rewrite a working part as a side effect of a fix — a fix that also restructures invites new defects and makes the change unreviewable. If the right fix is structural (the root cause is the design, not a line), stop: record it and route it as its own change — a refactor or architecture task with its own tests and review — instead of smuggling it into the bug fix.

## 7. Performance Hygiene

- **Measure before optimizing.** Profile/timing first; the bottleneck is rarely where intuition says. An optimization without a before/after measurement is a guess wearing a costume.
- **N+1 detection:** a loop that issues a query/request per item is the most common self-inflicted wound. Signs: query count grows with list size; page slows linearly with data. Fix with batch loading/joins/includes — and verify the query count, not just the feeling.
- **Pagination by default:** every list endpoint and list UI has a default page size and a cap. "Return everything" is a decision that expires the first time the table grows.
- **Cache deliberately:** know what is cached, its key (identity-scoped where data is per-user — see the debugging example for the cost of getting this wrong), and its invalidation. A cache without an invalidation story is a stale-data generator.
- **Don't ship heavy work to the weakest client:** aggregate, filter, and paginate server-side; the low-end device constraint (when the project has one) is an implementation requirement, not a QA finding.
- Watch payload size, image weight, and synchronous work on request paths; move slow, non-urgent work to background jobs with status the user can see.

Symptom → first probe table:

| Symptom | Likely cause | First probe |
|---|---|---|
| List page slows as data grows | N+1 queries, or no pagination | Count queries for 10 vs. 100 rows |
| One endpoint is slow, others fine | Missing index on the filter column, or an external call in the request path | Query plan + timing breakdown (DB vs. network vs. code) |
| Everything slow at peak only | Connection/thread pool exhaustion, lock contention | Pool metrics and lock waits at peak, not at idle |
| Client feels janky on low-end devices | Oversized payloads, unoptimized images, main-thread work | Payload sizes + a low-end device profile run |
| Memory grows until restart | Unbounded cache/collection, leaked listeners/subscriptions | Heap snapshot diff over time |

## 8. Working in Code You Didn't Write

Most Gate 5 work happens in an existing codebase, not a green field. Rules for foreign territory:

- **Read before writing:** trace the flow you are about to change end-to-end (entry point → domain → data) before editing. The cost of reading is minutes; the cost of a wrong assumption is a defect.
- **Match the local idiom:** error style, naming, folder layout, test style. If the codebase does it a way you dislike, your task is not the moment to convert it — note it, and propose it separately if it matters.
- **Respect load-bearing quirks:** odd-looking code often encodes a past incident (a workaround, a race fix, a platform bug). Before "cleaning" it, check git history/comments/linked issues. If the reason is unrecoverable, add characterization tests (Section 5) before touching it.
- **Leave a map:** when you figure out something non-obvious about the area, the commit message or dev notes should carry it — the next reader may be you, with no memory of today.
- **Blame is a research tool, not a weapon:** history answers "why is it like this?" — use it for that, never to assign fault in review or notes.

Self-check before handing work to Code Review:

- [ ] The diff contains only this task's changes (no stray formatting sweeps, no unrelated fixes)
- [ ] Every new behavior has a test; every bug fix has a reproducing test
- [ ] No debug output, commented-out code, TODO-without-owner, or secrets in the diff
- [ ] Error paths were exercised, not just happy paths (kill the server, send the bad input, expire the token)
- [ ] The evidence bundle (build/test output, screenshots where UI changed) is attached per the playbook's standards
- [ ] Anything you knowingly left imperfect is written in the dev notes as a limitation — surprises belong to no one

## 9. Git Discipline

- **Atomic commits:** one logical change per commit; the commit builds and its tests pass. If you cannot describe the commit in one sentence without "and", split it.
- **Message format:** imperative subject ≤ ~72 chars saying WHAT and, when non-obvious, WHY in the body. Follow the repo's convention (e.g. Conventional Commits `feat:`, `fix:`, `refactor:`) if it has one.
  - Good: `fix: scope profile cache per user to stop cross-account greeting leak`
  - Bad: `fix bug`, `updates`, `wip`
- **Reviewable diffs:** keep changes as small as the task allows; separate mechanical changes (renames, formatting, moves) from behavioral changes into different commits/PRs — a 2,000-line diff with a 3-line behavior change hides the 3 lines.
- **Never commit:** secrets, credentials, `.env` files, build artifacts, or commented-out code blocks ("dead code with a tombstone"). Commented code gets deleted; git remembers it.
- **No history rewriting on shared branches;** no force-push to branches others build on.
- Committing/pushing happens only under the project's approval rule (see the repo's gate law) — preparing clean commits is Dev's job; deciding they land is the owner's.
