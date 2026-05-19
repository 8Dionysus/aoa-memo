# AGENTS.md

## Applies To

This card applies to `mechanics/questbook/legacy/`.

## Role

Legacy preserves Questbook placement provenance for
`mechanics/questbook/legacy/`. It is not the active route for quest source
files, generated projections, or source-contract law. Use `legacy/INDEX.md`
for the placement map.

## Route Stack

- Above: the package `AGENTS.md`, `PROVENANCE.md`, and `OWNER_MAP.md` define
  the active route and stronger-owner boundary.
- Here: `INDEX.md` maps former paths to active surfaces, `DISTILLATION_LOG.md`
  records restoration decisions, and `raw/` contains historical snapshots.
- Below: `raw/` is evidence only. Do not edit it as current doctrine and do not
  cite it as an active route.

## Boundaries

- Keep active quest law in `mechanics/questbook/`.
- Keep active quest source files under `quests/`.
- Do not restore root flat quest aliases from legacy placement.
- Do not treat legacy as source truth.

## Validation

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/release/release_check.py
```

## Closeout

Report only the relevant placement provenance and whether active Questbook
routes changed.
