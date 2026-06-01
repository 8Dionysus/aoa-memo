# AGENTS.md

## Guidance for `config/`

`config/` holds repo-wide source maps for route cards, memo mechanics,
validation lanes, and root technical districts. These files are
guardrail-support inputs for builders and validators; they help the memory
layer stay inspectable without becoming memory truth.

## District Card

| Surface | Use for | Companion |
|---|---|---|
| `agents/agents_mesh.json` | current AGENTS route-card contracts | `generated/agents/agents_mesh.min.json` |
| `validation_lanes.json` | current validation and release command lanes, with effective validator layer metadata | `docs/validation/COMMAND_AUTHORITY.md`, `docs/validation/validator_inventory.json`, `scripts/validation_lanes.py` |
| `mechanics/memo_mechanics.json` | current memo mechanic package contracts | `generated/mechanics/memo_mechanics.min.json` |
| `root-topology/root_technical_districts.json` | exact root technical district allowlist and family contracts | `generated/root-topology/root_technical_districts.min.json` |

Use `generated/root-topology/root_technical_districts.min.json` for a fast map of root
district purpose, route card, family ids, and local routing. Use
`config/root-topology/root_technical_districts.json` when you need the exact file list or
family contract.

## Route Stack

- Above: root `AGENTS.md`, `DESIGN.AGENTS.md`, and
  `mechanics/ARTIFACT_TOPOLOGY.md` decide why a config surface is repo-wide.
- Here: config names the source map, family contracts, and validation refs.
- Below: generated companions, scripts, tests, schemas, examples, manifests,
  and mechanic packages follow the owning family named here.

## Editing Route

When config changes:

1. identify the family being changed
2. update the source owner named in that family
3. rebuild the affected generated companion
4. run the matching validator
5. inspect the diff for recall or provenance drift

Keep config public-safe, local-ref based, and reviewable. Secret tokens, private
memories, local-only host paths, and hidden retention rules belong nowhere in
this directory.

## Validation

For root technical district changes, run:

```bash
python scripts/mechanics/validate_mechanic_artifact_topology.py
python scripts/root-topology/build_root_technical_districts_index.py --check
python scripts/root-topology/validate_root_technical_districts_index.py
```

For route-card or mechanic-map changes, add the matching checks:

```bash
python scripts/memory/validate_memo.py --profile schema
python scripts/memory/validate_memo.py --profile memory-context
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

For validation lane changes, run:

```bash
python scripts/root-topology/validate_validator_topology.py
python -m pytest -q tests/root-topology/test_validation_lanes.py tests/root-topology/test_validator_topology.py tests/root-topology/test_ci_gate.py tests/root-topology/test_release_check.py
```
