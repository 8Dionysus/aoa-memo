# Pre-correction external-actor landing receipt was rejected and superseded

## Memory

The 10:40 receipt for the role-first external-actor claim is retained as
historical evidence, but its machine result is now `rejected`: the origin
claim-object override did not exist at that time. The 11:18 receipt is the
only `result: landed` authority for the object. This audit event records the
provenance/lifecycle correction; it does not change the bounded claim or add
proof, runtime, stats, or pattern authority.

## Source Route

- `memo/intake/receipts/20260815T104000Z.aoa-agents.role-first-external-actor-responsibility-return.landing-receipt.json`
- `memo/intake/receipts/20260815T111816Z.aoa-agents.role-first-external-actor-responsibility-return.landing-receipt.json`
- `memo/objects/claims/2026/role-first-external-actor-responsibility-return/object.json`
- `repo:aoa-agents/memo/receipts/20260815T111200Z.role-first-external-actor-claim-correction.forwarding-receipt.json`
- `https://github.com/8Dionysus/aoa-memo/pull/299#discussion_r3789278376`

## Review Posture

This is a historical `audit_event` with `current_recall.status=historical`.
It exists to keep the receipt lane machine-readable and auditable after the
post-merge correction. It is not an external-agent proof object, a stronger
claim, or recurring-pattern admission.

## Next Routes

Use the current 11:18 landing receipt for successful landing authority. Use
the rejected 10:40 receipt and this audit event only when tracing the
pre-authorization correction.
