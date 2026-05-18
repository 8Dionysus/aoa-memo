# Questbook Legacy Index

| Former surface | Active route | Note |
|---|---|---|
| `quests/AOA-MEM-Q-*.yaml` | `quests/memo/<state>/AOA-MEM-Q-*.yaml` | memo quest sources now use lane-first lifecycle placement |
| `quests/AOM-Q-AGON-*.md` | `quests/agon/ready/AOM-Q-AGON-*.md` | Agon follow-through remains in root quest item store, not package-local docs |
| `quests/AOMEMO-Q-AGON-*.md` | `quests/agon/ready/AOMEMO-Q-AGON-*.md` | Agon memo follow-through now carries the Markdown quest source contract |
| `scripts/build_quest_surfaces.py` | `mechanics/questbook/scripts/build_quest_surfaces.py` | generated quest projection builder belongs to Questbook mechanic |
| none | `mechanics/questbook/docs/QUEST_SOURCE_CONTRACT.md` | active source contract for memo quest sources |
