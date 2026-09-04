# Source contract Validation

This file owns the focused invocation(s) shown here; the package route adds wider checks.

Shared executable routes remain owned by [`mechanics/VALIDATION.md`](../../../VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python -m pytest -q mechanics/questbook/parts/source-contract/tests
```

Then follow the package-specific route in [`../../VALIDATION.md`](../../VALIDATION.md) for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.
