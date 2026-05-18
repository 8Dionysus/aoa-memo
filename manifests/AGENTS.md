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
`config/root_technical_districts.json` `manifest_policy`, which must match the
root `manifests.allowed_files` list.

Mechanic-owned manifests live under the owning package. The Agon recurrence
manifests and their hook bindings live under:

- `mechanics/agon/manifests/recurrence/`
- `mechanics/agon/manifests/recurrence/hooks/`

Keep `component.agon.` records aligned with `mechanics/agon/docs/`,
`mechanics/agon/config/`, `mechanics/agon/generated/`,
`mechanics/agon/scripts/`, and `mechanics/agon/tests/`.

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

```bash
python mechanics/agon/scripts/validate_agon_memo_prebindings.py
python scripts/validate_memo.py
python scripts/release_check.py
```

## Closeout

Report which manifest family changed, which source surface owns the meaning,
whether hook bindings changed, and which validation ran.
