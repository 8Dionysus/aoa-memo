---
name: aoa-memo
description: "AoA/Abyss durable memory and owner orientation: use when ongoing work may depend on reviewed prior decisions, provenance, lifecycle/currentness, or an existing memo artifact, even when none is named. Also use to recall, review, or evolve a candidate, export, quarantine packet, object, corpus identity, lifecycle target, or read model. First tool turn reads only this SKILL.md. Use aoa-memo-writeback only before any memo artifact exists. Do not use for raw-session retrieval, proof, routing authority, roles, workflows, KAG substrate, runtime storage, or generic notes."
---

# aoa-memo

Give ordinary AoA/Abyss work one cheap chance to notice relevant reviewed
memory, then deepen only when a concrete memory question survives current
owner-source verification. Never turn memory into proof, current source truth,
route authority, role permission, runtime state, or hidden prompt residue.

## Applicability preflight

Inspect only the request before resolving the owner:

- use the fast orientation lane when the task continues, resumes, or crosses
  owner surfaces and a reviewed prior decision, durable lesson, provenance
  constraint, or lifecycle fact could materially change where or how to work,
  even when the request names no memory artifact
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

## Start and choose one speed

1. The first tool turn after selection must read only this `SKILL.md`. Record
   `<bundle_dir>` as its absolute containing directory. If task-workspace
   inspection, search, or another skill body was combined with that read,
   return
   `blocked_package_gate_not_observed` immediately. Do not read the contract,
   source-return rule, target, owner, or evidence in that invocation.
   Restart only through a new invocation; later compliance cannot repair the
   unobserved package gate.
   When a concrete memo artifact was already named, loading
   `aoa-memo-writeback` first is `blocked_selection_gate_not_observed`; stop
   rather than continuing with both bundles.
2. Run the applicability preflight. Stop on a handoff or negative result.
3. Choose exactly one speed:

   | Speed | Select when | First action |
   | --- | --- | --- |
   | `orient` | Ordinary AoA/Abyss work may benefit from prior reviewed context, but no exact memo artifact or lifecycle operation is yet material. | Follow **Fast orientation** below. |
   | `deep` | A concrete artifact, owner-memory claim, contradiction, lifecycle target, read-model drift, review, or source evolution is already material. | Follow **Deep owner route** below. |

Do not run both speeds speculatively. `orient` may escalate to `deep` only
after a bounded access-plane hit proves that exact owner memory is material.

## Fast orientation

This is the normal participation path for persistent Codex sessions. It is
read-only, deterministic, and optional: correct silence is a successful
result.

1. Resolve only the current repository label and a one-sentence intent from
   already available request/cwd context. Do not inspect the workspace to
   manufacture an intent.
2. Call `aoa_memo_brief(repo, intent)` exactly once through the existing
   `aoa_memo` MCP read contour. The brief is a locator, never authority.
3. If the brief exposes no material reviewed hit, or current owner source
   already settles the question, choose `silence` and continue the task from
   current source. Do not announce memory merely because the tool ran.
4. Use `aoa_memo_search` at most once, with reviewed scope and a bounded
   lexical query, only when one specific earlier decision or lesson could
   change the owner route and the brief did not identify it exactly. Never
   search by broad curiosity.
5. Before memory changes an answer or action, verify the exact current source
   route named by the hit. Historical memory may explain a path; current owner
   source decides what is true now.
6. If interpreting the memory object's meaning, provenance, temporal posture,
   contradiction, lifecycle, or projection is material, escalate to `deep`
   `recall`. Otherwise stop this skill after one route-oriented observation or
   silence.

The fast lane performs no model call, prompt injection, writeback, candidate
creation, policy promotion, or external effect. It does not depend on
`aoa-session-memory`; a session-evidence packet may be consumed by ref when
already supplied, but raw-session discovery remains a sibling handoff.

## Deep owner route

1. In one tool turn containing no other read or command, read
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
2. In the next tool turn, read only `references/source-return.md` to EOF and
   await the result.
3. In a later tool turn, read only the selected mode reference to EOF and await
   the result. Do not preload another mode or combine these three package reads.
   Any target, origin-port, evidence, owner-checkout, workspace, or other-skill
   read before all three results is terminal
   `blocked_package_gate_not_observed`.
4. Execute the source-return gate before any owner-relative read, then follow
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
- `orient`, `recall`, and `review` are read-only. `evolve` may change owner
  source only with an accepted review, explicit authority, and the
  repository's normal confirmation route.

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

Stop after one silence or route-oriented observation, bounded recall, review
disposition, authorized source-first change, no-change result, owner handoff,
or explicit blocker. Preserve `missing`, `unknown`, `stale`, `historical`,
`superseded`, `retracted`, `quarantined`, and `current` as distinct states.

Keep raw trials, task-local DAGs, candidate scaffolds, runtime state, temporary
rubrics, and session notes outside the owner package.
