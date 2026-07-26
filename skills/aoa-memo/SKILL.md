---
name: aoa-memo
description: "Use aoa-memo to recall, review, or evolve an existing memo candidate, export, quarantine packet, memory object, corpus identity, lifecycle target, or read model. Use aoa-memo-writeback only before any memo artifact exists. Do not use for raw-session retrieval, proof, routing, roles, workflows, KAG substrate, runtime storage, or generic notes."
---

# aoa-memo

Route one explicit memory question through its canonical owner without turning
memory into proof, current source truth, route authority, role permission,
runtime state, or hidden prompt residue.

## Applicability preflight

Inspect only the request before resolving the owner:

- if no concrete memo artifact exists and the task is to notice a reusable
  lesson or create the first candidate from live-session, closeout, landed
  work, PR, diff, or review evidence, return `owner_handoff` to
  `aoa-memo-writeback`
- if the request names or supplies a concrete candidate, export, quarantine
  packet, object, corpus identity, lifecycle target, or memory read-model
  target, this bundle is the direct route; do not inspect or load
  `aoa-memo-writeback`
- if the task needs raw `.aoa` session lookup, transcript retrieval, or
  rehydration, return `owner_handoff` to the session-memory route
- do not deflect a genuine question about existing owner memory, provenance,
  currentness, lifecycle, contradiction, or read-model drift merely because no
  exact file path was supplied
- return `not_applicable` for proof, routing, roles, workflows, KAG substrate,
  runtime retention or repair, generic note taking, or an already named
  validator invocation

On either preflight handoff, do not resolve the `aoa-memo` owner, inspect the
corpus, enumerate candidates, or create an artifact.

## Start

1. The first tool turn after selection must read only this `SKILL.md`. Record
   `<bundle_dir>` as its absolute containing directory. If task-workspace
   inspection, search, or another skill body was combined with that read or
   occurred before the package references below were loaded, return
   `blocked_package_gate_not_observed` immediately. Do not read the contract,
   source-return rule, mode, target, owner, or evidence in that invocation.
   Restart only through a new invocation; later compliance cannot repair the
   unobserved package gate.
   When a concrete memo artifact was already named, loading
   `aoa-memo-writeback` first is `blocked_selection_gate_not_observed`; stop
   rather than continuing with both bundles.
2. Run the applicability preflight. Stop on a handoff or negative result.
3. In one tool turn containing no other read or command, read
   `references/contract.yaml` to EOF and await the result. Then choose exactly
   one mode from the requested operation:

   | Mode | Select when | Read |
   | --- | --- | --- |
   | `recall` | Existing owner memory or a recall projection must be interpreted, compared, or diagnosed. | `references/recall.md` |
   | `review` | A concrete candidate, export, quarantine packet, contradiction, or lifecycle target needs a disposition. | `references/review.md` |
   | `evolve` | The request asks to create, land, change, consolidate, supersede, retract, withdraw, quarantine, or rebuild an owner memory/corpus/lifecycle/contract/read-model source, even when a required gate may later block the operation. | `references/evolve.md` |

   Select by the requested operation, not by whether its gates already pass.
   Missing review, evidence, ownership, authority, or confirmation blocks
   `evolve`; it does not turn a requested owner change into `review`.
4. In the next tool turn, read only `references/source-return.md` to EOF and
   await the result.
5. In a later tool turn, read only the selected mode reference to EOF and await
   the result. Do not preload another mode or combine these three package reads.
   Any target, origin-port, evidence, owner-checkout, workspace, or other-skill
   read before all three results is terminal
   `blocked_package_gate_not_observed`.
6. Execute the source-return gate before any owner-relative read, then follow
   the selected procedure and return the common ABI.

Keep the modes internal until held-out manual work proves that separate
prompt-visible skills improve triggers, contracts, composition, and outcomes.

## Owner and authority boundary

- `aoa-memo` owns reviewed memory-object shape, provenance, temporal and recall
  posture, lifecycle, corpus intake, and its generated memory models.
- Origin owners retain source meaning and candidate acceptance. `.aoa` retains
  raw session evidence. `aoa-evals` retains proof. MCP and KAG remain access or
  retrieval layers.
- A candidate, schema-valid packet, green validator, generated reader, MCP
  result, or KAG node cannot establish durable owner acceptance.
- `recall` and `review` are read-only. `evolve` may change owner source only
  with an accepted review, explicit authority, and the repository's normal
  confirmation route.

## Task-local composition

Build only the edges needed by the selected question:

```text
source owner or captured evidence
  -> local candidate, receipt, or export
  -> origin-owner plus aoa-memo review
  -> reviewed corpus source
  -> generated read model
  -> MCP, KAG, or bounded consumer
```

A later node cannot repair or strengthen an earlier source, review, or
provenance gap. When session-memory already returned an evidence packet, begin
at those refs and do not search the session archive again.

## Stop

Stop after one bounded recall, review disposition, authorized source-first
change, no-change result, owner handoff, or explicit blocker. Preserve
`missing`, `unknown`, `stale`, `historical`, `superseded`, `retracted`,
`quarantined`, and `current` as distinct states.

Keep raw trials, task-local DAGs, candidate scaffolds, runtime state, temporary
rubrics, and session notes outside the owner package.
