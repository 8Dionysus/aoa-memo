# aoa-memo Skill Home

This directory is the canonical home for callable procedures owned specifically
by `aoa-memo`. It is not a mirror of the shared AoA catalog.

## Admitted bundle

| Bundle | Internal modes | Visibility | Admission |
| --- | --- | --- | --- |
| `aoa-memo` | fast `orient`; deep `recall`, `review`, `evolve` | OS-user-advertised | `docs/decisions/AOA-MEM-D-0083-two-speed-participation-spine.md` |

Fast orientation and the three deep modes share one trigger family, authority
ladder, and coexistence boundary. They remain one bundle until held-out manual
work proves that separate prompt-visible procedures improve outcomes.

Fast orientation exists so an ordinary persistent Codex session can notice
reviewed context without paying the full owner-package cost on every task. It
uses the existing read-only MCP brief as a locator, accepts silence, and
escalates to the strict deep route only when exact memory meaning is material.

`port.manifest.json` declares admitted source and selection by the single
OS-level `os-user-default` profile. Canonical files live under
`skills/aoa-memo/`; this repository does not duplicate the globally installed
bundle under `.agents/skills`.

## Verification posture

Manual tasks establish usefulness. Working validation commands live in
`skills/AGENTS.md`. The pinned `aoa-skills` source check validates identity,
admission, and package digest; the OS profile installer separately previews
collisions and verifies the managed user copy. Neither check proves routing,
model portability, safety, or outcome benefit.
