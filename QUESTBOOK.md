# QUESTBOOK.md — aoa-memo

This questbook tracks memory-layer obligations related to quest evidence and writeback boundaries.

It is a compact public index. Source quest files live in lane-first lifecycle
directories under [`quests/`](quests/), and Questbook law lives in
[`mechanics/questbook`](mechanics/questbook/README.md).

## Update Trigger

Update this root index when public memory-layer obligation state changes, a
quest lane/source file moves, or Questbook generated projections change their
published route. Do not use it as a second roadmap, release note, or hidden
quest ledger.

## Frontier

- `AOA-MEM-Q-0003` - define a quest chronicle writeback surface for campaign witness and progression evidence
- `AOA-MEM-Q-0004` - align router orchestrator quests to inspect-first and capsule-second memo recall
- `AOA-MEM-Q-0005` - align review orchestrator quests to closure, residual-risk, and recurrence memo notes
- `AOA-MEM-Q-0006` - align bounded-execution orchestrator quests to step-local recall and handoff continuity
- `AOA-MEM-Q-0012` - land the first object-population wave across stable object slots
- `AOA-MEM-Q-0013` - apply the first real lifecycle pressure transition on reviewed corpus
- `AOA-MEM-Q-0014` - hand off the first full memo-quality lens pack to `aoa-evals`

## Blocked / reanchor

- `AOA-MEM-Q-0008` - reanchor checkpoint automation recall as a thin-evidence memo candidate
- `AOA-MEM-Q-0009` - reanchor Agents-of-Abyss v0.4.0 recall as a thin-evidence memo candidate

## Harvest candidates

- `AOA-MEM-Q-0008` - reanchor checkpoint automation recall as a thin-evidence memo candidate
- `AOA-MEM-Q-0009` - reanchor Agents-of-Abyss v0.4.0 recall as a thin-evidence memo candidate

## Quest-harvest posture

`aoa-quest-harvest` may be installed at `.agents/skills/aoa-quest-harvest` as a post-session aid for memo-facing recall and writeback triage.

- use it only after a reviewed run, closure, or pause
- do not use it inside an active route
- it does not define orchestrator identity
- it does not replace playbook, memo, eval, or source-owned doctrine
- do not promote on one anecdotal repeat

Allowed verdicts:

- `keep/open quest`
- `promote to skill`
- `promote to playbook`
- `promote to orchestrator surface`
- `promote to proof surface`
- `promote to memo surface`

Generated quest summaries stay builder-backed and validator-checked so root
generated files remain projections instead of a second quest ledger.

## Backing files

- `quests/memo/<state>/AOA-MEM-Q-*.yaml`
- `quests/agon/<state>/AOM-Q-AGON-*.md`
- `quests/agon/<state>/AOMEMO-Q-AGON-*.md`
- `generated/quests/quest_catalog.min.json`
- `generated/quests/quest_dispatch.min.json`
- `generated/quests/quest_catalog.min.example.json`
- `generated/quests/quest_dispatch.min.example.json`

## Rule

Root `QUESTBOOK.md` stays an index. The `quests/` district owns item files,
`mechanics/questbook/` owns source contract and validation, and generated
quest surfaces remain projections.
