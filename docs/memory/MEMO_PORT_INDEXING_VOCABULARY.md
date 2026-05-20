# Memo Port Indexing Vocabulary

## Purpose

This document names the controlled vocabulary for local `memo/` ports.

The vocabulary lets OS Abyss classify local memory packets without turning
every repository into its own private taxonomy. It is intentionally small:
classification should be enough for indexing, routing, validation, and review,
not a complete ontology.

## Source Surface

The machine-readable source is:

- `config/memory-ports/indexing_vocabulary.json`

The compact generated companion is:

- `generated/memory/memo_port_vocabulary.min.json`

## Terms

Use `kind` for the shape of remembered item:

```text
decision
route
pattern
lesson
constraint
incident
preference
checkpoint
handoff
```

Use `family` for the memory family:

```text
memory-access
runtime
topology
validation
release
agent-behavior
provenance
kag-bridge
session-recovery
```

Use `scope` for where the memory applies:

```text
session
repo
workspace
project
ecosystem
host
agent
```

Use `route` for where the packet is trying to go:

```text
local_only
reviewed_intake
owner_handoff
quarantine
archive
```

Use `review_state` for local review progress:

```text
candidate
validated
rejected
forwarded
reviewed
landed
superseded
archived
```

Use `lifecycle` for memory posture:

```text
captured
candidate
reviewed
current
superseded
retracted
archived
frozen
```

Use `source_trust` for source posture:

```text
review_required
reviewed_owner_source
untrusted
unknown
derived
generated
```

Use `risk` for write-path risk markers:

```text
indirect_prompt_injection
sleeper_memory
poisoned_experience
source_spoofing
private_data_bleed
instruction_as_content
stale_context
permission_leakage
over_promotion
hallucinated_merge
```

## Extension Law

Local ports may define local terms in `PORT.yaml` when the central vocabulary
is too coarse.

Local terms must not redefine central terms. They should be visibly local,
preferably owner-prefixed or owner-obvious. A local term that appears in three
or more repositories should be proposed for central review instead of copied
forever.

## Boundary

Vocabulary terms route and index local memory packets. They do not promote
local candidates into durable memory, decide truth, or grant access rights.

