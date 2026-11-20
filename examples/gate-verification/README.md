# Gate verification examples

Two filled-in gate reports for the same fictional QA gate, checked by
`scripts/verify-gate.py`:

```bash
python3 scripts/verify-gate.py examples/gate-verification/good-report.md   # exits 0
python3 scripts/verify-gate.py examples/gate-verification/bad-report.md    # exits 1
```

- **good-report.md** — every mandatory item (all five UI states + responsive)
  is mapped to an executed test case with a real evidence file under
  `evidence/`; the not-tested list is explicitly `None.`
- **bad-report.md** — the 2026-11-20 failure pattern: a 40/40 green suite
  presented as proof of overall frontend quality. The script rejects it because
  the loading state has no test case (automatic BLOCKED), one evidence path
  does not exist, and the not-tested list holds unaccepted mandatory gaps.

The script verifies everything a report *declares*. Whether the coverage
matrix lists *all* mandatory items is checked against the role's gate
checklist — by the user at verdict time, or by CI.
