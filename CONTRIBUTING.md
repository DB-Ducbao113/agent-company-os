# Contributing to Agent Company OS

Contributions are welcome — a new role, a better checklist, a sharper test case, a translation, a worked example.

## The rules that keep this repo coherent
1. **Everything is in English.** (Issues may be filed in any language; merged content is English.)
2. **Skills stay project-agnostic.** No real project names, companies, people, or data in skills/workflow/templates. Project facts belong in a user's own `PROJECT-PROFILE.md`, never here. Examples must be generic (a clinic, a course store, a booking app…).
3. **Every skill keeps the uniform structure** (see any existing SKILL.md): Role & Principles → When to Use / NOT Use → Inputs → What To Do → What To Use → What To Look Up → Outputs → Worked Example → Gate Checklist (+ Gate Test Cases) → Anti-Patterns → Handoff to the Next Role → References. A PR that breaks the structure will be asked to restore it — the uniformity is the product.
4. **Frontmatter must stay valid:** `name` = folder name (lowercase, hyphens), `description` ≤ 1024 characters stating what + when + triggers, body < 500 lines (push depth into `references/playbook.md`).
5. **Changes to the laws** (Constitution, gate law, test-case gate) require a rationale in the PR description and a CHANGELOG entry — these are the load-bearing walls.
6. **After editing any skill/template/workflow file**, regenerate the single-file edition: `bash scripts/build-full-context.sh`, and include the rebuilt `dist/FULL-CONTEXT.md` in the same PR.

## How to propose a change
- Small fixes (typos, a checklist item, a test case): open a PR directly.
- New role or workflow change: open an issue first describing the gap (which real situation the current repo handles badly), so the shape can be agreed before writing.
- When you fix a gap, say which workflow test case (docs/TESTING-GUIDE.md, WT-01…WT-10) or real failure exposed it, if any.

## Validation checklist for PRs (self-run)
- [ ] Frontmatter valid for every touched skill (name = folder, description ≤ 1024 chars)
- [ ] No project-specific content anywhere
- [ ] Internal references point at files that exist
- [ ] Version metadata bumped if a skill's behavior changed
- [ ] `dist/FULL-CONTEXT.md` rebuilt
- [ ] CHANGELOG.md entry added under "Unreleased"
