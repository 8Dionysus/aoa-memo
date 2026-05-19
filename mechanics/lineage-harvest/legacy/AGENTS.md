# AGENTS.md

## Applies To

This card applies to `mechanics/lineage-harvest/legacy/`.

## Role

This directory preserves lineage-harvest placement provenance.

It is not the active route. Active doctrine lives under
`mechanics/lineage-harvest/docs/`.

## Route Stack

- Above: the package `AGENTS.md`, `PROVENANCE.md`, and `OWNER_MAP.md` define
  the active route and stronger-owner boundary.
- Here: `INDEX.md` maps former paths to active surfaces, `DISTILLATION_LOG.md`
  records restoration decisions, and `raw/` contains historical snapshots.
- Below: `raw/` is evidence only. Do not edit it as current doctrine and do not
  cite it as an active route.

## Boundaries

- Do not add active lineage-harvest docs here.
- Do not treat legacy refs as source truth.
- Do not restore old flat docs-root paths as active aliases.
- Keep `legacy/INDEX.md` aligned when placement history changes.

## Validation

Run the mechanics validation lane after any legacy edit:

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
```
