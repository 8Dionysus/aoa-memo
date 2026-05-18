# Quest Chronicle Writeback

## Purpose

This note defines the first chronicle-shaped RPG reflection surface for `aoa-memo`.

It exists so that reviewed questlines and progression evidence can leave a recallable witness without turning memory into a second quest authority.

## Core rule

A quest chronicle is a witness object.

It may preserve:
- a bounded lane summary
- stage witness notes
- participating agent refs
- linked progression evidence refs
- a recall anchor and next recall cue
- temperature posture

It must not:
- replace source-owned quest state
- replace source-owned campaign or playbook meaning
- become a player sheet or runtime inventory
- hide unresolved contradictions as settled memory

## Good first-wave chronicle posture

Use a chronicle when:

- a questline or campaign lane has enough shape to remember
- the memory will help future recall, distillation, or archivist handoff
- provenance and anchor refs can stay explicit
- the chronicle can remain compact

## Temperature posture

Recommended first-wave posture:

- `warm` for short-horizon campaign witness
- `cool` for stable summaries that may matter later
- `cold` only for later audit or delayed recall
- avoid `hot` unless tied to an active checkpoint
- reserve `frozen` for reviewed settled evidence

## Stage witness posture

A stage witness should answer:

- what stage was observed
- what anchor mattered
- what changed or was confirmed
- what future recall cue is worth preserving

## Upstream refs

Example chronicles may cite upstream read-only refs such as `AOA-SK-Q-0003` or `AOA-EV-Q-0005`.
Those refs stay source-owned upstream and do not widen this rollout into `aoa-skills` or `aoa-evals`.

## Anti-patterns

- copying the live quest as if it were memo truth
- using chronicle notes as a hidden project backlog
- storing decorative RPG inventory state
- preserving every transient event as if it deserved durable recall
