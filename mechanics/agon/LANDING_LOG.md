# Agon Landing Log

## 2026-05-18

- Landed Agon as a memo mechanic package.
- Moved active Agon source docs from the transitional `mechanics/agon/docs/` district
  into `mechanics/agon/docs/`.
- Preserved former flat docs-root and docs-district lineage through the legacy
  index.
- Added owner map, provenance bridge, package card, and mechanics validation.

Validation route:

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
