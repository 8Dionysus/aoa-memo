# Owner source return

Resolve the canonical `aoa-memo` owner before any owner-relative read. This
route establishes package provenance and owner navigation only; it does not
prove current memory meaning, installed parity, or a disposition.

## Gate

1. Use the `<bundle_dir>` recorded from the loaded `SKILL.md`. Initialize one
   unresolved `<source_route>` and `<owner_root>`.
2. Inspect the exact same-bundle source handle:

   ```text
   <bundle_dir>/.aoa-skill-source.json
   ```

   Establish whether this exact path is a regular readable file. An absent
   handle permits the Git branch below; an unreadable, malformed, or invalid
   existing handle blocks resolution. Metadata and content checks may share
   one tool call, but do not speculate into another source route.
3. If that path is a regular file:

   - set `<source_route>` to `source-handle`
   - require schema `aoa_skill_source_receipt_v1` or
     `aoa_skill_source_receipt_v2`
   - require bundle `aoa-memo` and owner `aoa-memo`
   - require version `0.1.24`
   - require an existing absolute `owner_root`
   - require a safe relative `source_path`
   - require `<owner_root>/<source_path>/SKILL.md`
   - for v2, require non-empty `digest`, `source_fingerprint`,
     `source_fingerprint_scope`, and `prompt_description_sha256`; when
     `capability_graph_hash` is present, require it to be a non-empty string
     and preserve it

   If the path exists but is invalid, mismatched, or not a regular file, return
   `blocked_missing_owner_source`. Do not try another route.
4. Only when the exact same-bundle handle path does not exist, set
   `<source_route>` to `git` and resolve its Git root:

   ```text
   git -C <bundle_dir> rev-parse --show-toplevel
   ```

   Require the returned root to contain `skills/port.manifest.json`.
5. Read the manifest at the resolved owner root:

   ```text
   <owner_root>/skills/port.manifest.json
   ```

   Validate this manifest before relying on owner-relative evidence. The
   resolved root determines the path; no guessed or neighboring manifest may
   substitute for it.
6. Require owner `aoa-memo`, bundle `aoa-memo`, and the actual bundle path. In
   the source-handle branch, also require the same owner, name, and path as the
   handle. A mismatch returns `blocked_missing_owner_source`.
7. After manifest success, follow the owner surfaces required by the selected
   mode. Independent reads may be batched once their paths and authority are
   established.

Require the loaded contract, handle when present, and owner manifest to agree
on package version and identity. If the relevant source revision or content
changed since an earlier read, verify and read the current source before using
its claims. Return `blocked_missing_owner_source` when that identity or current
source cannot be established; extra tool turns cannot supply it.

## Prohibited fallback

Never use `find`, `rg --files`, parent traversal, sibling scans, workspace
conventions, temporary fixtures, `.system`, or another skill directory to
discover a substitute owner. Do not retry the unused branch after a later
owner read fails.

Resolve every owner-relative path beneath the returned root. Treat handle
schema, owner ref, dirty posture, digest, source fingerprint, capability graph
hash, and prompt-description hash as install provenance rather than authority
or current-parity proof.

## Receipt

Report:

- `<source_route>`
- `<owner_root>`
- handle schema and identity dimensions, or git action ref
- manifest action ref
- first owner-read path and action ref used after source validation

A failed or ambiguous source resolution blocks owner-dependent work. Do not
produce an owner-dependent memory disposition from the installed package alone.
