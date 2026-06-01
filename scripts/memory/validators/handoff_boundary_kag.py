"""Inter-agent handoff and export-boundary validation profile."""

from __future__ import annotations

from ._shared import *  # noqa: F403

def load_kag_export_builder():
    module_path = CONSUMER_HANDOFF_KAG_SOURCE_EXPORT_PART / "scripts" / "generate_kag_export.py"
    spec = importlib.util.spec_from_file_location(
        "generate_kag_export",
        module_path,
    )
    if spec is None or spec.loader is None:
        print("[FAIL] mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json")
        print("  - unable to load KAG export generator")
        raise SystemExit(1)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def validate_kag_source_export() -> None:
    builder = load_kag_export_builder()
    kag_export_path = builder.KAG_EXPORT_PATH

    errors: list[str] = []
    expected_payload = builder.build_kag_export_payload()
    if not kag_export_path.exists():
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must exist")
        actual_payload = {}
    else:
        actual_payload = load_json(kag_export_path)

    if actual_payload != expected_payload:
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must match the committed generator-backed payload")

    missing_fields = sorted(KAG_EXPORT_REQUIRED_FIELDS - set(actual_payload))
    if missing_fields:
        errors.append(
            "mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json is missing required fields: "
            + ", ".join(missing_fields)
        )

    append_ref_errors(
        errors,
        [
            ("kag_export.entry_surface.path", actual_payload.get("entry_surface", {}).get("path")),
        ]
        + [
            (f"kag_export.direct_relations[{index}].target_ref", relation.get("target_ref"))
            for index, relation in enumerate(actual_payload.get("direct_relations", []))
            if isinstance(relation, dict)
        ],
    )

    source_inputs = actual_payload.get("source_inputs")
    if not isinstance(source_inputs, list) or len(source_inputs) != 2:
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep exactly two source_inputs")
    else:
        expected_source_inputs = expected_payload["source_inputs"]
        if source_inputs != expected_source_inputs:
            errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep the memo-primary / ToS-supporting source_inputs split")

    if actual_payload.get("section_handles") != expected_payload["section_handles"]:
        errors.append("mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep the canonical bridge section_handles")
    if actual_payload.get("direct_relations") != expected_payload["direct_relations"]:
        errors.append(
            "mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json must keep the source/claim/episode/ToS/provenance direct_relations set"
        )

    kag_root_text = os.environ.get("AOA_KAG_ROOT")
    if kag_root_text:
        kag_root = Path(kag_root_text).expanduser().resolve()
        schema_path = kag_root / "schemas" / "federation-kag-export.schema.json"
        if not schema_path.exists():
            errors.append(
                f"AOA_KAG_ROOT canonical schema path does not exist: {schema_path}"
            )
        else:
            schema = load_json(schema_path)
            validator = Draft202012Validator(schema, format_checker=FORMAT_CHECKER)
            schema_errors = [
                f"{'.'.join(str(part) for part in err.absolute_path) or '<root>'}: {err.message}"
                for err in sorted(
                    validator.iter_errors(actual_payload),
                    key=lambda err: list(err.absolute_path),
                )
            ]
            errors.extend(
                f"AOA_KAG_ROOT federation-kag-export.schema.json -> {message}"
                for message in schema_errors
            )

    if errors:
        print("[FAIL] mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json")
        for err in errors:
            print(f"  - {err}")
        raise SystemExit(1)
    print("[OK]   mechanics/consumer-handoff/parts/kag-source-export/generated/kag_export.min.json")
