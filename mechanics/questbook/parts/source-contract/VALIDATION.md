# Source contract Validation

Executable validation for this part is routed through the package validation lane.

Run from the repository root:

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python -m pytest -q mechanics/questbook/parts/source-contract/tests
```

Then run the package-specific commands named in `../../AGENTS.md#validation` for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.
