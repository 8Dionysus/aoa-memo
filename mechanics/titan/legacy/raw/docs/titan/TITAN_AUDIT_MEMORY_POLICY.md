# Titan Audit Memory Policy

A Titan report is not memory.

A finding may become a memory candidate only during closeout, and only if it has:
- source refs
- bounded claim
- owner route hint
- promotion status = candidate

Compaction-recovered sources must carry confidence limits.
