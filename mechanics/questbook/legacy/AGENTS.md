# AGENTS.md

## Applies To

This card applies to `mechanics/questbook/legacy/`.

## Role

Legacy preserves Questbook placement provenance for
`mechanics/questbook/legacy/`. It is not the active route for quest source
files, generated projections, or source-contract law. Use `legacy/INDEX.md`
for the placement map.

## Boundaries

- Keep active quest law in `mechanics/questbook/`.
- Keep active quest source files under `quests/`.
- Do not restore root flat quest aliases from legacy placement.
- Do not treat legacy as source truth.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```

## Closeout

Report only the relevant placement provenance and whether active Questbook
routes changed.
