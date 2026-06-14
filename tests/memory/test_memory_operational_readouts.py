from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_MEMORY_DIR = REPO_ROOT / "scripts" / "memory"
if str(SCRIPTS_MEMORY_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_MEMORY_DIR))

import build_memory_operational_readouts as operational_readouts
import memory_operational_access


def readout_payload(name: str, marker: str) -> dict[str, object]:
    return {
        "schema_version": f"aoa_memo_{name}_v1",
        "surface_kind": f"memo_{name}_readout",
        "owner_repo": "aoa-memo",
        "generated_by": "scripts/memory/build_memory_operational_readouts.py",
        "source_refs": ["repo:aoa-memo"],
        "source_owner_split": {"memo_owner": "aoa-memo"},
        "summary": {"marker": marker},
    }


def test_run_mcp_cli_reports_missing_checkout(monkeypatch, tmp_path: Path) -> None:
    missing_mcp_root = tmp_path / "missing-aoa-memo-mcp"
    monkeypatch.setattr(memory_operational_access, "MCP_ROOT", missing_mcp_root)

    result = memory_operational_access.run_mcp_cli(["brief", "--repo", "aoa-evals"])

    assert result["ok"] is False
    assert "MCP checkout unavailable" in result["error"]
    assert str(missing_mcp_root) not in result["error"]


def test_run_mcp_cli_reports_timeout(monkeypatch, tmp_path: Path) -> None:
    mcp_root = tmp_path / "aoa-memo-mcp"
    mcp_root.mkdir()
    monkeypatch.setattr(memory_operational_access, "MCP_ROOT", mcp_root)

    def fake_run(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        raise subprocess.TimeoutExpired(cmd="aoa_memo_mcp.cli", timeout=1)

    monkeypatch.setattr(memory_operational_access.subprocess, "run", fake_run)

    result = memory_operational_access.run_mcp_cli(["search", "memory"], timeout=1)

    assert result["ok"] is False
    assert "timed out after 1s" in result["error"]


def test_live_access_readout_records_missing_checkout_probe_failures(
    monkeypatch, tmp_path: Path
) -> None:
    missing_mcp_root = tmp_path / "missing-aoa-memo-mcp"
    monkeypatch.setattr(memory_operational_access, "MCP_ROOT", missing_mcp_root)

    payload = memory_operational_access.build_access_plane_currentness(live=True)

    assert payload["summary"]["overall_status"] == "failed"
    failed_probes = [
        probe for probe in payload["probes"] if probe["status"] == "failed"
    ]
    assert failed_probes
    assert any(probe["name"] == "brief:aoa-evals" for probe in failed_probes)
    assert str(missing_mcp_root) not in json.dumps(payload)


def test_non_live_check_rejects_stale_access_readout(
    monkeypatch, tmp_path: Path, capsys
) -> None:
    output_dir = tmp_path / "generated" / "memory"
    output_dir.mkdir(parents=True)
    access_output = output_dir / "access_plane_currentness.min.json"
    source_wave_output = output_dir / "source_intake_wave.min.json"
    port_status_output = output_dir / "workspace_memo_port_status.min.json"

    monkeypatch.setattr(operational_readouts, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(operational_readouts, "ACCESS_OUTPUT", access_output)
    monkeypatch.setattr(operational_readouts, "SOURCE_WAVE_OUTPUT", source_wave_output)
    monkeypatch.setattr(operational_readouts, "PORT_STATUS_OUTPUT", port_status_output)

    checked_in_access = readout_payload("access", "checked-in")
    expected_access = readout_payload("access", "expected")
    source_wave = readout_payload("source-wave", "current")
    port_status = readout_payload("port-status", "current")

    access_output.write_text(
        operational_readouts.render_json(checked_in_access), encoding="utf-8"
    )
    source_wave_output.write_text(
        operational_readouts.render_json(source_wave), encoding="utf-8"
    )
    port_status_output.write_text(
        operational_readouts.render_json(port_status), encoding="utf-8"
    )

    exit_code = operational_readouts.check_outputs(
        {
            access_output: expected_access,
            source_wave_output: source_wave,
            port_status_output: port_status,
        },
        live=False,
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "access_plane_currentness.min.json is stale" in captured.err
