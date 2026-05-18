# AGENTS.md

## Applies To

This card applies to `mechanics/consumer-handoff/`.

## Role

The consumer-handoff mechanic owns memo-side handoff surfaces for neighboring
owners that consume memory while keeping stronger authority outside
`aoa-memo`.

It covers agent posture descriptors, playbook memory scopes, eval guardrail
handoff cases, KAG/ToS bridge and export faces, and orchestrator-facing recall
alignment.

It does not own actor identity, role rights, playbook choreography, proof
verdicts, graph substrate truth, Tree-of-Sophia source meaning, routing
implementation, orchestrator class identity, or runtime execution.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target
`docs/*.md` surface.

For schemas, examples, generated outputs, scripts, tests, quests, or manifests
that reference these handoff docs, read the nearest local `AGENTS.md` before
editing that district.

## Post-Change Review

After consumer-handoff changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- generated mechanics or AGENTS mesh companions
- generated memo registry, memory catalogs, KAG export, or quest catalogs
- validators and tests that pin consumer refs

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
python scripts/validate_memory_surfaces.py
python -m pytest -q mechanics/consumer-handoff/tests/test_consumer_handoff_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py mechanics/consumer-handoff/tests/test_playbook_memory_scopes.py mechanics/consumer-handoff/tests/test_downstream_feed_contracts.py tests/test_memo_validators.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report the handoff docs changed, whether examples/generated surfaces moved,
whether old flat docs-root references remain outside allowed provenance, and
which stronger owner boundaries stayed outside `aoa-memo`.
