# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/`.

## Role

The checkpoint mechanic owns memo-side checkpoint memory: bounded checkpoint
gates, carry packets, approval records, health records, improvement threads,
and checkpoint-to-memory mappings.

It keeps checkpoint artifacts public, source-linked, and reviewable. It does
not own checkpoint execution, runtime stores, retry policy, actor rights,
proof verdicts, route dispatch, playbook choreography, or owner acceptance.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target `docs/*.md`
surface.

For schemas, examples, generated outputs, scripts, tests, quests, or manifests
that reference checkpoint memory, read the nearest local `AGENTS.md` before
editing that district.

## Boundaries

- Keep checkpoint surfaces memory-only, evidence-linked, and operation-first.
- Do not claim checkpoint execution, runtime persistence, retry scheduling,
  role rights, route dispatch, proof, playbook acceptance, or source-owner
  acceptance.
- Do not create a new durable memory-object kind for checkpoints. Map
  checkpoint artifacts into existing object kinds such as `state_capsule`,
  `decision`, `episode`, `audit_event`, `claim`, `pattern`, `bridge`, and
  `provenance_thread`.
- Keep recurrence return posture with `mechanics/recurrence-support/` unless
  the surface is the checkpoint artifact itself.
- Keep generic writeback governance with `mechanics/writeback/`; this package
  owns only the checkpoint-specific source contract that writeback consumes.
- Keep old root examples or root schemas out of active references once the
  checkpoint package owns the artifact.

## Post-Change Review

After checkpoint changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- checkpoint package docs, schemas, examples, and tests
- recurrence-support and writeback consumer refs
- generated mechanics, AGENTS mesh, memory object surfaces, and writeback
  companions
- docs-root maps, root route cards, decision records, changelog, or roadmap

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_memo.py
python -m pytest -q mechanics/checkpoint/tests/test_checkpoint_mechanic.py tests/test_memo_validators.py tests/test_downstream_feed_contracts.py tests/test_memo_mechanics.py tests/test_agents_mesh.py tests/test_mechanic_artifact_topology.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report checkpoint docs changed, whether package-local artifacts and consumer
refs stayed owner-routed, whether old root examples or schema refs remain, and
which stronger owner boundaries stayed outside `aoa-memo`.
