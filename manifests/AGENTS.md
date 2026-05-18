# AGENTS.md

## Guidance for `manifests/`

`manifests/` holds recurrence manifests that describe memo-facing component
surfaces and their hook bindings.

These files route repeatable memory-layer obligations. They do not own memory
truth, proof, role rights, KAG graph semantics, or runtime retention.

## Current Shape

The current manifest family is `manifests/recurrence/` and includes
`component.agon.*` surfaces plus matching hook manifests under
`manifests/recurrence/hooks/`.

Keep `component.agon.` records aligned with `docs/agon/`, config seeds,
generated registries, tests, and quests that define the Agon memo seam.

## Boundaries

- Keep manifests public-safe and deterministic.
- Do not place private traces, secrets, local host paths, or raw runtime state
  here.
- Do not let recurrence manifests become live schedulers or proof verdicts.
- Route runtime execution to runtime owners and role authority to `aoa-agents`.

## Validation

When manifests change, run the narrow validator for the affected surface and
then the broad memo gate:

```bash
python scripts/validate_memo.py
python scripts/release_check.py
```

## Closeout

Report which manifest family changed, which source surface owns the meaning,
whether hook bindings changed, and which validation ran.
