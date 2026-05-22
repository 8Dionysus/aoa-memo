# Memory Object Shape

This file defines how reviewed memory objects live in `aoa-memo/memo/`.

## Design Choice

Store each reviewed memory as a small directory bundle:

```text
memo/objects/<kind-dir>/<year>/<slug>/
  object.json
  MEMO.md
```

The bundle is intentionally plain:

- JSON keeps the object machine-checkable and indexable.
- Markdown keeps the object readable and reviewable by humans and agents.
- The directory gives the object room to grow later without renaming the object.

## Kind Directories

| Object kind | Directory |
|---|---|
| `anchor` | `anchors/` |
| `state_capsule` | `state-capsules/` |
| `episode` | `episodes/` |
| `claim` | `claims/` |
| `decision` | `decisions/` |
| `pattern` | `patterns/` |
| `bridge` | `bridges/` |
| `audit_event` | `audit-events/` |

Use the schema kind, not the directory spelling, inside `object.json`.

## Object JSON

`object.json` must validate against:

1. `schemas/memory-objects/memory_object.schema.json`
2. the kind-specific schema under `schemas/memory-objects/`

The minimum practical fields are:

- `id`
- `kind`
- `title`
- `summary`
- `scope`
- `owner_refs`
- `payload_ref`
- `time`
- `provenance.source_refs`
- `trust`
- `lifecycle`
- `access`
- `bridges`

The object should answer:

- what is remembered;
- where the evidence or source route is;
- who owns stronger truth;
- how current it is;
- whether it may be recalled, superseded, retracted, archived, or exported.

## Memo Markdown

`MEMO.md` should stay short and use this shape:

```markdown
# <Title>

## Memory
...

## Source Route
...

## Review Posture
...

## Next Routes
...
```

The Markdown companion explains the object. It should not add claims missing
from `object.json`.

## Intake Relationship

External repositories send memory toward `aoa-memo` through local memo ports:

```text
repo/memo/candidates -> repo/memo/exports -> aoa-memo reviewed intake -> memo/objects
```

Inside `aoa-memo`, `memo/intake/` stores reviewed packets and receipts for this
corpus. The durable memory object is the bundle under `memo/objects/`.

The landing route is explicit:

1. The origin export packet must set `allowed_result` to `reviewed_write`.
2. Candidate and receipt refs must resolve inside the origin memo port.
3. `scripts/memory/land_reviewed_memo_intake.py` copies the accepted packet to
   `memo/intake/reviewed/`, creates the target object bundle, and writes a
   `memo/intake/receipts/*.landing-receipt.json` record.
4. `validate_memo_corpus.py` verifies the copied packet, landing receipt, and
   object bundle remain connected.

## Growth Rule

Prefer adding a precise bundle over adding a flat root document.

If a memory needs many objects, make several small bundles connected by
`provenance.provenance_thread_id`, lifecycle links, and source refs. Generated
catalogs and MCP resources can then assemble views without turning the corpus
into one large mutable file.
