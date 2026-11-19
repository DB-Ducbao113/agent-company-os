# Playbook — QA / Tester (deep reference)

Technical detail for the QA Tester's `SKILL.md`: the ISTQB test design techniques
with fully worked examples, reporting standards, and operating strategy.

## 1. Equivalence Partitioning

**Idea:** divide the input domain into partitions the system processes the same
way; test one representative value per partition, plus the invalid partitions.

**Example:** a "purchase quantity" field accepts integers from 1 to 99.

| Partition | Type | Representative value |
|---|---|---|
| 1 – 99 | Valid | 10 |
| ≤ 0 | Invalid | 0 |
| ≥ 100 | Invalid | 150 |
| Not a number (text, empty, decimal) | Invalid | "abc", "", 2.5 |

At least one test case per partition. A common defect: the system validates the
valid partition correctly but "swallows" values or crashes on invalid ones — so
invalid partitions matter as much as valid ones.

## 2. Boundary Value Analysis

**Idea:** defects cluster at the boundaries of a range. For a boundary [min, max],
test: min−1, min, min+1, max−1, max, max+1 (the 3-value form) — at minimum
min−1, min, max, max+1 (the 2-value form).

**Continued example:** quantity 1–99 → test 0, 1, 2, 98, 99, 100.
**Money threshold example:** discount when an order is ≥ 500,000 → test 499,999,
500,000, 500,001.
**Length example:** password 8–64 characters → test 7, 8, 9, 63, 64, 65 characters.
**Date example:** valid until 31 Dec → test 31 Dec and 1 Jan of the next year; for
February in a leap year, test 28 and 29.

## 3. Decision Table

**Idea:** when the outcome depends on a combination of many conditions, enumerate
every meaningful combination so no case is missed.

**Example:** a discount policy. Conditions: C1 order ≥ 500,000; C2 customer is a
member; C3 code still valid.

| Rule | C1 | C2 | C3 | Expected result |
|---|---|---|---|---|
| R1 | T | T | T | 15% discount |
| R2 | T | F | T | 10% discount |
| R3 | T | T | F | No discount; report the code has expired |
| R4 | T | F | F | No discount; report the code has expired |
| R5 | F | T | T | No discount; report the threshold is not met |
| R6 | F | F | T | No discount; report the threshold is not met |
| R7 | F | * | F | No discount (both reasons) |

Each rule = at least one test case. If the full table is too large (2^n), reduce
it by merging combinations that produce the same outcome and where the remaining
condition's value does not matter (the * notation).

## 4. State Transition

**Idea:** for an entity with a lifecycle, test every valid state transition and
also attempt the forbidden ones.

**Example:** an order lifecycle: `Pending confirmation → Confirmed → Delivering →
Completed`, with a cancel branch: from `Pending confirmation` and `Confirmed` it
may move to `Cancelled`; `Completed` is a final state.

Tests must include:
- Each valid transition: perform it and verify the new state + the accompanying
  data (who performed it, the timestamp).
- Representative forbidden transitions: `Completed → Cancelled` must be blocked;
  `Delivering → Pending confirmation` (going backwards) must be blocked.
- Permissions per transition: which role may perform each transition (a customer
  may cancel only while still `Pending confirmation`…).
- Repeated actions: pressing confirm twice in a row — it must not jump two steps
  or create duplicate data.

## 5. Traceability Matrix

| AC | Test cases | Technique | Result | Related bug | Evidence |
|---|---|---|---|---|---|
| AC-03 (discount by threshold) | TC-11, TC-12, TC-13 | EP + BVA | PASS | — | run #7 |
| AC-04 (code usable once) | TC-14, TC-15 | Decision Table | FAIL → fixed → PASS | BUG-02 | runs #7, #9 |
| AC-05 (cancel by state) | TC-18, TC-19 | State Transition | PASS | — | run #8 |

How to read the matrix: a row whose Test cases column is empty = an unverified AC;
the Result column must reflect the most recent run on the build named in the report.

## 6. Quality Bug Reports

A bug report is up to standard if it answers 6 questions without follow-up:
1. Where is the defect (which screen/function/environment)?
2. How do you encounter it again (steps 1-2-3, with concrete data)?
3. What actually happens? 4. What should happen instead (point to the AC)?
5. How severe is it, and what is the blast radius? 6. Where is the evidence?

A good title states the symptom + the condition: "An order of 499,999 still gets a
10% discount when code X is applied" — instead of "Discount bug." Include the
frequency if it does not happen every time (always / sometimes / seen once).

## 7. Severity Table

| Level | Definition | Example | Gate impact |
|---|---|---|---|
| P0 — Critical | The system is unusable; data is lost/leaked; a serious security hole | Cannot log in; can see another user's data; data lost on save | Absolute block; stop testing the related area |
| P1 — Major | A main feature is wrong/broken with no acceptable workaround | Money calculated wrong; order state jumps incorrectly; discount code reusable | Blocks the gate until fixed and re-verified |
| P2 — Minor | A deviation with a workaround; a secondary feature is broken | List filtering wrong in one rare combination; an error message has wrong wording but the right code | Does not block if recorded with a fix plan |
| P3 — Trivial | Minor presentation issues with no behavioral impact | Slight spacing misalignment, a minor typo | Recorded; fixed in batches |

Severity is graded by **impact**, not by who reported it or how hard the fix is.
A 5-minute fix is still P1 if it calculates money wrong.

## 8. Regression Strategy

- **Fixed smoke set:** backbone flows + login + core features — run on every fix.
- **Impact-based regression:** identify where else the just-changed component is
  used (shared functions/services/screens) → test the AC that touch those places.
- **Full regression:** before a major release, or when a shared foundational
  component used everywhere is changed.
- **Automation priority:** test cases that run repeatedly, are stable, and are
  high-value → propose converting them to automated tests; exploratory and
  judgment-based checks stay manual.
- State clearly in the report: which regression scope ran, on which build — a
  generic "regression done" has no value.

## 9. Running Security Tests (the part Security hands over)

Execute them like ordinary test cases, plus these notes:
- Use two different accounts with the same role to test cross-access (change the
  ID in the URL/request).
- Use a low-privilege account to attempt high-privilege actions both in the UI
  (a hidden button is not enough) and via the API directly (the server must block it).
- Test tokens: expired, one character altered, and a token from a logged-out session.
- Malicious input: special characters, script-like content, extremely long
  strings, wrong-format/oversized files on upload.
- Every FAIL in this group: open a P0/P1 severity bug, copy Security, and never
  downgrade the level yourself.

## 10. Disciplined Exploratory Testing

- Every session has a charter: a goal ("explore the checkout flow on an unstable
  network"), a duration, and an area.
- Record your path and findings during the session; any finding that becomes a
  bug is converted into a bug report with reproduction steps, or into an
  additional regression test case if it is behavior that must be preserved.
- Exploratory testing complements the systematic techniques; it does not replace them.
