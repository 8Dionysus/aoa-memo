# Agon Landing Log

## 2026-05-18

- Landed Agon as a memo mechanic package.
- Moved active Agon source docs from the transitional `mechanics/agon/docs/` district
  into `mechanics/agon/docs/`.
- Preserved former flat docs-root and docs-district lineage through the legacy
  index.
- Added owner map, provenance bridge, package card, and mechanics validation.
- Moved Agon-specific quest follow-through notes from flat root `quests/` into
  the public `quests/agon/ready/` lane and gave them the memo Markdown quest
  source contract.

Validation route:

```bash
python mechanics/questbook/scripts/validate_quest_store.py
python scripts/validate_memo_mechanics.py
python scripts/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
