# VALIDATION.md

On-demand human procedure for `stats/AGENTS.md`.

## On-demand procedure

### Preserved route from `stats/AGENTS.md`

```bash
find memo/objects -name object.json -type f | sort
```
```bash
python scripts/release/validate_local_stats_port.py
```
