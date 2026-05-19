# Questbook Parts

## Active Parts

| Part | Source Surface | Contract |
|---|---|---|
| Obligation index | [QUESTBOOK](../../QUESTBOOK.md) | compact list of open memo-facing obligations; not a second roadmap |
| Quest item store | [quests](../../quests/README.md) | lane-first lifecycle source files under `quests/<lane>/<state>/` |
| Source contract | [QUEST_SOURCE_CONTRACT](docs/QUEST_SOURCE_CONTRACT.md), [validate_quest_store](parts/source-contract/scripts/validate_quest_store.py) | reviewable YAML and Markdown source shape for memo quest objects |
| Quest read-model projections | [quest-read-model-projections part](parts/quest-read-model-projections/README.md), [build_quest_surfaces](parts/quest-read-model-projections/scripts/build_quest_surfaces.py), [generated quest catalog](../../generated/quest_catalog.min.json), [generated quest dispatch](../../generated/quest_dispatch.min.json) | root-published read models that never author quest meaning |

## Part-Local Artifacts

| Part | Artifact Surface |
|---|---|
| Source contract | `mechanics/questbook/parts/source-contract/scripts/validate_quest_store.py`, `mechanics/questbook/parts/source-contract/tests/test_questbook_store.py` |
| Quest read-model projections | `mechanics/questbook/parts/quest-read-model-projections/scripts/build_quest_surfaces.py` |

## Interface

Inputs are public-safe memo obligations, owner-routed follow-through notes, and
source refs. Outputs are source quest files, generated projections, and
bounded next actions.
