# Questbook Parts

## Active Parts

| Part | Source Surface | Contract |
|---|---|---|
| Public index | [QUESTBOOK](../../QUESTBOOK.md) | compact list of open memo-facing obligations; not a second roadmap |
| Quest item store | [quests](../../quests/README.md) | lane-first lifecycle source files under `quests/<lane>/<state>/` |
| Source contract | [QUEST_SOURCE_CONTRACT](docs/QUEST_SOURCE_CONTRACT.md) | reviewable YAML and Markdown source shape for memo quest objects |
| Generated projections | [build_quest_surfaces](./scripts/build_quest_surfaces.py), [generated quest catalog](../../generated/quest_catalog.min.json), [generated quest dispatch](../../generated/quest_dispatch.min.json) | compact mirrors that never author quest meaning |

## Interface

Inputs are public-safe memo obligations, owner-routed follow-through notes, and
source refs. Outputs are source quest files, generated projections, and
bounded next actions.
