# Deployment Incident Memory Gate

Deployment incidents enter memo only when evidence, review posture, owner
route, and future effect exist.

This surface belongs to the operational-gate memo mechanic. It decides whether
a deployment incident is memory material. It does not decide release quality,
runtime remediation, rollback execution, current service health, or proof.

## Admission Rule

An incident may enter durable memo recall when all of these are present:

- `gate_id`: a stable memory-gate decision reference
- `incident_id`: a stable incident or release-train reference
- `decision`: the bounded admission outcome for durable memo recall
- `reason`: the evidence-linked rationale for the admission outcome
- `evidence_refs`: reviewable refs to logs, reports, PRs, CI runs, release
  notes, or owner receipts
- `review_posture`: the verdict, evaluation result, or owner review posture
  that explains why the incident is meaningful
- `owner_route`: the repository or service owner that owns the next stronger
  consequence
- `future_effect`: the concrete future recall effect, such as a regression
  sentinel, release checklist update, retention watch, or writeback candidate
- `expiry_or_recheck`: the condition under which the memory expires, is
  rechecked, or becomes recurrence evidence

Low severity noise expires unless recurrence proves materiality.

## Reject By Default

Do not admit an incident merely because it was loud, recent, frustrating, or
operationally adjacent. Without evidence, owner route, review posture, and
future effect, it remains working context outside durable memo.

## Mechanic-Local Technical Contracts

Current public contract examples live with the operational-gate mechanic:

- `mechanics/operational-gate/parts/deployment-incident-gate/schemas/deployment_incident_memory_gate_v1.json`
- `mechanics/operational-gate/parts/deployment-incident-gate/examples/deployment_incident_memory_gate.example.json`
- `mechanics/operational-gate/parts/deployment-incident-gate/schemas/deployment_lesson_candidate_v1.json`
- `mechanics/operational-gate/parts/deployment-incident-gate/examples/deployment_lesson_candidate.example.json`

These contracts teach admissible shape. They do not become proof or runtime
state.

## Next Route

- Release quality and rollout decisions route to the release owner.
- Runtime remediation routes to `abyss-stack` or the runtime owner.
- Proof, smoke, and regression verdicts route to `aoa-evals`.
- Retention outcome tracking routes to the retention mechanic.
- Owner return lanes route to the writeback mechanic.

Memo preserves only the reason an incident should or should not be remembered.
