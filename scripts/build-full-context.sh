#!/usr/bin/env bash
# Build dist/FULL-CONTEXT.md — the single-file version of this repo for chat AIs
# that cannot browse a whole repository. Run from the repo root:
#   bash scripts/build-full-context.sh
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="dist/FULL-CONTEXT.md"
mkdir -p dist

add() { # add <title> <file>
  if [ -f "$2" ]; then
    { echo ""; echo "---"; echo ""; echo "# ===== $1 — $2 ====="; echo ""; cat "$2"; echo ""; } >> "$OUT"
  fi
}

{
  echo "# AGENT COMPANY OS — FULL CONTEXT (single-file edition)"
  echo ""
  echo "This file concatenates the whole Agent Company OS repository into one document so a chat AI"
  echo "can read it in a single fetch or upload. Rules: follow AGENTS.md first; every new task starts"
  echo "at the orchestrator-intake skill; read a role's section before acting in that role."
  echo ""
  echo "Generated: $(date +%F)"
} > "$OUT"

add "ENTRY POINT" "AGENTS.md"
add "CONSTITUTION" "constitution/CONSTITUTION.md"
add "PROJECT PROFILE TEMPLATE" "constitution/PROJECT-PROFILE.template.md"
add "MASTER WORKFLOW" "workflow/MASTER-WORKFLOW.md"
add "ROLE CHAIN" "workflow/ROLE-CHAIN.md"
add "ROUTING MATRIX" "workflow/ROUTING-MATRIX.md"
for d in skills/*/; do
  add "SKILL" "${d}SKILL.md"
  add "SKILL PLAYBOOK" "${d}references/playbook.md"
done
for f in templates/*.md; do add "TEMPLATE" "$f"; done
add "EXTERNAL SKILLS INDEX" "skills-index/SKILLS-INDEX.md"
add "WORKED EXAMPLE" "examples/example-redesign-ui.md"

echo "Built $OUT ($(wc -l < "$OUT") lines, $(du -h "$OUT" | cut -f1))"
