# AGENTS.md

## Applies To

This card applies to `mechanics/questbook/` and every nested path until a
nearer `AGENTS.md` narrows the lane.

## Role

Questbook owns memo-side public obligation mechanics: root `QUESTBOOK.md`,
the lane-first `quests/` item store, source contracts, lifecycle placement,
generated quest projections, and owner-routing stop-lines.

It does not own source quest state, playbook choreography, proof outcomes,
runtime scheduling, role rights, or hidden memory.

## Route Stack

- Above: root `AGENTS.md` owns repo identity and release route;
  `mechanics/AGENTS.md` owns shared mechanic package law and validators.
- Here: `README.md` is the mechanic card, `DIRECTION.md` names current
  pressure, `PARTS.md` lists active function nodes, `OWNER_MAP.md` names
  stronger owners, and `PROVENANCE.md` plus `legacy/` preserve placement
  history.
- Below: `docs/` holds active source docs, `parts/` holds functioning
  contracts and artifact homes, and `legacy/` is historical evidence only.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, `PROVENANCE.md`,
`parts/README.md`, `docs/QUEST_SOURCE_CONTRACT.md`, `QUESTBOOK.md`, and
`quests/README.md`.

For Agon quest follow-through, also read `mechanics/agon/AGENTS.md` and the
matching `mechanics/agon/docs/AGON_*.md` surface.

## Boundaries

- Root `QUESTBOOK.md` is a compact public index, not a second roadmap.
- Root `quests/` is the public lane-first item store, not a package-local
  artifact directory and not private scratch work.
- Generated quest catalog and dispatch files are root-published read models
  from quest source files; rebuild them rather than editing by hand. Their
  part contract is `parts/quest-read-model-projections/`.
- Do not turn memo quest records into proof, route dispatch, playbook
  scenario state, runtime retention, role authority, or source-owner
  acceptance.

## Post-Change Review

Before closeout, review the changed route rather than only the changed file:

- Quest source changed: check lane, lifecycle state, owner route, source
  contract, generated projections, and public-safety posture.
- Questbook law changed: check `README.md`, `PARTS.md`, `OWNER_MAP.md`,
  `PROVENANCE.md`, `LANDING_LOG.md`, `ROADMAP.md`, `docs/`, and decisions.
- Generated projections changed: rebuild with the package builder, run the
  generated checks, and check `parts/quest-read-model-projections/`.
- Root quest route changed: update `QUESTBOOK.md`, `quests/AGENTS.md`, and
  `quests/README.md` only when their future-facing route changed.

## Validation

```bash
python mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py
python mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py --check
python scripts/memory/validate_memo.py
python -m pytest -q mechanics/questbook/parts/source-contract/tests tests/memory/test_memo_questbook_boundaries.py
```

Before landing, also run:

```bash
python scripts/release/release_check.py
```

## Closeout

Report changed quest lanes, lifecycle states, generated projections rebuilt or
not rebuilt, owner boundaries affected, checks run, skipped checks, and the
next owner route when a quest is only carrying another repository's work.
