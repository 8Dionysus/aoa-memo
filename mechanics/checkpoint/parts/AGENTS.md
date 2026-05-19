# AGENTS.md

## Applies To

This card applies to `mechanics/checkpoint/parts/` and every nested active part.

## Role

`mechanics/checkpoint/parts/` holds functioning part contracts for the Checkpoint memo mechanic.

Parts are active operation nodes. They are not legacy indexes, source-doc dumps,
proof verdicts, runtime workers, route dispatchers, role policies, KAG substrate
truth, or owner-acceptance receipts.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/checkpoint/AGENTS.md`,
`mechanics/checkpoint/DIRECTION.md`, `mechanics/checkpoint/PARTS.md`,
`mechanics/checkpoint/OWNER_MAP.md`, `mechanics/checkpoint/PROVENANCE.md`, and the
nearest part `README.md`, `CONTRACT.md`, and `VALIDATION.md`.

## Boundaries

- Keep each part tied to one row in `mechanics/checkpoint/PARTS.md`.
- Keep detailed source meaning in the source docs named by the part.
- Keep former placement evidence in `mechanics/checkpoint/PROVENANCE.md` and `legacy/`.
- Route stronger proof, runtime, role, route, KAG, playbook, stats, ToS, or source-owner claims through `OWNER_MAP.md`.

## Validation

Use the package validation route in `mechanics/checkpoint/AGENTS.md`.

For part topology changes, also run:

```bash
python scripts/validate_memo_mechanic_parts.py
```

Before landing, run:

```bash
python scripts/release_check.py
```

## Closeout

Report active parts changed, whether source docs or artifacts moved, which
owner stop-lines stayed outside memo, and which package validation ran.
