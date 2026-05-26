# AGENTS Authority Boundary Audit

- Decision ID: AOA-MEM-D-0044

## Status

Accepted on 2026-05-19.

## Index Metadata

- Original date: 2026-05-19
- Legacy path: docs/decisions/2026-05-19-agents-authority-boundary-audit.md
- Surface classes: agents/mesh, boundary/runtime/sibling
- Mechanic parents: none
- Guard families: docs route, AGENTS/mesh, sibling and boundary
- Memory object classes: audit_event
- Posture: active rationale

## Context

After the root semantic topology landed, every active district had a nearest
`AGENTS.md`, and the source-backed AGENTS mesh covered all current route
cards. The next risk was quieter: neighboring root documents could still carry
agent-owned route modes or executable runbooks, making future agents choose
between a route card and an adjacent overview.

The audit also found route-card-local drift: legacy mechanic cards still
named old flat root script paths after the script topology moved into
`scripts/mechanics/` and `scripts/release/`.

This matters because `AGENTS.md` is the active operational route surface.
README, CHARTER, DESIGN, and mechanic-doc map surfaces should orient,
authorize, or describe form. They should not become shadow route cards or
stale topology maps.

## Decision

Keep active agent route law and executable validation routes in root
`AGENTS.md` and the nearest nested `AGENTS.md`.

Neighboring root documents may point to those route cards, but they must not
duplicate AGENTS-owned route modes or executable validation command blocks.
Mechanic docs maps may point to nearby AGENTS cards and part-local artifact
homes, but they must not preserve old flat artifact paths after topology moves.

Add `neighbor_doc_boundaries` to `config/agents/agents_mesh.json` and teach
`scripts/agents/validate_agents_mesh.py` to fail when audited root neighbors
reintroduce AGENTS-owned guidance.

Teach the same validator to reject stale flat root script commands in any
`AGENTS.md`, so route cards keep pointing at the current semantic script
districts.

## Consequences

- `README.md` remains a public front door and does not carry root route-mode
  law.
- `CHARTER.md` names authority and change health, while operational editing
  order stays in AGENTS.
- `DESIGN.AGENTS.md` describes agent-surface form and validation intent, while
  executable commands stay in route cards.
- `mechanics/agon/docs/README.md` names part-local companion homes instead of
  retired flat artifact paths.
- `mechanics/titan/docs/TITAN_MEMORY_POSTURE.md` keeps its domain closeout
  receipt wording distinct from route-card closeout instructions.
- Legacy mechanic route cards point at `scripts/mechanics/` and
  `scripts/release/`, not the retired flat root script paths.
- Future route-card audits have a machine-checkable boundary instead of only a
  prose convention.

## Verification

Use:

```bash
python scripts/agents/validate_agents_mesh.py
python scripts/agents/build_agents_mesh_index.py --check
python scripts/agents/validate_agents_mesh_index.py
python -m pytest -q tests/agents
python scripts/release/release_check.py
```
