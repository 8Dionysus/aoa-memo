# Decision: Distributed erasure requires walkable owner closure

- Decision ID: AOA-MEM-D-0080

## Status

Accepted on 2026-07-29 for source-local Phase 11 contracts and synthetic
failure-injection evaluation. Live private-data deletion, deployment, and
landing remain deferred.

## Index Metadata

- Original date: 2026-07-29
- Surface classes: lifecycle/retention, boundary/runtime/sibling
- Mechanic parents: retention
- Guard families: lifecycle/retention, memory surface, sibling and boundary
- Memory object classes: decision, audit_event
- Posture: active distributed-erasure rationale

## Context

The immutable active-organ v1 ABI already defines C14 erase requests, C15
distributed manifests, C16 per-owner work items, and C17 completion-or-residue
receipts. Those contracts prevent a local delete from becoming a global
completion claim, but Phase 11 must additionally prove that every material
surface is walkable, every owner returns evidence, recovery probes are
themselves privacy-safe, and rebuild or race paths cannot resurrect material.

A generic delete flag cannot distinguish canonical memory, raw session
evidence, local ports, lexical and dense indexes, graphs, runtime stores,
backups, host-local paths, replay corpora, training descendants, and the
minimal audit tombstone. It also cannot distinguish successful absence from a
broken recovery probe.

## Decision

Keep C14-C17 immutable and add a source-local closure validator plus
content-minimized recovery-probe contract.

A Phase 11 request must name ER0-ER9. A complete manifest must contain one
surface-scoped C16/C17 chain for every id:

- ER0 canonical object, summaries, and Markdown/read models;
- ER1 operator-authorized raw session evidence;
- ER2 local memo ports and lexical postings;
- ER3 embeddings, graph nodes and edges, and KAG projections;
- ER4 runtime stores, caches, and nervous indexes;
- ER5 exports, backups, and restore descendants;
- ER6 `abyss-machine` host-local surfaces;
- ER7 experiment and replay copies;
- ER8 training datasets plus checkpoints or a model-unlearning obligation;
- ER9 one content-minimized audit tombstone.

The surface-scoped worker identity does not replace its parent owner. Every
owner extension pins both. This keeps C15 walkable without pretending that one
aggregate owner receipt proves hidden child work.

Recovery proof requires a synthetic positive control detected before erasure
and a negative probe after erasure. Exact, lexical, dense, graph, and
paraphrase routes are checked where applicable. The probe stores only digests,
counts, classes, and refs; it cannot retain the subject material. Required
race/rebuild probes must show that deleted descendants were not recreated.

`complete` requires all ten surfaces erased, every required recovery probe
passed, no residue, and no retention exception. Approved exceptions may yield
only `complete_with_approved_exceptions`, never plain completion. Pending,
partial, failed, unwalkable, or unprobed work blocks the corresponding private
memory deployment class.

Raw `.aoa` evidence may be erased only through an explicit operator/privacy
decision and the `aoa-session-memory` owner contract. Ordinary cleanup remains
forbidden. Model unlearning remains the training/model owner's obligation; a
missing owner receipt is residue, not deletion.

`aoa-memo` owns request, manifest, closure meaning, and minimal tombstone
semantics. `abyss-stack` owns runtime and backup purge evidence.
`abyss-machine` owns host-path and physical evidence. `aoa-session-memory`
owns raw and local-port evidence. `aoa-kag` owns projection purge evidence.
`aoa-evals` owns recovery and adversarial verdicts. Training/model owners own
dataset, checkpoint, and unlearning evidence.

This decision authorizes contracts, validators, public-safe synthetic
fixtures, and disposable lab artifacts only. It does not authorize deleting
live data.

## Alternatives

- Treat canonical deletion as global erasure. Rejected because descendants,
  exports, backups, training copies, and rebuild paths can survive.
- Let every repository invent an unrelated receipt. Rejected because global
  closure would not be mechanically walkable.
- Store the erased secret inside the recovery probe for later comparison.
  Rejected because the proof would preserve the material it claims to erase.
- Call an unreachable or unsupported surface erased. Rejected because
  inability to inspect is residue.
- Hide approved retention exceptions. Rejected because legal or technical
  residue changes the completion class and deployment posture.

## Consequences

- Every global claim can be walked from C14 to C15, C16, owner extension, C17,
  and content-minimized recovery evidence.
- Positive controls distinguish successful absence from a non-working probe.
- Rebuild and race restoration become explicit falsifiers.
- Training/model obligations cannot be laundered through a storage receipt.
- Private memory classes remain blocked when closure cannot be proven.

## Affected Surfaces

- `mechanics/retention/parts/consolidation-and-forgetting/`
- `docs/memory/MEMORY_MODEL.md`
- `aoa-session-memory` raw and local-port owner extension
- `aoa-kag` projection owner extension
- `abyss-stack` runtime and backup owner extension
- `abyss-machine` host-local owner extension
- `aoa-evals` active-organ offline replay bundle

## Verification

Phase 11 must prove:

- exact ER0-ER9 coverage and parent-owner pins;
- one walkable work item, owner extension, receipt, and recovery probe for
  every surface;
- positive controls detect the synthetic marker before erasure;
- negative exact, lexical, dense, graph, and paraphrase probes recover nothing;
- the recovery probe retains no subject material;
- cache, projection, restore, and rebuild races do not restore material;
- tombstones are content-minimized and do not identify erased payloads;
- exceptions and model-unlearning obligations remain explicit;
- any missing, failed, partial, or residue path blocks the private deployment
  class.
