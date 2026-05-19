# AGENTS.md

## Applies To

This card applies to `mechanics/consumer-handoff/legacy/`.

## Role

`legacy/` preserves old consumer-handoff placement provenance through
`legacy/INDEX.md`.

It is not the active route for consumer-handoff docs, not a source of current
authority, and not a place to park active schemas, examples, generated outputs,
scripts, tests, quests, manifests, runtime receipts, or downstream owner
doctrine.

## Route Stack

- Above: the package `AGENTS.md`, `PROVENANCE.md`, and `OWNER_MAP.md` define
  the active route and stronger-owner boundary.
- Here: `INDEX.md` maps former paths to active surfaces, `DISTILLATION_LOG.md`
  records restoration decisions, and `raw/` contains historical snapshots.
- Below: `raw/` is evidence only. Do not edit it as current doctrine and do not
  cite it as an active route.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `../AGENTS.md`, `../README.md`,
and `../PROVENANCE.md`.

## Boundaries

- Keep legacy entries short and route-like.
- Do not add old-path aliases back into active docs.
- Do not treat former flat docs-root paths as current contracts.
- Do not move active consumer-handoff docs here.
- Do not use legacy entries to grant actor rights, scenario authority, proof,
  graph truth, routing behavior, or runtime execution.

## Validation

```bash
python scripts/mechanics/validate_memo_mechanics.py
python scripts/mechanics/build_memo_mechanics_index.py --check
python scripts/mechanics/validate_memo_mechanics_index.py
```

## Closeout

Report whether legacy provenance changed and whether the active route still
points to `mechanics/consumer-handoff/docs/`.
