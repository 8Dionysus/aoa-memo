# Lineage Harvest Memo Mechanic

- Decision ID: AOA-MEM-D-0010

## Status

Accepted on 2026-05-18.

## Index Metadata

- Original date: 2026-05-18
- Legacy path: docs/decisions/2026-05-18-lineage-harvest-memo-mechanic.md
- Surface classes: mechanic package
- Mechanic parents: lineage-harvest
- Guard families: mechanic topology
- Memory object classes: none
- Posture: active rationale

## Context

After the recurrence-support landing, `aoa-memo` still had one flat docs-root
surface that was neither core memory doctrine nor route-return support:

- `docs/PATTERN_LINEAGE_MEMORY.md`

The surface names a repeatable operation: cross-repo recurring owner-local
signals become reviewable pattern-lineage memory candidates only when evidence,
owner route, bounded verdict, retention, and authority gates remain visible.

Several nearby homes were plausible but wrong:

- `mechanics/recurrence-support/` owns relaunch anchors, witness traces, and
  reviewed closeout recall landings, not pattern promotion lineage.
- `mechanics/governance/` owns authority-boundary memory for federation
  decisions, not the candidate lineage record itself.
- `mechanics/writeback/` owns return lanes into memory, not the pattern-lineage
  gate.
- `mechanics/retention/` owns retention evidence and outcomes, not the
  harvest candidate.
- `mechanics/adoption/` owns owner-local adoption memory after stronger review,
  not the cross-repo lineage candidate.

Leaving the surface flat would keep one current operation outside the validated
mechanics tree and invite future placement drift.

## Decision

Move `docs/PATTERN_LINEAGE_MEMORY.md` to
`mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md` and add
`mechanics/lineage-harvest/` as an operation-first memo mechanic with package
card, owner map, provenance bridge, landing log, roadmap, docs route, legacy
route, generated mechanics coverage, AGENTS mesh coverage, doctrine recall
coverage, tests, and active path updates.

Keep `mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/schemas/pattern_lineage_memory_entry_v1.json` and
`mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/examples/pattern_lineage_memory_entry.example.json` in root technical
districts while they remain public support contracts and release-gate
companions.

## Consequences

- `mechanics/lineage-harvest/README.md` becomes the active mechanic card.
- The old flat path is historical provenance only, allowed in
  `config/memo_mechanics.json`, `mechanics/lineage-harvest/legacy/INDEX.md`,
  and decision records.
- Active references now point to
  `mechanics/lineage-harvest/docs/PATTERN_LINEAGE_MEMORY.md`.
- Generated `memo_mechanics`, `agents_mesh`, memo registry, and doctrine recall
  surfaces must stay aligned.
- Stronger owners keep stronger claims: `Agents-of-Abyss` for federation
  harvest program law, source repositories for consent and source truth,
  `aoa-evals` for proof, `aoa-stats` for summaries, `aoa-kag` for graph
  promotion intake, `Tree-of-Sophia` for authored meaning and canon,
  `aoa-routing` for dispatch, `aoa-agents` for rights and assistant adoption
  posture, `aoa-playbooks` for adoption choreography, and `abyss-stack` for
  runtime watchtower execution.

## Verification

Expected verification:

- `python scripts/validate_memo_mechanics.py`
- `python scripts/build_memo_mechanics_index.py --check`
- `python scripts/validate_memo_mechanics_index.py`
- `python scripts/validate_agents_mesh.py`
- `python scripts/build_agents_mesh_index.py --check`
- `python scripts/validate_agents_mesh_index.py`
- `python scripts/validate_memory_surfaces.py`
- `python scripts/validate_memo.py`
- `python -m pytest -q mechanics/lineage-harvest/parts/pattern-lineage-memory-gate/tests/test_lineage_harvest_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py mechanics/recurrence-support/parts/witness-trace-contract/tests/test_recurrence_support_mechanic.py tests/test_cross_mechanic_candidate_contracts.py`
- `python scripts/release_check.py`
