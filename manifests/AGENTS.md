# AGENTS.md

## Guidance for `manifests/`

`manifests/` is reserved for shared recurrence manifests that are not owned by
one mechanic package.

Shared manifests can route repeatable memory-layer obligations. They do not own
memory truth, proof, role rights, KAG graph semantics, runtime retention, or a
mechanic package's local artifact contract.

## Current Shape

There are no active shared manifests in root `manifests/` right now.
That empty state is machine-checked by
`config/root-topology/root_technical_districts.json` `manifest_policy`, which must match the
root `manifests.allowed_files` list.
`generated/root-topology/root_technical_districts.min.json` carries the compact public atlas
entry for this reserved district.

Mechanic-owned manifests live under the owning package or nearest functioning
part. Agon recurrence manifests and their hook bindings live under:

- `mechanics/agon/parts/prebinding-and-candidate-intake/manifests/recurrence/`
- `mechanics/agon/parts/bridge-and-evidence-seams/manifests/recurrence/`
- `mechanics/agon/parts/stage-landing-and-stop-lines/manifests/recurrence/`

Keep `component.agon.` records aligned with `mechanics/agon/docs/`,
the relevant `mechanics/agon/parts/<part>/config/`,
`mechanics/agon/parts/<part>/generated/`,
`mechanics/agon/parts/<part>/scripts/`, and
`mechanics/agon/parts/<part>/tests/`.

## Conditional route scope

- Above: root `AGENTS.md`, `config/root-topology/root_technical_districts.json`, and the
  owning mechanic decide whether a manifest is shared or mechanic-local.
- Here: root `manifests/` is reserved for shared recurrence manifests.
- Below: active mechanic manifests belong under the owning package or part
  alongside their config, generated, scripts, and tests.

## Boundaries

- Keep manifests public-safe and deterministic.
- Do not place private traces, secrets, local host paths, or raw runtime state
  here.
- Do not let recurrence manifests become live schedulers or proof verdicts.
- Route runtime execution to runtime owners and role authority to `aoa-agents`.

## Validation

When root shared manifests change, add the shared source surface and run the
broad memo gate. When mechanic-local manifests change, run the owning mechanic
validator first:
## Closeout

Report which manifest family changed, which source surface owns the meaning,
whether hook bindings changed, and which validation ran.

## Validation route

Use the nearest `VALIDATION.md` route only after the touched surface is known; reusable lanes remain in `config/validation_lanes.json`.
