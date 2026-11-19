# AI Feature UX — Designing Features That Contain AI

> Read this whenever the feature being designed CONTAINS AI: chat assistants, text/image
> generation, summarization, recommendations, copilots, smart search, classification.
> A deterministic screen either works or it doesn't. An AI feature is a **distribution,
> not a binary** — the same input class produces a range of outputs, some wrong. The UX
> discipline below exists to make that distribution safe and legible to the user.

## 1. The core shift

- "Done" for an AI feature means: a **target acceptable-output rate on a scoped input
  class** (defined with the BA as rate-based acceptance criteria), plus a **graceful
  tail** — every output below the bar must fail visibly, recoverably, and without
  damaging user data or trust.
- Design the failure and recovery flows with the same care as the happy path. For AI
  features, recovery is not an edge case; statistically, it is a main flow.
- One confidently wrong output presented as fact can destroy trust in the whole
  feature. When the system is unsure, the interface must show that — uncertainty is
  information, not weakness.
- **Scope the input class.** The acceptable-output rate is only meaningful against a
  defined class of inputs ("questions about the user's own orders", not "any
  question"). The design must make that scope visible — placeholder text, example
  prompts, and out-of-scope handling all teach the user what the feature is for.
  Inputs outside the class route to the Refused state (§4), not to an improvised answer.
- **Design the graceful tail explicitly.** For each AI flow, name in advance what the
  user gets when output is bad: a retry with a different phrasing, a form that captures
  the request for a human, a link to the non-AI way of doing the same task. If the
  tail is "the user gives up", the feature is not designed yet.

## 2. Pattern checklist (apply every item that fits)

| Pattern | What it requires in the design |
|---|---|
| Streaming output | Long generations render progressively with a visible generating state, a stop/cancel control, and no layout jump when the stream completes |
| Citations / provenance | Factual claims generated from sources carry visible citations or source links the user can open; uncited generated claims are visually distinguishable from sourced ones |
| Confidence / uncertainty display | Low-confidence results are marked as such (label, hedging language, visual treatment); the UI never presents a guess with the same authority as a verified fact |
| Human override | Every AI-produced artifact can be edited, corrected, or replaced by the user before it takes effect; the AI's version is a draft until the user accepts it |
| Undo at every step | Every AI-initiated change offers undo for a reasonable window; "the AI did it" is never a dead end |
| Escalation to a human | A visible path from the AI flow to a human (support, reviewer, approver) when the AI cannot help, keeps failing, or the user asks |
| Error recovery as a primary flow | Retry, regenerate, rephrase, and "start over" are first-class actions; a failed generation preserves the user's input and context |
| Capability disclosure | The interface shows what the AI can and cannot do in this feature (scope, data it uses), before the user relies on it |
| Feedback capture | Beyond thumbs up/down: capture corrections, regenerations, and edits — the correction itself is the highest-value signal (see §6) |
| Input guidance | Example prompts, scope hints, and structured inputs (chips, templates, pickers) that steer users into the input class the feature handles well — guidance is cheaper than recovery |

## 3. Autonomy tiers — match autonomy to the cost of error

Decide the tier per action, not per feature. State the tier in `03-design.md`.

| Tier | Behavior | Use when |
|---|---|---|
| 1 — Suggest | AI proposes; nothing happens until the user acts on the proposal | Default starting tier for any new AI capability |
| 2 — Approve | AI prepares the complete action; the user reviews and confirms before it executes | The action has real effects but is reversible, or review is cheap |
| 3 — Act with review | AI executes; the result is surfaced for after-the-fact review with undo | Low cost of error, high volume, fully reversible |

Hard rules:
- **Irreversible actions are always gated by human confirmation**, regardless of tier:
  sending, paying, deleting, publishing, changing permissions, anything another person
  will see or rely on.
- Autonomy may only be raised with evidence (measured acceptable-output rate on real
  usage), never by default or by schedule. Record the evidence when the tier changes.
- The tier is visible in the UI where it matters: the user must be able to tell whether
  they are looking at a suggestion, a pending action awaiting their approval, or a
  completed action they can still undo.

## 4. The AI states — extension to the component anatomy

The standard 5 states (default, loading, empty, error, success) are not enough for AI
components. Every AI component spec must also cover:

| State | Design requirement |
|---|---|
| Generating | Progressive/streaming rendering, elapsed indication for long runs, stop control |
| Partial | An interrupted or truncated result is marked as partial — never silently presented as complete |
| Low-confidence | Visually distinct treatment + the wording tells the user to verify; offer the verification path (source, human, retry) |
| Refused | The AI declined (out of scope, policy, missing data): say why in user language and offer the nearest allowed alternative or the human path |
| Failed | Generation errored: preserve input, offer retry/regenerate, never show a blank or a fake result |
| Overridden | The user edited or replaced the AI output: the UI reflects the user's version as authoritative; do not silently re-apply the AI version |

## 5. AI disclosure — a design deliverable, not a legal footnote

- Users must be told **they are interacting with AI, clearly, at the first
  interaction** — in the interface itself. A line in the terms and conditions does
  not count as disclosure.
- AI-generated content that could be mistaken for human or factual content carries a
  visible "AI-generated" label; where the platform supports it, generated media also
  carries **machine-readable marking** (metadata/watermarking) so the marking survives
  copying and re-sharing.
- Disclosure design is part of `03-design.md` for any feature that interacts with
  users as AI or generates synthetic content — reviewed at the gate like any other
  screen, not appended afterward.
- Do not design anthropomorphism that implies capabilities the system does not have
  (a name, avatar, and typing indicator are fine; implying memory, feelings, or
  authority the system lacks is not).

## 6. Anti-patterns

| Anti-pattern | Why it breaks |
|---|---|
| Fake confidence | Presenting every output with identical certainty and polish, including guesses — the user cannot calibrate trust, and the first visible error discredits everything |
| Silent failure | A failed or refused generation shows an empty state, a generic error, or worst of all a plausible-looking fabricated result |
| No-undo automation | AI actions that execute irreversibly with no confirmation and no undo path |
| Thumbs-up as the only feedback | Thumbs reward confident, agreeable answers — including confidently wrong ones. Track corrections, regenerations, and escalations instead (QA uses these as production health signals) |
| Automation creep | Quietly raising the autonomy tier (suggest → auto-apply) without new evidence or a design review |
| Human-looking deception | Avatars/names/persona copy that lead users to believe they are dealing with a person |
| Dead-end refusal | "I can't help with that" with no reason, no alternative, and no human path |

## 7. Worked micro-example — a support-chat assistant

Feature: an in-app assistant that answers questions about the user's own orders.

- **Input class (scoped):** order status, delivery, returns for the signed-in user's
  orders. Anything else → Refused state with a link to human support and to the
  general help center. The placeholder text says exactly this scope.
- **Tiers:** answering = Tier 1 (suggest — text only). Drafting a return request =
  Tier 2 (the assistant fills the form; the user reviews and submits). Submitting the
  return itself is never automated: irreversible-ish and user-visible, so it stays
  behind the user's own confirmation click.
- **States in the spec:** Generating (streamed answer + stop), Low-confidence (order
  lookup returned conflicting data → answer is hedged, shows both sources, offers the
  human path), Refused (question about another person's order → explains why, offers
  support), Failed (lookup service down → preserves the question, retry button, and a
  "check order status manually" link as the graceful tail).
- **Disclosure:** a persistent "AI assistant — answers may be wrong; verify order
  details on the order page" line at the top of the chat, shown before the first
  message is sent. Exported chat transcripts carry an "AI-generated" header.
- **Feedback captured:** corrections via "this is wrong" → reason picker; every
  escalation to a human is logged with the conversation ID — these feed QA's
  production health signals, not a thumbs counter.

## 8. Gate additions for AI features

When the feature contains AI, `03-design.md` must additionally record:
- [ ] The autonomy tier per AI action, with the irreversible actions listed and their confirmation design
- [ ] All six AI states (§4) designed for every AI component
- [ ] The confidence/uncertainty treatment: what triggers "low-confidence" display and what it looks like
- [ ] The disclosure design (§5): where the AI disclosure appears and how generated content is labeled/marked
- [ ] The recovery flows: retry/regenerate/edit/escalate, reachable from every AI failure state
- [ ] The feedback signals the UI captures (corrections, regenerations, escalations) and where they surface
