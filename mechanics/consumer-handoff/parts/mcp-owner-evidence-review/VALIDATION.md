# MCP owner evidence review Validation

Run from the repository root:

```bash
python -m pytest -q mechanics/consumer-handoff/parts/mcp-owner-evidence-review/tests
python scripts/mechanics/validate_memo_mechanic_parts.py
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/mechanics/build_mechanic_artifact_inventory.py --check
python scripts/mechanics/validate_mechanic_artifact_inventory.py
```

These checks prove the source contract and negative boundaries. A real owner
review additionally requires a fresh signed capture, a committed source
revision, the deployed owner checkout at that exact revision, and a private
output directory.
