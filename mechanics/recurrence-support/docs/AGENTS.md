# AGENTS.md

## Applies To

This card applies to `mechanics/recurrence-support/docs/`.

## Role

This directory owns active mechanic-owned doctrine and support notes for the
recurrence-support memo mechanic.

It is not a dispatch lane, runtime retry system, live scratchpad, role-rights
surface, proof bundle, scenario choreography lane, source acceptance record, or
legacy route.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/ARTIFACT_TOPOLOGY.md`,
`../AGENTS.md`, `../README.md`, `../PARTS.md`, `../OWNER_MAP.md`, and
`../PROVENANCE.md`.

When a doc points into schemas, examples, generated surfaces, quests, scripts,
or tests, read that district's nearest `AGENTS.md` before changing the linked
artifact.

## Boundaries

- Keep recurrence-support docs memory-only, evidence-linked, and
  operation-first.
- Do not claim route dispatch, runtime retry, live stores, role rights,
  identity continuity, eval verdicts, playbook acceptance, source truth, or
  owner acceptance.
- Keep witness trace technical artifacts in the recurrence-support package.
  Checkpoint artifacts belong in `mechanics/checkpoint/`; shared recall and
  quest artifacts remain in their owner districts.
- Do not introduce return-only memory-object families.
- Do not preserve old flat docs-root aliases as active routes.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_memo.py
python -m pytest -q mechanics/recurrence-support/tests/test_recurrence_support_mechanic.py tests/test_memo_validators.py mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/test_roadmap_parity.py
```

## Closeout

Report active recurrence-support docs changed, whether package-local contract
refs changed, whether artifact placement changed, and whether stronger owners
remain outside `aoa-memo`.
