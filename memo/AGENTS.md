# AGENTS.md

Route card for `memo/`.

## Purpose

`memo/` is the reviewed memory corpus district for `aoa-memo`.
It holds source-owned memory object bundles that have landed in this repository
after review, plus the small support lanes needed to keep those objects
addressable, inspectable, and ready for generated read models.

This district is the repo's own memory body. Local `repo/memo/` ports in other
repositories feed candidates and intake packets toward this corpus; they do not
share this shape.

## Route Stack

- Above: root `AGENTS.md`, `DESIGN.md`, `MEMORY_INDEX.md`,
  `docs/memory/MEMORY_MODEL.md`, and `docs/root/ROOT_SURFACE_LAW.md`.
- Here: reviewed object bundles, corpus support lanes, and reviewed intake
  receipts.
- Across: `schemas/memory-objects/`, `docs/memory/`, `examples/`, and
  `generated/memory-objects/`.
- Downstream: MCP resources, recall briefs, eval/KAG handoff surfaces, and
  generated memory catalogs.

## Corpus Shape

Use object bundles:

```text
memo/objects/<kind-dir>/<year>/<slug>/
  object.json
  MEMO.md
```

`object.json` is the machine-checkable object and must validate against
`schemas/memory-objects/memory_object.schema.json` plus the kind-specific
schema. `MEMO.md` is the human-facing companion and should explain the same
object without becoming stronger than the JSON contract.

Object kind directories are:

- `anchors/`
- `state-capsules/`
- `episodes/`
- `claims/`
- `decisions/`
- `patterns/`
- `bridges/`
- `audit-events/`

## Support Lanes

- `support/provenance-threads/` holds reviewed provenance-thread material when
  the thread is stronger as corpus support than as an example.
- `support/recall-contracts/` holds reviewed recall contracts that serve the
  corpus directly.
- `intake/reviewed/` holds accepted intake packets before or alongside corpus
  landing.
- `intake/quarantine/` holds bounded intake material that must not be promoted
  yet.
- `intake/receipts/` records local checks and landing receipts for this corpus.

## Placement

Add a new bundle here when `aoa-memo` is the reviewed memory owner and the
object should survive as durable OS Abyss memory truth.

Keep public teaching examples in `examples/`. Keep candidate packets in the
origin repository's local `memo/` port. Keep raw session evidence in `.aoa`.
Keep generated recall/read models in `generated/`.

## Reviewed Intake Landing

Use `scripts/memory/land_reviewed_memo_intake.py` when an origin
`repo/memo/exports/*.aoa-memo-intake.json` packet has `allowed_result:
reviewed_write` and review accepts a durable object bundle.

Run it first without `--write` to inspect the planned object path, copied
intake packet, and landing receipt. Add `--write` only after the object kind,
slug, title, summary, and recall posture are correct.

## Validate

```bash
python scripts/memory/validate_memo_corpus.py
python scripts/memory/generate_memory_object_surfaces.py --check
python scripts/agents/validate_agents_mesh.py
python scripts/root-topology/validate_root_technical_districts_index.py
python -m pytest -q tests/memory/test_memo_corpus.py tests/memory/test_reviewed_intake_landing.py tests/agents/test_agents_mesh.py tests/root-topology/test_root_technical_districts_index.py
```
