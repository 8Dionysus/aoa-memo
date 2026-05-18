# AGENTS.md

## Applies To

This card applies to `mechanics/lineage-harvest/legacy/`.

## Role

This directory preserves lineage-harvest placement provenance.

It is not the active route. Active doctrine lives under
`mechanics/lineage-harvest/docs/`.

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
