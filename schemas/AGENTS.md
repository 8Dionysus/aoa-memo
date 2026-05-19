# AGENTS.md

This file applies to JSON schemas under `schemas/`.

## Role of this directory

`schemas/` defines the public contract surface for `aoa-memo`.
These root files decide what counts as a valid shared memory object, recall
contract, provenance thread, and generated memo surface.

Schema edits are contract edits.
Treat them as changes to how the memory layer speaks, not as local cleanup.

Root schemas are also part of the root technical-district contract. Each
non-route schema file must be listed in exactly one
`config/root_technical_districts.json` `schema_families` entry that names the
owner surface, source refs, and validators.

For quick orientation, `generated/root_technical_districts.min.json` names this
district's role, route card, family ids, and local routing path.

## Route Stack

- Above: root `AGENTS.md`, docs doctrine, examples, and
  `config/root_technical_districts.json` decide why a schema is root-wide.
- Here: root schemas define shared memory, recall, provenance, support, and
  generated-surface contracts.
- Below: mechanic-owned schemas live under the owning package or part and must
  not drift into root without the artifact topology rule.

## Main schema groups

Keep these groups distinct:

- core memory object schemas such as `memory_object.schema.json`, `anchor.schema.json`, `state_capsule.schema.json`, `episode.schema.json`, `claim.schema.json`, `decision.schema.json`, `pattern.schema.json`, `bridge.schema.json`, and `audit_event.schema.json`
- recall and posture schemas such as `recall_contract.schema.json`, `trust_posture.schema.json`, `lifecycle_posture.schema.json`, and `decay_policy.schema.json`
- shared support-object schemas such as `provenance_thread.schema.json` and `core-memory-contract.schema.json`
- generated object-surface schemas such as `memory_object_catalog.schema.json`, `memory_object_capsules.schema.json`, `memory_object_sections.schema.json`, and `memory_object_surface_manifest.schema.json`

Do not blur memory objects, recall posture, and support exports into one generic shape.

Mechanic-owned schemas live under `mechanics/<owner>/schemas/`. Examples include
`mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_graph_face.schema.json`,
`mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json`, and
`mechanics/checkpoint/parts/checkpoint-carry-contract/schemas/inquiry_checkpoint.schema.json`.

## Editing posture

When you change a schema:

- preserve stable `$id` values unless a real contract migration is intended
- prefer additive changes over breaking renames or silent meaning drift
- keep required fields honest about temporal posture, provenance, and reviewability
- do not add fields that make memory look like proof, workflow policy, or routing authority
- update examples and generated surfaces that depend on the changed contract

If you change `memory_object_surface_manifest.schema.json`, `memory_object_catalog.schema.json`, `memory_object_capsules.schema.json`, or `memory_object_sections.schema.json`, review the generator-backed object family as one surface.

## Cross-file discipline

Keep alignment between:

- `recall_contract.schema.json` and the recall contract examples in `examples/`
- `memory_object.schema.json` and the per-kind examples plus `docs/MEMORY_OBJECT_PROFILES.md`
- `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_chunk_face.schema.json` and `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/schemas/memory_graph_face.schema.json` with the bridge examples and `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md`
- `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/schemas/checkpoint-to-memory-contract.schema.json` with `mechanics/checkpoint/parts/checkpoint-to-memory-mapping/examples/checkpoint_to_memory_contract.example.json` and `mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md`

If recall contracts expose a compact intermediate consumer step, keep that
`capsule_surface` additive, local-ref-valid, and aligned with the intended
generated family rather than inventing a new routing payload.

## Validation

After schema edits, run the validators that cover the affected surface:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
```

If a change touches generator-backed object surfaces, also run:

```bash
python scripts/generate_memory_object_surfaces.py
```
