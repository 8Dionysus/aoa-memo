# AGENTS.md

This file applies to public example artifacts under `examples/`.

## Role of this directory

`examples/` holds reviewable, sanitized, public memo examples.
They demonstrate how schemas, docs, and generated surfaces fit together.

Examples here are not private notes and not hidden runtime state.
Everything in this directory should stay safe to publish and easy to validate.

Root examples are part of the root technical-district contract. Each non-route
example file must be listed in exactly one
`config/root_technical_districts.json` `example_families` entry that names the
owner surface, source refs, and validators.

## Example families

Keep the example families legible:

- core memory-object examples such as `anchor.example.json`, `state_capsule.example.json`, `episode.example.json`, `claim.example.json`, and `pattern.example.json`
- lifecycle and audit examples such as `claim.current-entrypoint.example.json`, `claim.superseded.example.json`, `claim.retracted.example.json`, `audit_event.supersession.example.json`, `audit_event.retraction.example.json`, and `provenance_thread.lifecycle.example.json`
- recall contract examples such as `recall_contract.working.json`, `recall_contract.semantic.json`, `recall_contract.lineage.json`, `recall_contract.router.semantic.json`, `recall_contract.router.lineage.json`, `recall_contract.object.working.json`, `recall_contract.object.semantic.json`, and `recall_contract.object.lineage.json`
- the curated object-surface manifest `memory_object_surface_manifest.json`

Not every file here is a memory object.
Some files are support contracts or router-facing recall entrypoints.
Keep those roles explicit.

The curated object-surface manifest may reference public memory-object
examples under a mechanic package when the example's owner boundary is
mechanic-local. In that case, keep the example under `mechanics/<slug>/examples/`
or the nearest `mechanics/<slug>/parts/<part>/examples/` home and regenerate
the object-facing generated family from the root manifest.

Mechanic-owned examples live under their package lane:

- `mechanics/consumer-handoff/parts/kag-tos-bridge-handoff/examples/` for KAG/ToS bridge and graph/chunk face examples
- `mechanics/consumer-handoff/parts/eval-guardrail-handoff/examples/` for eval guardrail handoff examples
- `mechanics/consumer-handoff/parts/kag-source-export/examples/` for KAG donor/export seed examples
- `mechanics/checkpoint/parts/<part>/examples/` for inquiry checkpoint, checkpoint-to-memory, approval, health, checkpoint improvement, and checkpoint review examples
- `mechanics/writeback/parts/<part>/examples/` for quest chronicle, self-agency, rollback, and revision-ledger examples
- `mechanics/recurrence-support/examples/` for witness trace examples
- `mechanics/agon/parts/<part>/examples/`, `mechanics/titan/parts/<part>/examples/`, and the other mechanic package or part examples for their local contracts

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
- doctrine-first examples may point to docs such as `mechanics/consumer-handoff/docs/KAG_TOS_BRIDGE_CONTRACT.md` or `mechanics/writeback/docs/RUNTIME_WRITEBACK_SEAM.md` when deeper explanation is the intended expand surface

If a recall contract also publishes `capsule_surface`, keep it additive and
family-aligned:

- router-facing doctrine recall contracts use `generated/memory_capsules.json`
- object-facing semantic or lineage recall contracts use `generated/memory_object_capsules.json`
- `capsule_surface` stays a compact hydrate step between inspect and expand, not a new recall family

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
