# Consumer Handoff Memo Mechanic

Consumer handoff is the memo-side mechanic for publishing bounded memory
surfaces that stronger neighboring owners may inspect, scope, evaluate, bridge,
or orchestrate without turning `aoa-memo` into their authority layer.

## Mechanic card

- Status: `landed`

### Operation

publish memo-owned consumer handoff surfaces so stronger owner layers can inspect, scope, evaluate, bridge, or orchestrate memory without absorbing memo authority

### Trigger

Use when a memo surface exists primarily so `aoa-agents`, `aoa-playbooks`,
`aoa-evals`, `aoa-kag`, Tree of Sophia bridge work, routing/orchestrator
families, stats summaries, or another consumer can use memory safely while
keeping stronger policy, proof, graph, scenario, route, summary, or source
meaning outside this repository.

### Memo owns

Memo owns the public memory descriptors, scope grammar, recall-mode guidance,
source refs, bridge/export faces, guardrail case descriptions, and
orchestrator-facing recall posture that consumers may cite.

### Stronger owner split

- `aoa-agents` owns actor identity, role rights, approvals, handoff policy,
  freeze rights, and promotion authority.
- `aoa-playbooks` owns scenario composition, choreography, and campaign return
  posture.
- `aoa-evals` owns scoring, pass/fail logic, evidence weighting, and proof
  verdict language.
- `aoa-kag` owns graph substrate normalization, federation-spine activation,
  and derived KAG semantics.
- `aoa-stats` owns derived movement summaries, trend aggregation, and
  observability posture over memory movement.
- `Tree-of-Sophia` owns source-authored ToS meaning, nodes, fragments,
  concepts, and lineages.
- `aoa-routing` owns dispatch behavior and route compression policy.
- `abyss-stack` owns runtime stores, workers, and operational execution.

### Inputs

Consumer-facing memo contracts, role-posture field lists, playbook recall
scope guidance, guardrail case packs, KAG/ToS bridge docs, source-owned donor
export notes, orchestrator quest alignment notes, and consumer feedback that a
memo surface is ambiguous or overclaims.

### Outputs

Bounded handoff surfaces, source refs, consumer field lists, scope and recall
mode notes, bridge/export contract notes, guardrail handoff cases, owner-route
stop-lines, generated or example ref updates, and validator requirements.

### Must not claim

- agent role rights, approvals, or actor identity
- playbook scenario authority or choreography
- eval verdicts, scoring, or proof status
- normalized KAG graph truth or federation activation
- Tree-of-Sophia source meaning by rewrite
- routing sovereignty or orchestrator class identity
- runtime storage, workers, or live operational state

### Validation

Use the validation lane in [AGENTS](AGENTS.md#validation).

### Next route

Route role policy to `aoa-agents`, scenario composition to `aoa-playbooks`,
proof to `aoa-evals`, graph substrate work to `aoa-kag`, derived memory
movement summaries to `aoa-stats`, source-authored ToS meaning to
`Tree-of-Sophia`, dispatch behavior to `aoa-routing`, and runtime execution or
storage to `abyss-stack`.

## Active Route

- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [PROVENANCE](PROVENANCE.md)
- [LANDING_LOG](LANDING_LOG.md)
- [ROADMAP](ROADMAP.md)
- [docs](docs/)
- [legacy index](legacy/INDEX.md)

## Functioning Parts

The active part map is [PARTS](PARTS.md). Source docs live in [docs](docs/).

## Historical Provenance

Use [PROVENANCE](PROVENANCE.md) first. Use [legacy](legacy/README.md) only
when auditing old flat docs-root placement.

## Owner Boundary

Consumer handoff remains a memo mechanic until a stronger owner accepts,
evaluates, activates, routes, or executes the next claim. Memo can publish a
safe handoff surface; it cannot make the consumer's stronger decision.

## Growth Posture

Future work should add typed handoff examples or generated consumer indexes
only when repeated consumer use proves a stable need. Do not widen this package
into a neighbor-owned doctrine mirror.
