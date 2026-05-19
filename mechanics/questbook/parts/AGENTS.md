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

## Route Stack

- Above: the package `AGENTS.md` and `PARTS.md` decide which function nodes are
  active and what each part may own.
- Here: `parts/README.md` is the part index; each `parts/<part>/` directory is
  a functioning node with `README.md`, `CONTRACT.md`, and `VALIDATION.md`.
- Below: part-local schemas, examples, config, generated outputs, scripts,
  tests, manifests, and quests belong under the owning part when they serve
  only that part.
- Sideways: source docs stay in `../docs/`; placement history stays in
  `../PROVENANCE.md` and `../legacy/`.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/questbook/AGENTS.md`,
`../README.md`, `../PARTS.md`, and the narrow part README.

For quest-read-model-projections changes, also read `generated/AGENTS.md`,
`../../ARTIFACT_TOPOLOGY.md`, and `../docs/QUEST_SOURCE_CONTRACT.md`.

## Boundaries

- Part docs describe active contracts; they are not raw inventories.
- Root `QUESTBOOK.md` remains the compact public index.
- Root `quests/` remains the lane-first public item store.
- Root `generated/quests/quest_*.json` files remain root-published read models over
  the public item store, not package-local generated artifacts.
- Package-local generated artifacts may exist only when they serve one
  package-local mechanic boundary and are not public Questbook read models.

## Validation

Use the parent Questbook validation route:

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/memory/validate_memo.py
```
