# Operational Gate Landing Log

| Date | Change | Validation |
|---|---|---|
| 2026-05-19 | Moved operational-gate schemas, examples, and local regressions into functioning part-local homes. | `python scripts/release_check.py` |
| 2026-05-18 | Moved deployment incident gate, office incident gate, service revision ledger, and post-release memory boundary surfaces from flat `docs/` into `mechanics/operational-gate/docs/`. | `python scripts/release_check.py` |

## Stop-Lines Preserved

- `aoa-memo` does not approve releases or judge release quality.
- `aoa-memo` does not certify current service health.
- `aoa-memo` does not execute deployment, rollback, remediation, or runtime
  writes.
- `aoa-memo` does not own proof verdicts, smoke results, or regression gates.
- `aoa-memo` does not grant assistant or service role rights.
- `aoa-memo` does not own dispatch behavior, stats truth, or source meaning.
