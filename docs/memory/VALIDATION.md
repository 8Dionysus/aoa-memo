# VALIDATION.md

On-demand human procedure for `docs/memory/AGENTS.md`.

## On-demand procedure

### Preserved route from `docs/memory/AGENTS.md`

Shared executable routes remain owned by [`examples/memory-ports/VALIDATION.md`](../../examples/memory-ports/VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/memory/validate_memory_operations.py
python scripts/memory/validate_memory_surfaces.py
python scripts/memory/build_memory_operational_readouts.py --write --live
python scripts/memory/build_memory_operational_readouts.py --check --live
python scripts/memory/validate_abyss_machine_memory_object_bundle.py
```
