# AGENTS.md

This file applies to helper and validator scripts under `scripts/`.

## Role of this directory

`scripts/` is the operational seam for `aoa-memo`.
It validates the memory layer, regenerates the object-facing surface family, and checks that examples, schemas, registry surfaces, and recall contracts stay aligned.

These scripts should remain small, reviewable, and honest about what they validate.
Do not turn them into hidden runtime infrastructure.

## Main script families

Keep the current split clear:

- `validate_memo.py` is the canonical memory-layer validator and now also checks nested guidance surfaces
- `validate_memory_surfaces.py` checks the doctrine family under `generated/` plus router-facing recall contracts
- `generate_memory_object_surfaces.py` rebuilds the object-facing family from curated examples
- `validate_memory_object_surfaces.py` checks manifest coverage, determinism, lifecycle integrity, and object-facing recall contracts
- `validate_lifecycle_audit_examples.py` checks lifecycle, provenance-thread, and audit-event example integrity
- `validate_nested_agents.py` checks that local guidance files stay present and explicit

## Editing posture

When editing scripts here:

- preserve small, direct validator logic over framework sprawl
- keep error messages specific and reviewable
- do not silently widen repository ownership from memory semantics into routing, proof, or runtime policy
- keep generator behavior deterministic
- avoid adding hidden network calls, secret handling, or environment-specific assumptions

If a validator starts depending on a new contract, update the matching nested `AGENTS.md`, examples, schemas, and generated surfaces together.

When validating recall contracts with a compact intermediate step, keep
`capsule_surface` checks explicit and local-ref-based. Validators here should
confirm family alignment without turning capsules into routing policy.

## Validation

After changing scripts, run the affected entrypoints directly. The common sequence is:

```bash
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python scripts/validate_memory_object_surfaces.py
python scripts/validate_lifecycle_audit_examples.py
```

If generator logic changed, also run:

```bash
python scripts/generate_memory_object_surfaces.py
```
