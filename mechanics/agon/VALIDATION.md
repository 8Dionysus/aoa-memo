# VALIDATION.md

On-demand human procedure for `mechanics/agon/AGENTS.md`.

## On-demand procedure

### Preserved route from `mechanics/agon/AGENTS.md`

Shared executable routes remain owned by [`mechanics/VALIDATION.md`](../VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_memo_prebindings.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_epistemic_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_kag_memo_evidence_package_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_mechanical_trial_memo_intakes.py
python mechanics/agon/parts/prebinding-and-candidate-intake/scripts/validate_agon_retention_rank_memo_bridge.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_slc_memo_bridge_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_sophian_memo_evidence_registry.py
python mechanics/agon/parts/bridge-and-evidence-seams/scripts/validate_agon_vds_memo_bridge.py
python -m pytest -q mechanics/agon/parts
```
This surface owns only the focused or composite invocations shown here; linked parent routes own wider/shared lanes.
