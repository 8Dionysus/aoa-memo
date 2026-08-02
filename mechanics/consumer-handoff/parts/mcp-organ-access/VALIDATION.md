# MCP organ access Validation

Run from the repository root:

```bash
python -m pytest -q mechanics/consumer-handoff/parts/mcp-organ-access/tests
python scripts/mechanics/validate_memo_mechanic_parts.py
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/mechanics/build_mechanic_artifact_inventory.py --check
python scripts/mechanics/validate_mechanic_artifact_inventory.py
```

These checks prove owner source shape and authority stop-lines only. Runtime
catalog parity, credentials, consumer use, proof, acceptance, admission, and
rollback require separate evidence.
