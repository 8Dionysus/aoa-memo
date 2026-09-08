---
name: aoa-memo
description: "AoA/Abyss durable memory and owner orientation: use when ongoing work may depend on reviewed prior decisions, provenance, lifecycle/currentness, or an existing memo artifact, even when none is named. Also use to recall, review, or evolve a candidate, export, quarantine packet, object, corpus identity, lifecycle target, or read model. Use aoa-memo-writeback only before any memo artifact exists. Do not use for raw-session retrieval, proof, routing authority, roles, workflows, KAG substrate, runtime storage, or generic notes."
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

1. Read this `SKILL.md` completely and record `<bundle_dir>` as its
   absolute containing directory. Choose this family from the request: an
   existing memo artifact belongs here; first writeback without an artifact
   belongs to `aoa-memo-writeback`. Do not load both families speculatively.
   Before using an owner-dependent claim or taking an effect, require the
   selected package, source identity, relevant current evidence, and authority
   conditions below to be established. Tool-turn count is not a gate.
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
2. Call `aoa_memo_recall_brief(repo, intent)` exactly once through the current
   admitted `aoa_memo` MCP read contour. The brief is a locator, never
   authority.
3. If the brief exposes no material reviewed hit, or current owner source
   already settles the question, choose `silence` and continue the task from
   current source. Do not announce memory merely because the tool ran.
4. Use `aoa_memo_recall_reviewed(query, mode, limit)` at most once, with a
   bounded lexical query. This primitive is fixed to the reviewed-corpus
   contour; use it only when one specific earlier decision or lesson could
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

1. Read `references/contract.yaml` completely and choose exactly one mode
   from the requested operation:

   | Mode | Select when | Read |
   | --- | --- | --- |
   | `recall` | Existing owner memory or a recall projection must be interpreted, compared, or diagnosed. | `references/recall.md` |
   | `review` | A concrete candidate, export, quarantine packet, contradiction, or lifecycle target needs a disposition. | `references/review.md` |
   | `evolve` | The request asks to create, land, change, consolidate, supersede, retract, withdraw, quarantine, or rebuild an owner memory/corpus/lifecycle/contract/read-model source, even when a required gate may later block the operation. | `references/evolve.md` |

   Select by the requested operation, not by whether its gates already pass.
   Missing review, evidence, ownership, authority, or confirmation blocks
   `evolve`; it does not turn a requested owner change into `review`.
2. Read `references/source-return.md` and the selected mode reference
   completely. Independent package reads may share a tool call once the paths
   and selected mode are known. Do not preload other modes.
3. Establish the source-return conditions before interpreting owner-relative
   evidence, then follow the selected procedure and return the common ABI.
   A missing or mismatched source blocks the dependent claim or effect; it
   does not become valid through extra reads.

Reuse already available complete reads only while their source identity,
version and relevant content remain applicable. Re-read when the source or
artifact changes, required context is no longer available, or a new material
fact is needed. Batch independent reads; preserve dependencies that determine
which source, mode, target or effect is admissible. A previous read or install
receipt is not evidence that a changed source is current.

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
  Existing authorization applies to the same effect, target and scope; do
  not ask for it again. It does not replace origin-owner acceptance, reviewed
  intake, or a distinct confirmation required for an exact landing plan.

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
