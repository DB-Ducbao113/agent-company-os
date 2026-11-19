# Customizing this repo

## For a specific project
Edit exactly one file: `constitution/PROJECT-PROFILE.md` (from the template). Never stuff project facts into the skills — skills must stay reusable.

## For a role that should work differently
Edit that role's `SKILL.md` (your own workflow/checklists), keep the frontmatter `name` unchanged, and rewrite the `description` if the activation scope changes. Keep the four-part structure (What To Do / What To Use / What To Look Up / Handoff) so the chain stays predictable.

## Adding a new role
1. Create `skills/<role-name>/SKILL.md` following the existing skills' structure (role → when to use → inputs → what to do → what to use → what to look up → outputs → gate checklist → anti-patterns → handoff).
2. Add a row to `workflow/ROLE-CHAIN.md` and `workflow/ROUTING-MATRIX.md` (activation question + column in the task-type table).
3. Add the role's output template to `templates/` if it has one.
4. Add supporting external skills to `skills-index/SKILLS-INDEX.md`.

## Shrinking it for a small project
You may merge roles (one agent playing BA + Architect for a small task) but you may NOT drop: Gate 0 (clarify + spec), maker ≠ checker in Code Review/QA, and Security whenever auth/money/data is touched.
