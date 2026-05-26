# Functional AGENTS Route Cards

- Decision ID: AOA-MEM-D-0050

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-19
- Legacy path: docs/decisions/2026-05-19-functional-agents-route-cards.md
- Surface classes: generated/readout, agents/mesh
- Mechanic parents: none
- Guard families: docs route, mechanic topology, generated/read-model, AGENTS/mesh
- Memory object classes: none
- Posture: active rationale

## Context

The mechanics refactor made `aoa-memo` package topology explicit, but several
human-facing maps still carried executable agent instructions: validation
commands in README-style indexes, migration posture in docs maps, and local
route hints scattered outside the nearest `AGENTS.md`.

That made the repo readable, but it made agent entry uneven. An agent entering
`mechanics/<slug>/`, `docs/`, `parts/`, `legacy/`, or a root technical district
had to infer what was above, what was local, and what lived below.

## Decision

Keep README and index files as human-readable maps. Put operational guidance,
route stacks, validation routes, migration posture, closeout expectations, and
artifact-placement runbooks in the nearest `AGENTS.md`.

Every mechanics package and its `docs/`, `parts/`, and `legacy/` subroutes now
gets a compact Route Stack:

- above: root and parent route cards
- here: the local active contract
- below or adjacent: child surfaces, artifact homes, or provenance lanes

Root technical districts also get Route Stack guidance so agents can quickly
see whether a file belongs in root, in a mechanic package, or in a part-local
home.

## Consequences

- `README.md` and package indexes stay navigable without becoming runbooks.
- `AGENTS.md` becomes the first operational surface for agent behavior in each
  directory.
- Generated AGENTS mesh must be refreshed whenever route-card text changes.
- Historical landing logs and decision records may still name validation that
  was run at landing time; they are evidence, not current runbooks.
- Part `VALIDATION.md` files remain part-local contract surfaces, while
  package and route-wide validation stays discoverable through AGENTS.

## Validation

This decision is validated through:

```bash
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_memo_mechanics.py
python scripts/validate_memo_mechanic_parts.py
python scripts/release_check.py
```
