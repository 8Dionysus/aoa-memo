from __future__ import annotations

from typing import Any

from memory_object_surface_common import (
    CORPUS_RECALL_MODES_BY_KIND,
    EXAMPLE_MANIFEST_SOURCE,
    MANIFEST_PATH,
    MEMO_OBJECTS,
    ROOT,
    SOURCE_KIND_REVIEWED_CORPUS,
    SOURCE_KIND_TEACHING_FIXTURE,
    JsonDict,
    SourceObject,
    fail,
    load_json,
    object_reference_fields,
    scope_classes_for,
    shipped_kinds,
)
from validate_memo import local_ref_error, validator_for


def validate_manifest() -> JsonDict:
    validator = validator_for("memory_object_surface_manifest.schema.json")
    manifest = load_json(MANIFEST_PATH)
    errors = [
        f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(manifest), key=lambda err: list(err.absolute_path))
    ]
    if errors:
        fail(MANIFEST_PATH.name, errors)
    return manifest


def validate_local_refs(memory_object: JsonDict, source_path: str) -> list[str]:
    errors: list[str] = []
    ref_checks: list[tuple[str, object]] = [("payload_ref", memory_object.get("payload_ref"))]
    for index, value in enumerate(memory_object.get("provenance", {}).get("source_refs", [])):
        ref_checks.append((f"provenance.source_refs[{index}]", value))
    ref_checks.append(("bridges.route_capsule_ref", memory_object.get("bridges", {}).get("route_capsule_ref")))
    for label, value in ref_checks:
        error = local_ref_error(value, f"{source_path}:{label}")
        if error:
            errors.append(error)
    return errors


def validate_memory_object(
    *,
    memory_object: JsonDict,
    source_path: str,
    validator: Any,
    allowed_kinds: set[str],
    errors: list[str],
) -> bool:
    validation_errors = [
        f"{source_path}:{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
        for err in sorted(validator.iter_errors(memory_object), key=lambda err: list(err.absolute_path))
    ]
    if validation_errors:
        errors.extend(validation_errors)
        return False
    if memory_object["kind"] not in allowed_kinds:
        errors.append(f"{source_path}: object kind {memory_object['kind']} is outside the shipped canon")
    try:
        scope_classes_for(memory_object)
    except ValueError as exc:
        errors.append(f"{source_path}: {exc}")
    errors.extend(validate_local_refs(memory_object, source_path))
    return True


def load_curated_objects(manifest: JsonDict) -> list[SourceObject]:
    validator = validator_for("memory_object.schema.json")
    allowed_kinds = shipped_kinds()
    seen_paths: set[str] = set()
    seen_ids: set[str] = set()
    curated: list[SourceObject] = []
    errors: list[str] = []

    if manifest.get("source_of_truth") != EXAMPLE_MANIFEST_SOURCE:
        errors.append(f"{MANIFEST_PATH.relative_to(ROOT)} must stay source_of_truth={EXAMPLE_MANIFEST_SOURCE}")

    for entry in manifest["entries"]:
        source_path = entry["example_path"]
        if source_path in seen_paths:
            errors.append(f"duplicate manifest example_path: {source_path}")
            continue
        seen_paths.add(source_path)
        example_path = ROOT / source_path
        if not example_path.exists():
            errors.append(f"manifest example_path does not exist: {source_path}")
            continue
        memory_object = load_json(example_path)
        if not validate_memory_object(
            memory_object=memory_object,
            source_path=source_path,
            validator=validator,
            allowed_kinds=allowed_kinds,
            errors=errors,
        ):
            continue
        object_id = memory_object["id"]
        if object_id in seen_ids:
            errors.append(f"duplicate memory object id in manifest set: {object_id}")
            continue
        seen_ids.add(object_id)
        curated.append((source_path, list(entry["recall_modes"]), memory_object, SOURCE_KIND_TEACHING_FIXTURE))

    if errors:
        fail("curated memory object manifest", errors)
    return curated


def corpus_recall_modes(memory_object: JsonDict) -> list[str]:
    return list(CORPUS_RECALL_MODES_BY_KIND[memory_object["kind"]])


def load_corpus_objects(seen_paths: set[str], seen_ids: set[str]) -> list[SourceObject]:
    validator = validator_for("memory_object.schema.json")
    allowed_kinds = shipped_kinds()
    corpus: list[SourceObject] = []
    errors: list[str] = []

    for object_path in sorted(MEMO_OBJECTS.glob("*/*/*/object.json")):
        source_path = object_path.relative_to(ROOT).as_posix()
        if source_path in seen_paths:
            errors.append(f"duplicate corpus source path: {source_path}")
            continue
        seen_paths.add(source_path)
        memory_object = load_json(object_path)
        if not validate_memory_object(
            memory_object=memory_object,
            source_path=source_path,
            validator=validator,
            allowed_kinds=allowed_kinds,
            errors=errors,
        ):
            continue
        object_id = memory_object["id"]
        if object_id in seen_ids:
            errors.append(f"duplicate memory object id across object read-model sources: {object_id}")
            continue
        seen_ids.add(object_id)
        corpus.append((source_path, corpus_recall_modes(memory_object), memory_object, SOURCE_KIND_REVIEWED_CORPUS))

    if errors:
        fail("reviewed memory corpus objects", errors)
    return corpus


def load_source_objects(manifest: JsonDict) -> list[SourceObject]:
    curated = load_curated_objects(manifest)
    seen_paths = {source_path for source_path, _, _, _ in curated}
    seen_ids = {memory_object["id"] for _, _, memory_object, _ in curated}
    return curated + load_corpus_objects(seen_paths, seen_ids)


def validate_internal_object_refs(curated: list[SourceObject]) -> None:
    curated_ids = {memory_object["id"] for _, _, memory_object, _ in curated}
    errors: list[str] = []

    for source_path, _, memory_object, _ in curated:
        for label, refs in object_reference_fields(memory_object):
            for ref in refs:
                if ref not in curated_ids:
                    errors.append(f"{source_path}:{label} references missing curated object id {ref}")

    if errors:
        fail("curated object references", errors)
