# Decision: Reviewed Memory Corpus District

- Decision ID: AOA-MEM-D-0063

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: reviewed corpus
- Mechanic parents: none
- Guard families: reviewed corpus/intake
- Memory object classes: decision
- Posture: active rationale

## Context

`aoa-memo` already owns memory doctrine, schemas, public examples, generated
read models, local memo port contracts, and memo mechanics. The reviewed object
corpus itself was still implicit: durable memory objects appeared as examples,
mechanic fixtures, generated projections, or incoming local-port packets.

OS Abyss needs a clear central memory body that can grow without turning root
docs, generated files, or external repo ports into source truth.

Fresh May 2026 memory-system practice points in the same direction:

- session memory and compaction are useful, but they are conversation/session
  continuity, not a reviewed cross-system memory corpus;
- long-term memory benefits from layered storage and scoped retrieval;
- graph/RAG faces work best as derived read models over sourced episodes,
  facts, and relationships;
- persistent memory is now a security boundary, because poisoned or sleeper
  memories can survive into future conversations.

## Decision

Add root `memo/` as the reviewed memory corpus district for `aoa-memo`.

Use object bundles:

```text
memo/objects/<kind-dir>/<year>/<slug>/
  object.json
  MEMO.md
```

`object.json` is the machine-checkable memory object. `MEMO.md` is the human
companion. Support surfaces live under `memo/support/`; reviewed intake packets
and receipts live under `memo/intake/`.

Do not copy the local port shape here. Local `repo/memo/` ports use `PORT.yaml`,
`candidates/`, `receipts/`, `exports/`, and `local/`. The central corpus owns
reviewed object bundles after landing.

## Consequences

- Reviewed memory now has a visible corpus home in `aoa-memo`.
- Local memo ports keep their candidate/export role without becoming durable
  truth.
- Generated read models can consume corpus-backed objects without changing the
  object bundle contract.
- MCP, RAG, KAG, and graph layers get a stable object-id/source-ref/lifecycle
  substrate instead of treating retrieved text as authority.
- New corpus content has a narrow validator and AGENTS route card from the
  first landing.

## Validation

The corpus must pass:

```bash
python scripts/memory/validate_memo_corpus.py
python -m pytest -q tests/memory/test_memo_corpus.py
```

Route-card and root topology changes must also pass the AGENTS mesh and root
technical district checks.
