# MCP owner evidence review Validation

Shared executable routes remain owned by [`mechanics/VALIDATION.md`](../../../VALIDATION.md); follow those on-demand lanes for this surface.
```bash
python -m pytest -q mechanics/consumer-handoff/parts/mcp-owner-evidence-review/tests
```

These checks prove the source contract and negative boundaries. A real owner
review additionally requires a fresh signed capture, a committed source
revision, the deployed owner checkout at that exact revision, and a private
output directory.
