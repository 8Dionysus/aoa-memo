# Questbook Landing Log

## 2026-05-19

- Moved the Questbook source validator into
  `mechanics/questbook/parts/source-contract/scripts/`.
- Moved the generated quest projection builder into
  `mechanics/questbook/parts/generated-views/scripts/`.
- Moved the Questbook regression into
  `mechanics/questbook/parts/source-contract/tests/`.
- Preserved the root `QUESTBOOK.md`, root `quests/`, and root generated
  projection outputs as intentional public surfaces.

Validation route:

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py --check
python -m pytest -q mechanics/questbook/parts/source-contract/tests
python scripts/release_check.py
```

## 2026-05-18

- Added `parts/generated-views/` as the functioning-part contract for
  root-published Questbook generated read models.
- Kept `generated/quest_catalog.min*.json` and
  `generated/quest_dispatch.min*.json` in root `generated/` because they are
  public read models over root `quests/`, not package-local generated
  artifacts.
- Strengthened the Questbook validator so the part contract, root technical
  district family, required outputs, and builder agree.
- Preserved stop-lines: no source quest state, proof, route dispatch, playbook
  choreography, runtime state, role authority, owner acceptance, or private
  memory.

Validation route:

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py --check
python scripts/validate_memo_mechanic_parts.py
python -m pytest -q mechanics/questbook/parts/source-contract/tests/test_questbook_store.py tests/test_memo_mechanic_parts.py
python scripts/release_check.py
```

## 2026-05-18

- Added Questbook as the memo mechanic for public memory-layer obligations.
- Moved flat root quest sources into lane-first lifecycle directories under
  `quests/`.
- Added the generated quest projection builder to the Questbook mechanic.
- Added source-contract and quest-store validation for YAML and Markdown quest
  sources.

Validation route:

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py --check
python scripts/release_check.py
```

## Stop-lines preserved

- No proof, runtime, role, route, source owner acceptance, or stronger-owner
  authority moved into memo.
