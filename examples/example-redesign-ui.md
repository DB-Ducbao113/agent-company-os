# WORKED EXAMPLE — Task: "Redesign the interface, make it look better"

> A generic example (not tied to any specific project) showing how Gate 0 runs end to end.

**Raw task:** "Redesign the interface, make it look better." → Ambiguous on 6 of 8 dimensions → the Orchestrator must NOT start work.

**Clarifying round (5 questions, each with options + a proposed default):**
1. Scope: (A) everything (B) just the main screen + the main action screen (C) a screen you name? *Proposed default: B.*
2. "Not good-looking" means: (A) colors/fonts (B) messy layout (C) doesn't look like a professional product (D) all three? *Default: D.*
3. Reference to learn from: you name one, or the agent researches 3–5 real products and presents a comparison first? *Default: research first.*
4. Existing design system/brand: (A) keep the framework, refine it (B) start fresh? *Default: A.*
5. You approve via: (A) static board (B) clickable prototype (C) running build? *Default: board → approve → code.*

**Playback:** "Redesign the look + layout of the 2 main screens, keeping the existing design-system framework and business flows, researching real products before drawing anything, you approve the board before any code. Out of scope this round: the remaining screens, the backend, feature changes." → The user confirms.

**Routing:** Architect (locks the compliance frame) → UI/UX (research → board, all 5 states) → Developer FE → QA (board vs. build comparison + regression on existing flows) → Release when ordered. BA reduced to scope lines inside the spec (no business change). Security/Integration skipped with stated reasons (no auth/API changes).
