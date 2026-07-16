# aoa-memo Skill Home

This directory is the canonical home for callable procedures owned specifically
by `aoa-memo`. It is not a mirror of the shared AoA catalog.

## Admitted bundle

| Bundle | Internal modes | Visibility | Admission |
| --- | --- | --- | --- |
| `aoa-memo` | `recall`, `review`, `evolve` | repo-advertised | `docs/decisions/AOA-MEM-D-0076-aoa-memo-owner-skill-bundle.md` |

The three modes share one trigger family, authority ladder, result ABI, and
coexistence boundary. They remain one bundle until held-out manual work proves
that separate prompt-visible procedures improve outcomes.

`port.manifest.json` declares admitted source and the exact derived Codex
projection. Canonical files live under `skills/aoa-memo/`; files under
`.agents/skills/aoa-memo/` are generated copies.

## Verification posture

Manual tasks establish usefulness. Working validation commands live in
`skills/AGENTS.md`. Projection parity is checked in CI by the exact
`aoa-skills` action commit pinned in `.github/workflows/repo-validation.yml`.
For a local checkout of that same contract, preview before writing and use
`--prune` only after inspecting every undeclared projection entry. A green
structural check does not prove routing, model portability, safety, or outcome
benefit.
