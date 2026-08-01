# MCP owner evidence review Contract

## Contract

authenticates one stack capture and binds its memo brief to the exact current reviewed-corpus read model without asserting proof, acceptance, or admission

## Owner Boundary

`aoa-memo` owns only the semantic and freshness review of one captured memory
brief. `abyss-stack` owns the authenticated capture and private artifact;
`aoa-sdk` owns the portable review ABI; `aoa-evals` owns proof; later owner
acceptance remains a separate `aoa-memo` act.

## Inputs

- one mode-`0600`, content-addressed stack canary receipt;
- its distinct mode-`0600` result artifact;
- the source-pinned stack signer in `config/review_trust.json`;
- the memo-owned `schemas/aoa-memo-brief-review.schema.json` grounding profile;
- one exact committed `aoa-memo` revision and a clean runtime owner checkout at
  that revision;
- the pinned SDK owner-review schema.

## Review Rules

The reviewer fails closed unless both stack attestations verify, all capture
identities and paths agree, and the capture is still live. The payload must be
`aoa_memo_brief_v1`, preserve the reviewed-memory owner and route-only root
posture, name only safe central contract paths, and return at least one
reviewed-corpus row that exactly matches the committed compact memory-object
catalog and its source object.

Exact freshness requires byte parity between the committed and runtime catalog,
a clean runtime owner checkout at the reviewed revision, and exact returned-row
parity. The owner watermark is the digest of that compact catalog. Workspace
port discovery, MCP transport health, and stack deployment identity remain
separate evidence axes.

## Output

One content-addressed `aoa_organ_owner_result_review_v1` document with a maximum
five-minute owner-review lifetime bounded by the earlier capture expiry.

## Stop-lines

The review does not prove benefit, central proof, owner acceptance, admission,
rollback, current host health, consumer use, or durable memory writes. It never
reads a bearer, starts a service, changes the corpus, or writes anywhere except
the explicitly named private output path.
