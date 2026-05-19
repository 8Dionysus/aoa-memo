# Questbook Provenance Bridge

Use active surfaces first:

- [README](README.md)
- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [parts](parts/README.md)
- [OWNER_MAP](OWNER_MAP.md)
- [QUEST_SOURCE_CONTRACT](docs/QUEST_SOURCE_CONTRACT.md)
- [QUESTBOOK](../../QUESTBOOK.md)
- [quests](../../quests/README.md)

The current Questbook mechanic grew from the former flat root quest store:
`quests/AOA-MEM-Q-*.yaml` and Agon follow-through markdown files in root
`quests/`. The active model now follows the Agents-of-Abyss pattern: this
mechanic owns quest law and generated projections, while root `quests/` remains
the public item store with lane-first lifecycle placement.

Active part-local tool placement:

- `mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py`
- `mechanics/questbook/parts/source-contract/tests/test_questbook_store.py`
- `mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py`

Use [legacy/INDEX](legacy/INDEX.md) only to audit former placement. Legacy
paths are historical receipts, not active contracts.
