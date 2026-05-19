# AGENTS.md

## Applies To

This card applies to `mechanics/recurrence-support/`.

## Role

The recurrence-support mechanic owns memo-side support for bounded relaunch
anchors, witness trace exports, and reviewed closeout recall landings.

It keeps route-return memory public, source-linked, and reviewable. It does not
own recurrence doctrine, dispatch behavior, runtime retry policy, actor rights,
proof verdicts, scenario choreography, or owner acceptance.

## Read Before Editing

Read root `AGENTS.md`, `mechanics/AGENTS.md`, this file, `README.md`,
`DIRECTION.md`, `PARTS.md`, `OWNER_MAP.md`, and `PROVENANCE.md`.

For source docs, continue through `docs/AGENTS.md` and the target `docs/*.md`
surface.

For schemas, examples, generated outputs, scripts, tests, quests, or manifests
that reference recurrence-support docs, read the nearest local `AGENTS.md`
before editing that district.

## Boundaries

- Keep recurrence-support docs memory-only, evidence-linked, and
  operation-first.
- Do not claim route dispatch, tier escalation, runtime retry budgets, live
  scratchpad storage, role rights, identity continuity, eval proof, playbook
  acceptance, source truth, or owner acceptance.
- Do not introduce `return_memory` or another return-only memory-object family.
- Keep old flat docs-root paths out of active references except in provenance,
  legacy, decisions, and former-path source maps.
- Do not move checkpoint schemas or examples back into this package; use
  `mechanics/checkpoint/` for checkpoint artifacts and this package for
  route-return support that consumes them.
- Keep writeback return lanes with writeback and consumer scope posture with
  consumer-handoff unless this package is only preserving relaunch support.

## Post-Change Review

After recurrence-support changes, check whether these surfaces moved:

- `DIRECTION.md`
- `PARTS.md`
- `OWNER_MAP.md`
- `PROVENANCE.md`
- `LANDING_LOG.md`
- `ROADMAP.md`
- `legacy/INDEX.md`
- recurrence-support package contract refs in
  `mechanics/recurrence-support/{schemas,examples,tests}/` plus shared recall
  and quest refs
- generated mechanics or AGENTS mesh companions
- docs-root maps, root route cards, decision records, changelog, or roadmap

Update only surfaces whose future-facing meaning changed.

## Validation

```bash
python scripts/validate_memo_mechanics.py
python scripts/build_memo_mechanics_index.py --check
python scripts/validate_memo_mechanics_index.py
python scripts/validate_agents_mesh.py
python scripts/build_agents_mesh_index.py --check
python scripts/validate_agents_mesh_index.py
python scripts/validate_memo.py
python -m pytest -q mechanics/recurrence-support/parts/witness-trace-contract/tests/test_recurrence_support_mechanic.py tests/test_memo_mechanics.py tests/test_agents_mesh.py tests/test_memo_validators.py mechanics/consumer-handoff/parts/playbook-scope-handoff/tests/test_playbook_memory_scopes.py tests/test_roadmap_parity.py
```

Before landing, also run:

```bash
python scripts/release_check.py
```

## Closeout

Report recurrence-support docs changed, whether package-local artifacts and
shared recall/quest refs stayed owner-routed, whether old flat docs-root
references remain only as allowed provenance, and which stronger owner
boundaries stayed outside `aoa-memo`.
