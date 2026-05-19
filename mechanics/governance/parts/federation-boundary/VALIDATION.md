# Federation boundary Validation

Executable validation for this part is routed through the package validation lane.

Run from the repository root:

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
python -m pytest -q tests/mechanics/test_cross_mechanic_candidate_contracts.py mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests/test_lineage_harvest_mechanic.py
```

Then run the package-specific commands named in `../../AGENTS.md#validation` for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.
