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
| `root-topology/root_technical_districts.json` | exact root files, bounded generated prefixes, and family contracts | `generated/root-topology/root_technical_districts.min.json` |

Use `generated/root-topology/root_technical_districts.min.json` for a fast map of root
district purpose, route card, family ids, and local routing. Use
`config/root-topology/root_technical_districts.json` when you need the exact file list,
bounded generated-prefix list, or family contract.

## Conditional route scope

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
For route-card or mechanic-map changes, add the matching checks:
For validation-lane changes, use the nearest `VALIDATION.md` route; reusable lanes remain in `config/validation_lanes.json`.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
