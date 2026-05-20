# example-repo memo port index

Generated from `PORT.yaml` and local memo packets.

## Counts

| District | Count |
|---|---:|
| candidates | 1 |
| receipts | 1 |
| exports | 1 |
| local | 0 |

## Routes

| Route | Count |
|---|---:|
| `reviewed_intake` | 1 |

## Open Items

| ID | State | Route | Path |
|---|---|---|---|
| `candidate:example-repo:20260520T171200Z:codex-plane-memory-route` | `candidate` | `reviewed_intake` | `candidates/20260520T171200Z.codex-plane-memory-route.candidate.json` |

## Validate

```bash
python scripts/memory/validate_local_memo_port.py --path <memo>
python scripts/memory/build_local_memo_port_index.py --path <memo> --check
```
