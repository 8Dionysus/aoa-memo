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

- canonical `Decision ID: AOA-MEM-D-####`
- context
- decision
- alternatives or tradeoffs
- consequences
- affected surfaces
- verification route

Each decision record must carry an `## Index Metadata` block with:

- original date
- surface classes
- mechanic parents
- guard families
- memory object classes
- posture

Generated lookup indexes under `docs/decisions/indexes/` are read models from
that metadata. They make lookup cheaper for agents; they do not replace the
decision note or the stronger source surfaces the decision describes.
Keep `modeled_surfaces` in `docs/decisions/indexes/index_contract.yaml` as a
top-level list of normalized repo-relative paths under `docs/decisions/`; do
not use it for root non-record Markdown.

Use full canonical-ID decision paths as the active source files:
`AOA-MEM-D-####-*.md`. Use the canonical decision ID as the stable handle.
Do not recreate date-named files, short numbered files, or generated
compatibility maps for them. Previous path names belong to git and PR history,
not to the active decision lookup surface.

Keep the record public-safe. Do not include private traces, secrets, local-only
host details, or unreduced personal data.

Verify decision-lane changes with:

```bash
python scripts/root-topology/build_decision_indexes.py --check
python -m pytest -q tests
python scripts/release/release_check.py
```
