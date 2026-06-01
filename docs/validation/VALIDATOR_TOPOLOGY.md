# Validator Topology

Validators are boundary organs. They protect source authority, projection
parity, runtime declarations, memory context, handoffs, traces, auditability,
security posture, and release composition. They are not a pile of historical
scripts where each wave leaves a standalone gate.

The machine-readable lane map is
[`../../config/validation_lanes.json`](../../config/validation_lanes.json).
This document owns the meaning of the layers; the manifest owns executable
commands and their effective layer, mode, owner surface, and failure route.

## Boundary Classes

| Layer | Role In `aoa-memo` | Hardness | Owner Surface | Failure Route |
|---|---|---|---|---|
| Source/Topology Validators | Authored source, route law, AGENTS mesh, package topology, owner maps, and validator topology. | hard | `docs/validation/VALIDATOR_TOPOLOGY.md` | Fix source authority before generated or release checks. |
| Projection/Generated Validators | Rebuild parity, generated schema shape, inventory drift, compact read models, and provenance of generated surfaces. | hard | `config/root-topology/root_technical_districts.json` | Rebuild from source, then fix source or generator. |
| Capability/Permission Validators | Memo-side local port/export/support-resource boundaries. | boundary-only | `docs/memory/LOCAL_MEMO_PORT_STANDARD.md` | Tool allowlists, MCP scopes, and least privilege route to runtime owners. |
| Runtime Policy Validators | Memory operation modes and write-path runtime declarations. | boundary-only | `docs/posture/MEMORY_OPERATION_MODES.md` | Live approvals, fallback states, cost/time caps, rollback, and circuit breakers route to runtime policy owners. |
| Trace/Eval Validators | Repo-local agent lane scenarios and regression harnesses. | regression | `.agents/spark/AGENTS.md` | Full trajectory, tool-call, state, outcome, grader, and dataset evals route to `aoa-evals`. |
| Memory/RAG/Context Validators | Provenance, freshness, retention, corpus shape, poisoning boundary, and allowed context influence. | hard | `docs/memory/MEMORY_MODEL.md` | Fix memo source, schemas, provenance, or corpus before accepting context readouts. |
| Inter-Agent/Handoff Validators | Memo-side bridge registries, handoff envelopes, allowed delegation, and escalation boundaries. | hard | `mechanics/consumer-handoff/docs/ORCHESTRATOR_MEMORY_ALIGNMENT.md` | Fix mechanic-local bridge source or downstream owner contract. |
| Observability/Audit Validators | Audit examples, landing logs, validation receipts, and traceable public evidence. | promoted audit | `docs/posture/AUDIT_EVENTS.md` | Advisory reports stay soft unless the manifest marks them `blocking-in-release`. |
| Security/Adversarial Validators | Memo-side injection-as-data, source spoofing, poisoning risk, unsafe write handling, and secret-leakage boundary language. | boundary-only | `docs/boundaries/MEMORY_WRITE_PATH_GUARDRAILS.md` | Red-team suites, tool misuse, and runtime enforcement route to security/eval/runtime owners. |
| Release/Nightly/Post-Merge Validators | Frozen artifact gate, nightly drift lane, post-merge rerun route, and compatibility entrypoints. | orchestration | `docs/root/RELEASING.md` | Fix the failing lane owner instead of editing release glue first. |

## Lane Shape

`source-fast` is the growth gate. It checks source/topology only: docs
districts, AGENTS mesh, semantic route cards, mechanic source topology, and
the validator topology itself. It must not check generated freshness, release
packaging, live runtime behavior, trace grading, or security completeness.

`generated` checks projection parity and read-model freshness. Builders with
`--check` are allowed here only because the manifest labels them as
Projection/Generated Validators with an owner surface and failure route.
Generated validators do not own source meaning.

`export/runtime` checks memo-side portable export and support-resource
contracts. It is not proof that a runtime tool allowlist, MCP scope, rate
limit, or approval gate is enforced.

`runtime` checks memory operation mode source and runtime-boundary declarations
inside this repo. Live guardrails, output guards, cost/time caps, HITL,
rollback, and circuit breakers belong to the runtime policy owner.

`memory` checks memory context authority: corpus, provenance, poisoning
boundaries, freshness, and whether memory is allowed to influence the next
agent or surface. Memory remains weaker than proof, route authority, runtime
state, role authority, KAG truth, and source-authored knowledge.
The historical broad `validate_memo.py` entrypoint remains for compatibility,
but release lanes must call its focused profiles rather than the unprofiled
`all` gate.

`handoff` checks memo-side bridge and handoff contracts. It does not authorize
downstream agents by itself.

`eval` runs repo-local agent-lane regression checks. Full multi-turn trace and
environment outcome grading belongs in `aoa-evals`.

`audit` checks that memo-owned actions leave enough evidence. Audit reports are
advisory unless this topology explicitly promotes them into release as
`blocking-in-release`.

`security` checks memo-side adversarial memory boundary declarations.
Prompt-only guardrails are not a security boundary.

`release` composes named lanes for a frozen artifact. `nightly` composes drift
signals and soft boundary checks; it is not the same gate as release.
`post-merge` confirms landed-main projection and regression health after a
merge without pretending to be release packaging or nightly drift analysis.

## Prohibitions

- Do not add a single `validate_everything.py`.
- Do not keep historical standalone validators outside lane ownership.
- Do not duplicate the same rule in lint, release, and tests.
- Do not treat prompt-only guardrails as a security boundary.
- Do not make audit/report scripts hard blockers unless this topology promotes them.
- Do not let generated validators define source meaning.
- Do not let a builder with `--check` become an unlabeled release validator.
- Do not claim live runtime or eval enforcement from static repo checks.

## Promotion Rule

A check may move from advisory or boundary-only into release only when the
manifest names:

- the validator layer,
- the mode (`blocking`, `blocking-in-release`, `boundary-only`, or `advisory`),
- the owner surface,
- the failure route, and
- the focused command sequence that runs it.

If that metadata is missing, the check is not a release validator.
