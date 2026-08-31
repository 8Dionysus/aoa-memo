# AGENTS.md

## Applies to

`mechanics/operational-gate/` and its active mechanic surfaces.

## Role

The operational-gate mechanic owns memo-side memory admission for operational
incidents, office/service events, untrusted or derived write attempts, service
revisions, release-train memory, and post-release boundary surfaces.

It decides how `aoa-memo` preserves operational memory as public, reviewable,
source-linked recall. It does not decide releases, execute runtime changes,
prove incidents, grant service rights, route live traffic, or summarize current
operational health.

## Local delta

The `operational-gate` mechanic identity remains local; shared package, docs, parts, and
legacy hierarchy is inherited from `mechanics/AGENTS.md`. Its package card,
DIRECTION.md, PARTS.md, OWNER_MAP.md, and PROVENANCE.md remain the semantic
anchors for this operation.

## Boundaries

- Keep operational-gate docs memory-only, evidence-linked, and
  operation-first.
- Do not claim release approval, current service health, incident root cause,
  runtime remediation, eval verdicts, service role rights, route dispatch, ToS
  runtime writes, or owner acceptance.
- Keep old flat docs-root paths out of active references except in provenance,
  legacy, decisions, and former-path source maps.
- Do not move public schemas or examples into this package unless the artifact
  topology rule proves they are single-mechanic-owned.
- Keep retention outcomes with the retention mechanic and writeback return
  lanes with the writeback mechanic unless this package is only deciding the
  admission gate.

## Verification

Use the nearest `VALIDATION.md` route for `operational-gate` work after the touched
surface is known; reusable lanes remain in `config/validation_lanes.json`.

## Closeout

Report the operational-gate docs changed, whether mechanic-local artifacts and
adjacent package refs stayed owner-routed, whether old flat docs-root references
remain only as allowed provenance, and which stronger owner boundaries stayed
outside `aoa-memo`.
