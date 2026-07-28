# Antifragility Memo Mechanic

Antifragility is the memo-side mechanic for preserving reviewed failure lessons
and recovery patterns without becoming proof, route authority, stats truth, or
runtime repair.

## Mechanic card

- Status: `landed`

### Operation

preserve reviewed failure lessons and recovery patterns as recallable memory without granting repair authority

### Trigger

Use when repeated stress, drift review, rollback follow-through, recovery
windows, or failure lessons must become explicit, source-linked, recallable,
and bounded.

### Memo owns

Memo owns failure-lesson and recovery-pattern memory posture, recall guidance,
source-ref requirements, suppression/freshness boundaries, lineage context,
and stop-lines for later review.

### Stronger owner split

- Source repositories own receipts, incident truth, rollback windows, and
  current health.
- `aoa-evals` owns proof that a recovery or failure claim holds.
- `aoa-stats` owns derived summaries over repeated windows.
- `aoa-sdk` owns route behavior and dispatch.
- `aoa-playbooks` owns scenario choreography and campaign cadence.
- `abyss-stack` owns runtime repair, live storage, and operational execution.

### Inputs

Reviewed source receipts, rollout or drift windows, rollback follow-through
windows, eval reports, stats summaries, route hints, lineage refs, and
operator-reviewed posture notes.

### Outputs

Bounded failure-lesson docs, recovery-pattern docs, schema/example source
refs, generated object surface inputs, and stronger-owner handoff routes.

### Must not claim

- the current run matches a past stressor by itself
- a failure or recovery claim has proof status
- a rollback or repair is authorized
- a route is safe without checking stronger evidence
- derived stats are source truth
- `aoa-memo` owns live operational health

### Validation

Use the validation lane in [AGENTS](AGENTS.md#validation).

### Next route

Route source receipts to the owner repository, proof to `aoa-evals`, repeated
window summaries to `aoa-stats`, dispatch behavior to `aoa-sdk`, scenario
composition to `aoa-playbooks`, and runtime repair to `abyss-stack`.

## Active Route

- [DIRECTION](DIRECTION.md)
- [PARTS](PARTS.md)
- [OWNER_MAP](OWNER_MAP.md)
- [PROVENANCE](PROVENANCE.md)
- [LANDING_LOG](LANDING_LOG.md)
- [ROADMAP](ROADMAP.md)
- [legacy index](legacy/INDEX.md)

## Functioning Parts

The active part map is [PARTS](PARTS.md). Source docs live in [docs](docs/).

## Historical Provenance

Use [PROVENANCE](PROVENANCE.md) first. Use [legacy](legacy/README.md) only when
auditing old flat docs-root placement.

## Owner Boundary

Antifragility remains a memo mechanic here until stronger owners accept proof,
runtime repair, route behavior, stats truth, source receipts, or scenario
authority.

## Growth Posture

Future antifragility work should sharpen source refs and suppression posture
before adding any stronger claim.
