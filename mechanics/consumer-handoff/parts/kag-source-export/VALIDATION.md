# KAG source export Validation

Executable validation for this part is routed through the package validation lane.

Run from the repository root:

```bash
python scripts/mechanics/validate_memo_mechanic_parts.py
python mechanics/consumer-handoff/parts/kag-source-export/scripts/generate_kag_export.py
python scripts/memory/validate_memo.py
```

Then run the package-specific commands named in `../../AGENTS.md#validation` for any changed source docs, schemas, examples, generated companions, scripts, tests, manifests, or owner routes.
