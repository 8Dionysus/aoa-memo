# AGENTS.md

## Applies To

This card applies to `mechanics/adoption/parts/` and every nested active part.

## Role

`mechanics/adoption/parts/` holds functioning part contracts for the Adoption memo mechanic.

Parts are active operation nodes. They are not legacy indexes, source-doc dumps,
proof verdicts, runtime workers, route dispatchers, role policies, KAG substrate
truth, or owner-acceptance receipts.

## Conditional route scope

- Above: the package `AGENTS.md` and `PARTS.md` decide which function nodes are
  active and what each part may own.
- Here: `parts/README.md` is the part index; each `parts/<part>/` directory is
  a functioning node with `README.md`, `CONTRACT.md`, and `VALIDATION.md`.
- Below: part-local schemas, examples, config, generated outputs, scripts,
  tests, manifests, and quests belong under the owning part when they serve
  only that part.
- Sideways: source docs stay in `../docs/`; placement history stays in
  `../PROVENANCE.md` and `../legacy/`.

## Conditional source route
When this task touches the path, consult root `AGENTS.md`, `mechanics/AGENTS.md`, `mechanics/adoption/AGENTS.md`,
`mechanics/adoption/DIRECTION.md`, `mechanics/adoption/PARTS.md`,
`mechanics/adoption/OWNER_MAP.md`, `mechanics/adoption/PROVENANCE.md`, and the
nearest part `README.md`, `CONTRACT.md`, and `VALIDATION.md`.

## Boundaries

- Keep each part tied to one row in `mechanics/adoption/PARTS.md`.
- Keep detailed source meaning in the source docs named by the part.
- Keep former placement evidence in `mechanics/adoption/PROVENANCE.md` and `legacy/`.
- Route stronger proof, runtime, role, route, KAG, playbook, stats, ToS, or source-owner claims through `OWNER_MAP.md`.

## Validation

Use the package validation route in `mechanics/adoption/AGENTS.md`.

For part topology changes, also run:
Before landing, run:
## Closeout

Report active parts changed, whether source docs or artifacts moved, which
owner stop-lines stayed outside memo, and which package validation ran.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
