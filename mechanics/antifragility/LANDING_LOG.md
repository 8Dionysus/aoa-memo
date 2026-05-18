# Antifragility Landing Log

## 2026-05-18

- Landed antifragility as a memo mechanic package.
- Moved active failure-lesson and recovery-pattern source docs from flat
  `docs/` paths into `mechanics/antifragility/docs/`.
- Preserved former flat docs-root lineage through the legacy index.
- Added owner map, provenance bridge, package card, generated mechanics
  coverage, AGENTS mesh coverage, and mechanics validation.

Validation route:

```bash
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```
