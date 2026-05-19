# Precedent and stay order Validation

Executable validation for this part is routed through the package validation lane.

Run from the repository root:

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
python -m pytest -q mechanics/governance/parts/governance-boundary/tests/test_governance_boundary_contracts.py
```

Then run the package-specific commands named in `../../AGENTS.md#validation` for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.
