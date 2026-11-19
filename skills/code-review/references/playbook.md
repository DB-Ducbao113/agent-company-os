# Code Review Playbook — Deep Reference

> Read while reviewing in Gate 5. SKILL.md gives the workflow; this file gives the lookup detail.

## 1. The Review Order per Google Engineering Practices (Detail)

This order exists because a finding's value decreases along it: a design defect makes the whole change
pointless, a style defect only makes the code slightly uglier. Never reverse it.

### 1. Design (the design of the change)
- Does the change belong in this system, this layer, this module?
- Is its interaction with the other parts sound: new dependencies, dependency cycles, duplicating an existing function?
- Is this the right time to introduce this change (too early/too late relative to the locked architecture)?
- Does it match the API contract and the related architecture decisions (ADRs)?

### 2. Functionality
- Does the code do what the user/spec needs — including the edge cases the author thought about least?
- Concurrency: two simultaneous requests, a user double-clicking, a job re-running — can data be corrupted?
- Are errors handled and *visible*, or swallowed so the system goes wrong in silence?
- For UI: can a real user complete the job; are waiting/error states clear?

### 3. Complexity
- Can each function/class be understood quickly by someone else? If the reviewer must read it 3 times to understand → too complex.
- Is there an abstraction built for an imagined need (nobody needs it yet)?
- Does the change make a currently simple module harder to modify later?

### 4. Tests
- Does new/changed behavior have corresponding tests; are the tests part of this same change?
- Would the tests *fail if the code were wrong* (check by asking: invert the logic — do the tests go red)?
- Are there tests for edges and error cases, or only the happy path?
- Are the tests fragile: dependent on system time, run order, the real network/data?

### 5. Naming
- Do variable/function/class names convey the correct business meaning, without implying the opposite?
- Are names consistent with the terminology in the spec/codebase?

### 6. Comments
- Good comments explain *why* (reason, constraint, warning). Comments that repeat *what* the code already says → remove them.
- Has the code change made a nearby comment/document wrong? A wrong comment is more dangerous than no comment.

### 7. Style
- Check only the parts of the project's style guide that automated tools (linter/formatter) do not already cover.
- Never turn a personal preference into a requirement; if it is not in the project's style guide, it is at most a [NIT] prefixed with "Nit:".

## 2. The Severity Label Scale

| Label | Meaning | The author must |
|---|---|---|
| [BLOCKER] | Merging would cause a functional defect, data loss, a security hole, a contract/architecture break, or a SEC-REQ violation | Fix it + provide evidence; the reviewer closes the finding before merge is allowed |
| [SHOULD FIX] | A real problem (hard to maintain, a missing test for secondary behavior, incomplete error handling) that does not cause harm immediately | Fix it in this change, or record tracked follow-up work accepted by the approver |
| [NIT] | A small thing: a slightly unclear name, a redundant comment, style outside the linter | Optional; skipping it needs no long explanation |

Additional convention (per Google): purely optional comments should open with "Nit:" / "Optional:" /
"Consider:" so the author can distinguish them from mandatory requests. Every unlabeled finding is by
default read as mandatory — so labeling is the reviewer's responsibility, not the author's guesswork.

## 3. Security-Sensitive Pattern List (sweep in every diff)

**Authentication & permissions**
- A new endpoint/action with no authentication check or role check.
- Permission checked only in the frontend/route while the service/data layer does not re-check it.
- Fetching a record by a client-supplied ID without an ownership check (IDOR/BOLA).
- Accepting an object from the client and writing it straight through (mass assignment): forbidden fields like role, balance, or approval status become editable.

**Input & queries**
- Concatenating input into SQL/commands/queries/templates (injection).
- Reflected input not escaped for its context (server-rendered XSS).
- File/directory paths taken from input without normalization + confinement to a root directory (path traversal).
- The server fetching a user-supplied URL without an allowlist (SSRF).

**Secrets & data**
- Secrets/API keys/tokens in code, committed config files, logs, or error messages.
- Logs containing passwords, tokens, or raw personal data.
- Responses returning more fields than the receiver needs, especially sensitive fields.
- Home-grown encryption/hashing; passwords stored in plaintext or with a weak hash; secrets compared with a regular comparison (timing).

**Configuration & dependencies**
- TLS certificate verification disabled, debug enabled in production configuration, CORS opened to `*` together with credentials.
- A new dependency from an obscure source, or a version with a published vulnerability.
- File uploads: no type/size limits, trusting the file extension, storing into an executable directory.

When you see a pattern: record a finding + a severity based on its real impact in this project's context;
when unsure → call Security; never downgrade it to a [NIT] yourself.

## 4. Comment Examples — Bad vs Good

**Bad:** "This part isn't written well, redo it."
→ No location, no reason, no idea what to change it into, no indication whether it is mandatory.

**Bad:** "Why would you write it like this???"
→ About the person, not the code.

**Good:** `[BLOCKER] services/order.ts:87 — The total is taken from the client's request instead of being
recomputed on the server from the base price; a user who modifies the request can buy at price 0
(violates BR-04 and SEC-REQ-01). Suggestion: drop the total field from the input, compute it on the
server; add a test "client sends a different total → the server ignores it".`

**Good (minor level):** `[NIT] utils/date.ts:12 — The name 'fmt2' does not state the target format;
consider 'formatDateForDisplay' to match the naming in this module. Not mandatory.`

A good comment always has 4 parts: **label → location → consequence → suggestion.** Without the
consequence, the author cannot judge importance; without the suggestion, the fix loop drags on.

## 5. Review Speed and Attitude (per Google)

- Review early and respond fast in small rounds rather than accumulating one giant review: an author who
  waits long gets discouraged, and the quality of subsequent changes drops with it.
- A "perfect" review does not exist; the standard is: does this change make the system *better overall*,
  and is there any [BLOCKER]-class finding? Never block a merge indefinitely chasing perfect code.
- Praise good points when you see them (a good test, an elegant handling) — briefly, in the right place.
  A review that only criticizes teaches authors to hide problems instead of surfacing them early.
- A long argument that will not settle → meet directly / escalate to the decision-maker, then record the
  conclusion in the review file. Never let a PR die in silence.
