# AGENTS.md

## Guidance for `docs/decisions/`

`docs/decisions/` preserves durable rationale for memory-layer topology,
ownership, route-law, validator, public-contract, and workflow choices.

Decision records explain why a path was chosen. They do not replace active
source docs, schemas, examples, generated companions, validators, or root
`AGENTS.md`.

Use this lane when future contributors need to know why a structure exists or
why a plausible alternative was rejected.

Do not use this lane for:

- raw evidence
- session transcripts
- generated output
- release notes
- roadmap promises
- routine implementation details
- sibling-owner doctrine

Decision records should name:

- context
- decision
- alternatives or tradeoffs
- consequences
- affected surfaces
- verification route

Keep the record public-safe. Do not include private traces, secrets, local-only
host details, or unreduced personal data.

Verify decision-lane changes with:

```bash
python -m pytest -q tests
python scripts/release/release_check.py
```
