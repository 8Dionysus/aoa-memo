# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/docs/`.

## Role

`mechanics/checkpoint/docs/` holds active mechanic-owned doctrine for
checkpoint memory.

It is not a runtime checkpoint runbook, proof ledger, route policy, playbook
script, or role authorization surface.

## Conditional route scope

- Above: the package `AGENTS.md`, `README.md`, `PARTS.md`, and `OWNER_MAP.md`
  set the operation and stronger-owner split.
- Here: `docs/README.md` maps the source family; individual docs own active
  mechanic doctrine and support notes.
- Adjacent: package or part artifact homes own schemas, examples, config,
  generated outputs, scripts, tests, manifests, and quests. Use
  `mechanics/ARTIFACT_TOPOLOGY.md` before moving root technical artifacts.
- Below: no nested active law is expected here; legacy context routes through
  `../PROVENANCE.md` and `../legacy/`.

## Conditional source route
When a task touches this path, consult only the relevant entries:

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
- Route dispatch and return navigation to `aoa-sdk`.
- Route proof to `aoa-evals`.
- Route center doctrine to `Agents-of-Abyss`.

## Validation
Before landing, also run:

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
