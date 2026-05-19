# Recurrence Support Landing Log

| Date | Change | Validation |
|---|---|---|
| 2026-05-19 | Moved witness trace schema, example, and regression into `mechanics/recurrence-support/parts/witness-trace-contract/` so the witness part owns its technical contract. | `python -m pytest -q mechanics/recurrence-support/parts/witness-trace-contract/tests`; `python scripts/release_check.py` |
| 2026-05-18 | Moved recurrence support, witness trace contract, and reviewed closeout recall landing surfaces from flat `docs/` into `mechanics/recurrence-support/docs/`. | `python scripts/release_check.py` |

## Stop-Lines Preserved

- `aoa-memo` does not own recurrence doctrine or center program law.
- `aoa-memo` does not decide dispatch, tier escalation, or return navigation.
- `aoa-memo` does not execute runtime retry, rebuild, checkpoint worker, or
  live scratchpad behavior.
- `aoa-memo` does not grant actor rights or identity continuity.
- `aoa-memo` does not own proof verdicts, scoring, or adoption decisions.
- `aoa-memo` does not own playbook scenario choreography or owner acceptance.
- `aoa-memo` does not create a new `return_memory` object family.
