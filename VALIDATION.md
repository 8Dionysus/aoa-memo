# VALIDATION.md

On-demand human procedure for the repository root.

## On-demand procedure

Run the repository-wide CI modes from the repository root when the change crosses their corresponding surface:

```bash
python scripts/ci_gate.py --mode source-fast
python scripts/ci_gate.py --mode generated
python scripts/ci_gate.py --mode memory
python scripts/ci_gate.py --mode tests
```

### Frozen release gate

```bash
python scripts/release/release_check.py
```
