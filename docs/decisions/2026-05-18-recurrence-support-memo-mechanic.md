# Recurrence Support Memo Mechanic

## Status

Accepted on 2026-05-18.

## Context

`aoa-memo` still had three flat docs-root surfaces that looked like recurrence
support but were not core memory doctrine:

- `docs/RECURRENCE_MEMORY_SUPPORT_SURFACES.md`
- `docs/WITNESS_TRACE_CONTRACT.md`
- `docs/REVIEWED_CLOSEOUT_RECALL_LANDING.md`

They share one operation: preserve enough reviewable memory for a route to
return. They do not define memory-object canon, proof, routing behavior,
runtime retry policy, role rights, or playbook choreography.

Leaving them flat made them look like general doctrine peers. Moving them into
writeback would blur route-return support with owner return lanes. Moving
`PATTERN_LINEAGE_MEMORY.md` with them would blur recurrence support with a
separate federation harvest and lineage-promotion operation.

## Decision

Move the three recurrence-support surfaces into
`mechanics/recurrence-support/docs/` and make `mechanics/recurrence-support/`
an operation-first memo mechanic with package card, owner map, provenance
bridge, landing log, roadmap, docs route, legacy route, generated mechanics
coverage, AGENTS mesh coverage, tests, and active path updates.

Keep witness trace, inquiry checkpoint, recall contract, checkpoint-to-memory,
quest, and generated artifacts in root technical districts while they remain
public support contracts and release-gate companions.

Keep `docs/PATTERN_LINEAGE_MEMORY.md` flat for now. It is a candidate for a
separate lineage or federation harvest mechanic, not part of this route-return
support operation.

## Consequences

- `mechanics/recurrence-support/README.md` becomes the active mechanic card.
- Old flat paths are historical provenance only, allowed in
  `config/memo_mechanics.json`, `mechanics/recurrence-support/legacy/INDEX.md`,
  and decision records.
- Active references now point to
  `mechanics/recurrence-support/docs/*.md`.
- Generated `memo_mechanics`, `agents_mesh`, memo registry, doctrine recall
  surfaces, quest catalog, and runtime writeback companions must stay aligned.
- Stronger owners keep stronger claims: `Agents-of-Abyss` for recurrence
  doctrine, `aoa-routing` for dispatch, `abyss-stack` for runtime retry,
  `aoa-agents` for rights, `aoa-playbooks` for scenario return, and
  `aoa-evals` for proof.

## Verification

Expected verification:

- `python scripts/validate_memo_mechanics.py`
- `python scripts/build_memo_mechanics_index.py --check`
- `python scripts/validate_memo_mechanics_index.py`
- `python scripts/validate_agents_mesh.py`
- `python scripts/build_agents_mesh_index.py --check`
- `python scripts/validate_agents_mesh_index.py`
- `python scripts/validate_memo.py`
- `python scripts/release_check.py`
