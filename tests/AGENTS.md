# AGENTS.md

## Guidance for `tests/`

`tests/` protects memory schemas, examples, generated catalogs, recall contracts, lifecycle audit examples, retired docs district checks, memo mechanics, and writeback boundaries.

Tests should expose provenance loss, recall overreach, stale context, schema mismatch, AGENTS mesh drift, and generated/source drift.

Root tests are part of the root technical-district contract. Each non-route
test file or public fixture must be listed in exactly one
`config/root-topology/root_technical_districts.json` `test_families` entry that names the
owner surface and protected refs.

`tests/root-topology/test_root_technical_districts_index.py` protects the compact district
atlas in `generated/root-topology/root_technical_districts.min.json` so root folder routing
can be inspected without opening the full allowlist first.

## Route Stack

- Above: source docs, schemas, examples, scripts, generated companions, and
  `config/root-topology/root_technical_districts.json` name what root tests protect.
- Here: root tests protect repo-wide and cross-mechanic invariants.
- Below: package-local mechanic tests live under the owning package or part
  when they protect a single mechanic operation.

Do not update expected outputs without checking the source-owned memory docs, schemas, or examples that own the meaning.

Keep fixtures public-safe. No private memories, secrets, hidden telemetry, or unreduced personal data.

Verify with:

```bash
python -m pytest -q tests
python scripts/agents/validate_semantic_agents.py
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/mechanics/validate_mechanic_artifact_inventory.py
python scripts/root-topology/validate_root_technical_districts_index.py
python scripts/mechanics/validate_memo_mechanic_parts.py
python scripts/mechanics/validate_memo_mechanic_readiness.py
python scripts/agents/validate_agents_mesh.py
python scripts/agents/validate_agents_mesh_index.py
python scripts/root-topology/validate_docs_districts.py
```
