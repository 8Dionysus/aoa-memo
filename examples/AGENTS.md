# AGENTS.md

This file applies to public example artifacts under `examples/`.

## Role of this directory

`examples/` holds reviewable, sanitized, public memo examples.
They demonstrate how schemas, docs, and generated surfaces fit together.

Examples here are not private notes and not hidden runtime state.
Everything in this directory should stay safe to publish and easy to validate.

## Example families

Keep the example families legible:

- core memory-object examples such as `anchor.example.json`, `state_capsule.example.json`, `episode.example.json`, `claim.example.json`, `pattern.example.json`, `bridge.kag-lift.example.json`, and `checkpoint_approval_record.example.json`
- lifecycle and audit examples such as `claim.current-entrypoint.example.json`, `claim.superseded.example.json`, `claim.retracted.example.json`, `audit_event.supersession.example.json`, `audit_event.retraction.example.json`, and `provenance_thread.lifecycle.example.json`
- bridge and support examples such as `checkpoint_to_memory_contract.example.json`, `witness_trace.example.json`, `memory_chunk_face.bridge.example.json`, `memory_graph_face.bridge.example.json`, `memory_eval_guardrail_pack.example.json`, and `inquiry_checkpoint.example.json`
- recall contract examples such as `recall_contract.working.json`, `recall_contract.semantic.json`, `recall_contract.lineage.json`, `recall_contract.router.semantic.json`, `recall_contract.router.lineage.json`, `recall_contract.object.working.json`, `recall_contract.object.semantic.json`, and `recall_contract.object.lineage.json`
- the curated object-surface manifest `memory_object_surface_manifest.json`

Not every file here is a memory object.
Some files are support contracts or router-facing recall entrypoints.
Keep those roles explicit.

## Editing posture

When updating examples:

- preserve public-safe, sanitized content
- keep timestamps, provenance, lifecycle posture, and trust posture explicit
- keep local refs valid and reviewable
- do not smuggle secrets, private infrastructure details, or hidden operational notes into example payloads
- do not let examples imply that memory is proof or current truth without temporal framing

For recall contracts, keep inspect and expand surfaces aligned with the intended family:

- router-facing recall contracts point to `generated/memory_catalog.min.json` and `generated/memory_sections.full.json`
- object-facing recall contracts point to `generated/memory_object_catalog.min.json` and `generated/memory_object_sections.full.json`
- doctrine-first examples may point to docs such as `docs/KAG_TOS_BRIDGE_CONTRACT.md` or `docs/RUNTIME_WRITEBACK_SEAM.md` when deeper explanation is the intended expand surface

## Validation

After editing examples, run:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
```

If you changed curated object examples or `memory_object_surface_manifest.json`, regenerate the object-facing family before finishing:

```bash
python scripts/generate_memory_object_surfaces.py
```
