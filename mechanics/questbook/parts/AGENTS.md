# AGENTS.md

## Applies To

This card applies to `mechanics/questbook/parts/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Role

Questbook parts hold compact functioning contracts for the memo-side public
obligation mechanic.

They do not own root quest source files, root generated read models, proof,
route dispatch, runtime state, playbook choreography, role authority, or owner
acceptance.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/questbook/AGENTS.md`,
`../README.md`, `../PARTS.md`, and the narrow part README.

For generated-views changes, also read `generated/AGENTS.md`,
`../../ARTIFACT_TOPOLOGY.md`, and `../docs/QUEST_SOURCE_CONTRACT.md`.

## Boundaries

- Part docs describe active contracts; they are not raw inventories.
- Root `QUESTBOOK.md` remains the compact public index.
- Root `quests/` remains the lane-first public item store.
- Root `generated/quest_*.json` files remain root-published read models over
  the public item store, not package-local generated artifacts.
- Package-local generated artifacts may exist only when they serve one
  package-local mechanic boundary and are not public Questbook read models.

## Validation

Use the parent Questbook validation route:

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py --check
python scripts/validate_memo.py
```
