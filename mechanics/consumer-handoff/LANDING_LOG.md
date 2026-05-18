# Consumer Handoff Landing Log

| Date | Change | Validation |
|---|---|---|
| 2026-05-18 | Moved the downstream feed regression from root `tests/` into `mechanics/consumer-handoff/tests/` and kept root tests limited to cross-mechanic regressions. | `python scripts/release_check.py` |
| 2026-05-18 | Moved agent, playbook, eval, KAG/ToS, KAG export, and orchestrator alignment handoff surfaces from flat `docs/` into `mechanics/consumer-handoff/docs/`. | `python scripts/release_check.py` |

## Stop-Lines Preserved

- `aoa-memo` does not grant role rights or actor identity.
- `aoa-memo` does not author playbook choreography.
- `aoa-memo` does not score, prove, or provide proof of memory quality.
- `aoa-memo` does not normalize graph truth or activate KAG federation.
- `aoa-memo` does not rewrite Tree-of-Sophia source meaning.
- `aoa-memo` does not own route dispatch or runtime execution.
