# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/docs/`.

## Role

`mechanics/checkpoint/docs/` holds active mechanic-owned doctrine for
checkpoint memory.

It is not a runtime checkpoint runbook, proof ledger, route policy, playbook
script, or role authorization surface.

## Route Stack

- Above: the package `AGENTS.md`, `README.md`, `PARTS.md`, and `OWNER_MAP.md`
  set the operation and stronger-owner split.
- Here: `docs/README.md` maps the source family; individual docs own active
  mechanic doctrine and support notes.
- Adjacent: package or part artifact homes own schemas, examples, config,
  generated outputs, scripts, tests, manifests, and quests. Use
  `mechanics/ARTIFACT_TOPOLOGY.md` before moving root technical artifacts.
- Below: no nested active law is expected here; legacy context routes through
  `../PROVENANCE.md` and `../legacy/`.

## Read Before Editing

Read:

1. root `AGENTS.md`
2. `mechanics/AGENTS.md`
3. `mechanics/checkpoint/AGENTS.md`
4. `mechanics/checkpoint/README.md`
5. `mechanics/checkpoint/OWNER_MAP.md`
6. the target doc

Use `mechanics/ARTIFACT_TOPOLOGY.md` before moving checkpoint schemas,
examples, generated outputs, scripts, or tests.

## Boundaries

- Keep docs active, checkpoint-specific, and source-linked.
- Route checkpoint execution and runtime state to `abyss-stack`.
- Route actor rights to `aoa-agents`.
- Route checkpoint play to `aoa-playbooks`.
- Route dispatch and return navigation to `aoa-routing`.
- Route proof to `aoa-evals`.
- Route center doctrine to `Agents-of-Abyss`.

## Validation

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/checkpoint/parts/checkpoint-memory-boundary/tests/test_checkpoint_mechanic.py tests/memory/test_memo_schema_contracts.py tests/memory/test_memo_memory_context_boundaries.py
```

Before landing, also run:

```bash
python scripts/release/release_check.py
```
