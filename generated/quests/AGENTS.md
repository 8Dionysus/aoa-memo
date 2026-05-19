# AGENTS.md

Route card for `generated/quests/`.

## Purpose

This district holds generated Questbook read-model projections.

## Source

Quest source truth routes to `quests/`, `QUESTBOOK.md`, and
`mechanics/questbook/`.

## Route

- Up: `generated/AGENTS.md`, then `AGENTS.md`.
- Across: `mechanics/questbook/parts/quest-read-model-projections/`.
- Downstream: consumers may inspect generated quest catalog and dispatch only
  as read models.

## Validate

```bash
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
```
