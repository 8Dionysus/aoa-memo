# VALIDATION.md

On-demand human procedure for `mechanics/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/AGENTS.md`

```bash
  python scripts/mechanics/validate_mechanic_artifact_topology.py
  python scripts/mechanics/build_mechanic_artifact_inventory.py --check
  python scripts/mechanics/validate_mechanic_artifact_inventory.py
  ```
This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
```bash
  python scripts/mechanics/build_memo_mechanic_landing_logs.py --check
  python scripts/mechanics/validate_memo_mechanic_landing_logs.py
  python scripts/mechanics/build_memo_mechanic_readiness.py --check
  python scripts/mechanics/validate_memo_mechanic_readiness.py
  python scripts/mechanics/validate_memo_mechanics.py
  ```
```bash
  python scripts/mechanics/validate_memo_mechanic_parts.py
  ```
```bash
  python scripts/mechanics/build_memo_mechanic_cards.py --check
  python scripts/mechanics/validate_memo_mechanic_cards.py
  ```
```bash
  python scripts/mechanics/build_memo_mechanic_owner_routes.py --check
  python scripts/mechanics/validate_memo_mechanic_owner_routes.py
  ```
```bash
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```
This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
