# Recall

Use this mode to interpret, compare, or diagnose memory that already belongs
to the owner corpus or one of its declared recall projections.

## Procedure

1. Restate the exact memory question and select the smallest contour:
   object meaning, provenance, temporal posture, lifecycle, current recall,
   contradiction, read-model drift, or consumer handoff.
2. After source return, choose one bounded navigation route:
   - when the request supplies an exact memory-object ID but not its path,
     query only that ID in
     `generated/memory-objects/memory_object_catalog.min.json`. Its envelope
     stores rows under `memory_objects`; use an equivalent of:

     ```text
     jq -ce --arg id "<exact-id>" \
       '[.memory_objects[] | select(.id == $id)]
        | if length == 1 then .[0]
          else error("expected exactly one memory object")
          end' \
       <owner_root>/generated/memory-objects/memory_object_catalog.min.json
     ```

     Require the returned `source_path` to be safe and owner-relative.
   - when the request supplies an exact owner-relative object path, validate
     that it stays under the owner root and use it directly
   - otherwise read the nearest owner route and use `MEMORY_INDEX.md` only
     when its vocabulary or inventory is material

   The compact catalog or an exact MCP search result may locate source; neither
   establishes meaning or currentness. Do not use `find`, repository-wide
   `rg`, `rg --files`, directory listings, envelope-shape probes,
   generated-section scanning, or guessed path probes to resolve an exact ID.
3. For a corpus object whose returned source path begins with `memo/`, read
   exactly `memo/AGENTS.md` as the nearest route card, then the returned
   `object.json` and its sibling `MEMO.md`. Read each file once; use a
   line-number-preserving read on that first pass when citations will be
   needed. Do not reread a source merely to add line numbers.

   Read a `payload_ref` or another provenance source only when the question
   asks for rationale, the object does not contain the needed claim, or two
   already-read sources conflict. Use `docs/memory/MEMORY_MODEL.md` only when
   its vocabulary is material. Do not infer currentness from an index row.
4. Keep confidence, authority, freshness, salience, temperature, lifecycle,
   and proof separate. Preserve `missing`, `unknown`, `stale`, `historical`,
   `superseded`, `retracted`, and `current`.
5. If sources conflict, preserve the contradiction or return to the stronger
   owner. Do not synthesize a smoother claim than the evidence supports.
6. For drift, query the exact object ID or exact source handle in each named
   projection, then walk from that bounded row toward authored source and stop
   at the earliest evidenced mismatch. For the generated memory-object
   capsule, use
   `generated/memory-objects/memory_object_capsules.json`; its rows also live
   under `memory_objects`. Use the same exact-one-row selector shape as the
   compact catalog. Do not list the generated directory, probe the envelope,
   read an entire projection, or query the same row twice.

   For an exact-ID corpus-object-versus-capsule question, the normal complete
   owner read set is: the exact compact-catalog row, `memo/AGENTS.md`, the
   returned `object.json`, its sibling `MEMO.md`, and the exact capsule row.
   Any additional owner read must name the material evidence still missing.
   Disconfirm one adjacent layer only when it could plausibly explain the
   symptom.
7. Return a compact recall capsule using the common output ABI. Do not mutate
   the corpus, lifecycle, generated readers, MCP state, or consumer cache.

## Verification

- inspect the exact object or projection named by the task
- trace every material claim to the strongest source actually read
- distinguish historical truth from current owner truth
- state which live, cross-owner, model, host, security, and consumer checks
  were skipped

## Stop

Stop after one bounded recall, one earliest drift boundary, `no_change`, an
owner handoff, or a blocker. A useful memory remains memory, not proof or
permission.
