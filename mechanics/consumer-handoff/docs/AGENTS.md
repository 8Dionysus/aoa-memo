# AGENTS.md

## Applies To

This card applies to `mechanics/consumer-handoff/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
consumer-handoff memo mechanic.

It is not a role policy lane, playbook choreography lane, eval proof bundle,
KAG substrate, ToS source-meaning mirror, routing implementation, orchestrator
class authority, runtime store, or legacy route.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

When a doc points into schemas, examples, generated surfaces, quests, scripts,
or tests, read that district's nearest `AGENTS.md` before changing the linked
artifact.

## Boundaries

- Keep consumer-handoff docs memory-only, source-linked, and operation-first.
- Do not claim actor rights, scenario authority, proof verdicts, graph
  normalization, source-authored ToS meaning, route dispatch, or runtime
  execution.
- Keep source refs and stronger owner names explicit.
- Do not add root technical artifacts here; use the artifact topology rule
  before moving schemas, examples, generated outputs, scripts, tests, quests,
  or manifests.
- Do not preserve old flat docs-root aliases as active routes.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_memo.py
python scripts/validate_memory_surfaces.py
python -m pytest -q mechanics/consumer-handoff/tests/test_consumer_handoff_mechanic.py mechanics/consumer-handoff/tests/test_playbook_memory_scopes.py mechanics/consumer-handoff/tests/test_downstream_feed_contracts.py tests/test_memo_validators.py
```

## Closeout

Report active consumer-handoff docs changed, whether generated/example refs
changed, whether artifact placement changed, and whether stronger owners
remain outside `aoa-memo`.
