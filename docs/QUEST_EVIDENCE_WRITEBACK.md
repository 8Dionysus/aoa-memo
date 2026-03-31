# QUEST EVIDENCE WRITEBACK

This note is anchored to [WRITEBACK_TEMPERATURE_POLICY](WRITEBACK_TEMPERATURE_POLICY.md).
It defines how `aoa-memo` remembers quest evidence without taking ownership of the quest itself.

The quest state remains source-owned. `aoa-memo` keeps the recallable witness of that state.

## Boundary

- source repos own quest state, acceptance, and next action
- `aoa-memo` owns the evidence trail, recall posture, and writeback boundary
- we never reclassify a source quest as memo truth just because it was recorded here

## Good writeback candidates

- reviewed witness traces that explain what was observed
- compact evidence summaries that preserve provenance
- temperature-labeled route notes that explain why a memory survived
- handoff notes for an archivist or follow-up pass

## Bad writeback candidates

- raw scratch notes that never got reviewed
- source-owned quest state copied as if it were memo truth
- unresolved contradictions presented as settled memory
- transient tooling output with no recall value
- example trace payloads that are not ready for this pass

## Temperature posture

- `hot`: only preserve when needed for an explicit checkpoint
- `warm`: strongest zone for quest evidence with short-horizon reuse
- `cool`: good for compact summaries that may be reused later
- `cold`: keep for audit and delayed recall, not default recall
- `frozen`: only after review and when the evidence has settled

## Witness trace posture

- use witness traces to record what happened, not to replace the source quest
- keep them redaction-first and provenance-aware
- write them back only when they help future recall or archivist handoff
- `AOA-MEM-Q-0002` is tracked here as the later compact example, but the example file is intentionally absent in this pass

## Archivist handoff

- hand off when evidence can be recalled without consulting the live route
- keep the source repo link visible
- if the memory cannot be described without taking over source state, keep it source-owned
- memo should preserve evidence, not become the quest owner
