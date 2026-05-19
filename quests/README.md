# Quest District

This directory holds public memo-facing obligations that should survive the
current diff.

It is not a private scratchpad and not a second roadmap. Program direction
belongs in [ROADMAP](../ROADMAP.md). The root quest index is
[QUESTBOOK](../QUESTBOOK.md). Questbook source law starts in
[QUEST_SOURCE_CONTRACT](../mechanics/questbook/docs/QUEST_SOURCE_CONTRACT.md).

Quest sources live in lane-first lifecycle directories:

```text
quests/<lane>/<state>/<quest-id>
```

## Lanes

| Lane | Use |
|---|---|
| [memo](memo/README.md) | `AOA-MEM-Q-*.yaml` memory-layer obligations and generated quest projections |
| [agon](agon/README.md) | `AOM-Q-AGON-*.md` and `AOMEMO-Q-AGON-*.md` Agon memo follow-through |

## Lifecycle States

| State | Use |
|---|---|
| `captured` | public-safe obligation exists, but route shaping is not complete |
| `triaged` | route-bearing obligation with enough shape to split, promote, or close |
| `ready` | next owner action is clear and bounded |
| `active` | currently being advanced by an owner lane |
| `blocked` | waiting on a named dependency or owner decision |
| `reanchor` | old route no longer matches; choose a new owner, band, or evidence path |
| `done` | landed with enough public evidence to leave the active index |
| `dropped` | intentionally closed without landing, with a visible reason |

## Quest Read-Model Projections

`generated/quest_catalog*.json` and `generated/quest_dispatch*.json` are built
from `AOA-MEM-Q-*.yaml` sources.

Quest read-model projections are compact mirrors. They do not author quest meaning.
Executable projection checks live in [quests/AGENTS](AGENTS.md#validation) and
the Questbook projection part.
