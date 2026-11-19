# EXAMPLE — A filled PROJECT-PROFILE (fictional project, for learning the format)

> This is what `constitution/PROJECT-PROFILE.md` looks like when filled in well. The project below is invented.
> Notice how specific the invariants are — vague profiles produce vague compliance.

# PROJECT PROFILE — BookMyClinic (fictional)

## 1. What the project is
- Name / one-line description: BookMyClinic — patients book appointments with independent clinics online.
- Who the end users are: patients (mostly mobile, 35–65 years old) and clinic receptionists (desktop).
- The core value it delivers: a confirmed appointment in under 2 minutes, with an SMS reminder.
- Current stage: ☑ in operation

## 2. Technology (decided — the agent must not change it unilaterally)
- Frontend: Next.js 15 + TypeScript, Tailwind, shadcn/ui components only
- Backend: Next.js API routes + Supabase (Postgres)
- Database / BaaS: Supabase, region Singapore
- Auth: Supabase Auth, phone OTP for patients, email+password for clinics
- Hosting / deploy: Vercel (production = `main` branch)
- Repo: github.com/example/bookmyclinic — working branch: feature branches off `main` — special notes: never push directly to `main`

## 3. Design system & brand
- Existing design system / tokens: `src/styles/tokens.css` + shadcn theme — comply, never invent a parallel system
- Primary colors / typography: teal #0F766E primary, neutral grays, font Inter
- Logo / brand assets: `public/brand/` — use as-is, never redraw
- Icon system: Lucide only — no emoji as icons
- Aesthetic references: calm healthcare products, large tap targets, generous whitespace
- Anti-references: dense dashboards, dark mode (not offered), playful/cartoon illustration

## 4. Invariants (never break)
- No double-booking: one appointment per doctor per slot, enforced by a DB unique constraint, not by UI checks
- Patient data is health data: never logged, never sent to analytics, masked in admin views except for receptionists of that clinic
- All money amounts stored as integer minor units; no floating point for prices
- No commit/push until the project owner approves a preview build

## 5. Operating constraints
- Low-end devices / slow-network users a priority: ☑ yes (patients on old Android phones; pages must stay light)
- Budget / hard deadlines: none standing
- Compliance standards: ☑ WCAG AA

## 6. How the project owner reviews
- Review format: ☑ running build (preview URL)
- Who gives final approval: the project owner, in chat, per gate
