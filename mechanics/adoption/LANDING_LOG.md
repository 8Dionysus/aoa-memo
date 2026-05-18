# Adoption Landing Log

## 2026-05-18

- Landed adoption as a memo mechanic package.
- Moved active adoption source docs from flat `docs/` paths into
  `mechanics/adoption/docs/`.
- Added owner map, provenance bridge, legacy index, and mechanics validation.

Validation route:

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
