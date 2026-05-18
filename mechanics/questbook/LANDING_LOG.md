# Questbook Landing Log

## 2026-05-18

- Added Questbook as the memo mechanic for public memory-layer obligations.
- Moved flat root quest sources into lane-first lifecycle directories under
  `quests/`.
- Moved the generated quest projection builder into
  `mechanics/questbook/scripts/`.
- Added source-contract and quest-store validation for YAML and Markdown quest
  sources.

Validation route:

```bash
python mechanics/questbook/scripts/validate_quest_store.py
python mechanics/questbook/scripts/build_quest_surfaces.py --check
python scripts/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
