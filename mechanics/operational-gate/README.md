# Operational Gate Memo Mechanic

Operational gate is the memo-side mechanic for deciding which operational
incidents, office-service events, untrusted write attempts, service revision
records, and post-release memory boundaries may become durable recall surfaces.

It preserves reviewed operational memory without turning `aoa-memo` into
rollout authority, runtime state, proof logic, or service ownership.

## Mechanic card

- Status: `landed`

### Operation

gate operational incidents, office/service revision entries, and post-release memory boundaries into durable recall only when evidence, owner route, review posture, retention posture, and future effect justify memory

### Trigger

Use when an operational event, deployment incident, service office incident,
untrusted or derived write attempt, service revision, release-train note, or
post-release boundary wants to enter memo and the repository must decide
whether the event is material memory, temporary noise, retention evidence,
writeback material, quarantine material, or a stronger-owner decision.

### Memo owns

Memo owns the memory admission rule, evidence/ref requirements, owner-route
stop-lines, write-path guard posture, future-effect wording, service revision
recall posture, post-release memory boundaries, and the public-safe examples
and schemas that teach those shapes.

### Stronger owner split

- `Agents-of-Abyss` owns center doctrine, experience stage law, live office
  expansion law, release-train posture, and program authority.
- `abyss-stack` or the runtime owner owns live deployment, service state,
  workers, storage, rollback execution, and operational remediation.
- `aoa-evals` owns proof, smoke, regression, verdict, and quality gates.
- `aoa-agents` owns assistant identity, rights, approvals, and handoff policy.
- `aoa-playbooks` owns release, rollback, campaign, and incident choreography.
- `aoa-sdk` owns dispatch behavior and route compression.
- `aoa-stats` owns derived operational observability and movement summaries.
- `Tree-of-Sophia` owns source-authored meaning and ToS write stop-lines.

### Inputs

Deployment incident candidates, service incident candidates, office event
markers, untrusted write candidates, derived summaries, service revision
entries, release-train memory entries, post-release boundary reviews,
owner-route refs, evidence refs, verdict refs, retention or expiry posture, and
recurrence signals.

### Outputs

Memory gate decisions, allowed, rejected, quarantined, or candidate-only memory
entries, service revision ledger posture, post-release boundary notes,
future-effect refs, owner-route handoffs, retained technical contract refs,
legacy placement provenance, and validator requirements.

### Must not claim

- release approval or release quality
- current service health
- incident root cause
- live deployment, rollback, or remediation execution
- eval proof or smoke verdict
- assistant/service role rights
- route dispatch authority
- Tree-of-Sophia runtime write authority
- owner acceptance by implication

### Validation

Use the validation lane in [AGENTS](AGENTS.md#validation).

### Next route

Route program law to `Agents-of-Abyss`, runtime action to `abyss-stack` or the
runtime owner, proof to `aoa-evals`, role rights to `aoa-agents`, release and
rollback choreography to `aoa-playbooks`, dispatch behavior to `aoa-sdk`,
derived operational summaries to `aoa-stats`, and source meaning to
`Tree-of-Sophia`.

## Active Route

- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [PROVENANCE](PROVENANCE.md)
- [LANDING_LOG](LANDING_LOG.md)
- [ROADMAP](ROADMAP.md)
- [docs](docs/)
- Historical recovery: see [AOA-MEM-D-0090](../../docs/decisions/AOA-MEM-D-0090-retire-spark-and-legacy-mechanics.md).

## Functioning Parts

The active part map is [PARTS](PARTS.md). Source docs live in [docs](docs/).

## Historical Provenance

Use [PROVENANCE](PROVENANCE.md) first. Historical recovery is pinned in [AOA-MEM-D-0090](../../docs/decisions/AOA-MEM-D-0090-retire-spark-and-legacy-mechanics.md).
auditing old flat docs-root placement.

## Owner Boundary

Operational gate remains a memo mechanic until a stronger owner decides the
release, runtime, proof, role, route, stats, or source-meaning consequence.
Memo can preserve why an operational event should be remembered; it cannot
make the operational decision.

## Growth Posture

Future work should add stricter operational-gate examples or validators only
when repeated incidents prove a stable contract. Do not widen this package
into a release authority mirror or runtime incident system.
