# Quest Source Contract

This surface owns the memo-side reviewability contract for quest sources.

## Root Index

`QUESTBOOK.md` is a compact public index for open memo-facing obligations. It
must not become a second roadmap, release log, proof ledger, hidden memory, or
private task dump.

## Source Store

Quest source files live under lane-first lifecycle directories:

```text
quests/<lane>/<state>/<quest-id>.yaml
quests/<lane>/<state>/<quest-id>.md
```

Current lanes:

- `memo` for `AOA-MEM-Q-*.yaml` memory-layer obligations
- `agon` for `AOM-Q-AGON-*.md` and `AOMEMO-Q-AGON-*.md` Agon memo
  follow-through

Current lifecycle states follow the shared Questbook vocabulary:
`captured`, `triaged`, `ready`, `active`, `blocked`, `reanchor`, `done`, and
`dropped`.

## YAML Contract

`AOA-MEM-Q-*.yaml` sources use the existing `work_quest_v1` schema. Their
`state` field must match the lifecycle directory. Generated quest catalog and
dispatch projections use these YAML sources.

## Markdown Contract

Agon follow-through Markdown sources use:

```text
source_contract: memo_quest_markdown_contract_v1
```

They must contain:

- `## Quest`
- `## Owner Route`
- `## Next Action`
- `## Acceptance Evidence`
- `## Stop-lines`

Markdown quest sources may route to Agon memo docs, but they must not claim an
Agon verdict, durable scar, rank mutation, retention execution, KAG promotion,
Sophian canon write, proof, route dispatch, role authority, or runtime state.

## Generated Projections

Generated quest surfaces are compact root-published read models:

- `generated/quest_catalog.min.json`
- `generated/quest_dispatch.min.json`
- `generated/quest_catalog.min.example.json`
- `generated/quest_dispatch.min.example.json`

Rebuild them with:

```bash
python mechanics/questbook/parts/generated-views/scripts/build_quest_surfaces.py
```

Do not hand-edit generated quest surfaces.

The placement contract lives in
[`parts/generated-views`](../parts/generated-views/README.md): the Questbook
mechanic owns the builder, validation, and stop-lines, while root `generated/`
publishes the compact read models for outside consumers.
