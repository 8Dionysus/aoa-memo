# Quest read-model projections Validation

Use:

```bash
python scripts/validate_memo_mechanic_parts.py
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/validate_memo.py
```

`validate_quest_store.py` checks that the quest-read-model-projections part exists, names the
required root-published outputs, and agrees with the root technical district
family for Questbook projections.
