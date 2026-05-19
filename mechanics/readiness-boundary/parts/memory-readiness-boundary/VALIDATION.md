# Memory readiness boundary Validation

Executable validation for this part is routed through the package validation lane.

Run from the repository root:

```bash
python scripts/validate_memo_mechanic_parts.py
python -m pytest -q mechanics/readiness-boundary/parts/memory-readiness-boundary/tests
```

Then run the package-specific commands named in `../../AGENTS.md#validation` for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.
