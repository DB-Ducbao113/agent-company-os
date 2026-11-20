#!/usr/bin/env python3
"""verify-gate.py — mechanical checker for GATE-REPORT files.

Usage:  python3 scripts/verify-gate.py <report.md>

A gate report (templates/GATE-REPORT.template.md) is only submittable for the
user's verdict when this script exits 0. It enforces the Coverage law and the
Claim-scoping law (workflow/MASTER-WORKFLOW.md, Test-Case Gate law §7–9):

  1. The coverage matrix (§4) exists and has at least one row.
  2. Every coverage row names a real test case (NONE/empty = automatic BLOCKED).
  3. Every coverage row's evidence path exists on disk and is a non-empty file
     (paths resolve relative to the report's folder, then the working directory).
  4. Every coverage row's result is PASS (FAIL/BLOCKED rows block the gate).
  5. The "Not tested / not covered" list (§5) exists; every item on it must be
     marked [ACCEPTED GAP] (user accepted it in writing) or [OUT OF SCOPE].
  6. The §3 tally, when filled with real numbers, shows FAIL: 0 and BLOCKED: 0.

What it cannot check: whether the matrix lists ALL mandatory items — that set
comes from the role's gate checklist and the spec, and is confirmed by the user
(or CI diffing the matrix against the checklist). The script makes everything
the report DOES declare verifiable; the laws make omissions a visible violation.

Exit codes: 0 = submittable · 1 = violations found · 2 = usage/file error.
Pure standard library; no network; deterministic.
"""
import os
import re
import sys


def section(text, start_pat, end_pats=("^## ",)):
    """Return the body of the section whose heading matches start_pat."""
    lines = text.splitlines()
    start = None
    for i, ln in enumerate(lines):
        if re.match(start_pat, ln):
            start = i + 1
            break
    if start is None:
        return None
    body = []
    for ln in lines[start:]:
        if any(re.match(p, ln) for p in end_pats):
            break
        body.append(ln)
    return "\n".join(body)


def table_rows(sec):
    """Data rows of the first markdown table in a section (list of cell lists)."""
    rows = []
    in_table = False
    for ln in sec.splitlines():
        s = ln.strip()
        if s.startswith("|") and s.endswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", c or "---") for c in cells):
                in_table = True
                continue
            if in_table:
                rows.append(cells)
        elif in_table and s == "":
            continue
        elif in_table:
            break
    return rows


def main(argv):
    if len(argv) != 2:
        print(__doc__.splitlines()[2])
        return 2
    path = argv[1]
    if not os.path.isfile(path):
        print(f"ERROR: report not found: {path}")
        return 2
    text = open(path, encoding="utf-8").read()
    base = os.path.dirname(os.path.abspath(path))
    problems = []
    oks = []

    # --- §3 tally consistency -------------------------------------------------
    m = re.search(r"Gate test cases:\s*Total:\s*(\d+)\s*·\s*PASS:\s*(\d+)\s*·\s*FAIL:\s*(\d+)\s*·\s*BLOCKED:\s*(\d+)", text)
    if m:
        total, passed, failed, blocked = map(int, m.groups())
        if failed or blocked:
            problems.append(f"§3 tally shows FAIL: {failed}, BLOCKED: {blocked} — the gate cannot be PASS.")
        elif total != passed:
            problems.append(f"§3 tally inconsistent: Total {total} != PASS {passed} with no FAIL/BLOCKED.")
        else:
            oks.append(f"§3 tally consistent: {passed}/{total} PASS.")

    # --- §4 coverage matrix ----------------------------------------------------
    cov = section(text, r"^##\s*4\..*[Cc]overage")
    if cov is None:
        problems.append("§4 Coverage matrix section is missing.")
    if cov is not None:
        rows = table_rows(cov)
        if not rows:
            problems.append("§4 coverage matrix has no data rows.")
        for i, cells in enumerate(rows, 1):
            if len(cells) < 4:
                problems.append(f"§4 row {i}: expected 4 cells (item, test case, evidence, result), got {len(cells)}.")
                continue
            item, cases, evidence, result = cells[0], cells[1], cells[2], cells[3]
            label = item or f"row {i}"
            if not item:
                problems.append(f"§4 row {i}: mandatory item cell is empty.")
            if not cases or cases.upper() == "NONE":
                problems.append(f"§4 '{label}': no test case — automatically BLOCKED (Coverage law).")
            ev = evidence.strip("`[] ")
            if not ev:
                problems.append(f"§4 '{label}': evidence cell is empty.")
            else:
                cand = ev if os.path.isabs(ev) else os.path.join(base, ev)
                if not os.path.isfile(cand):
                    cand2 = os.path.join(os.getcwd(), ev)
                    cand = cand2 if os.path.isfile(cand2) else cand
                if not os.path.isfile(cand):
                    problems.append(f"§4 '{label}': evidence file does not exist: {ev}")
                elif os.path.getsize(cand) == 0:
                    problems.append(f"§4 '{label}': evidence file is empty: {ev}")
            if result.strip().upper() != "PASS":
                problems.append(f"§4 '{label}': result is '{result or '(empty)'}', not PASS — the gate cannot be PASS.")

    # --- §5 not tested ----------------------------------------------------------
    nt = section(text, r"^##\s*5\..*[Nn]ot tested")
    if nt is None:
        problems.append("§5 'Not tested / not covered' section is missing (it is mandatory; write 'None.' when empty).")
    else:
        items = [ln.strip() for ln in nt.splitlines() if ln.strip().startswith(("- ", "* "))]
        if not items and "None." not in nt:
            problems.append("§5 lists no items and does not state 'None.' — the section must be explicit.")
        for it in items:
            if "[ACCEPTED GAP]" not in it and "[OUT OF SCOPE]" not in it:
                problems.append(f"§5 unaccepted gap blocks PASS: {it[2:].strip()[:90]}")

    for o in oks:
        print(f"  OK   {o}")
    for p in problems:
        print(f"  FAIL {p}")
    if problems:
        print(f"VERIFY-GATE: FAIL — {len(problems)} violation(s). This report is NOT submittable for a PASS verdict.")
        return 1
    print("VERIFY-GATE: PASS — coverage matrix complete, evidence verified on disk, no unaccepted gaps.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
