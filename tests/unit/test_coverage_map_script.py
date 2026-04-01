"""Tests for the coverage-map.py tooling script."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = (
    REPO_ROOT / ".github" / "skills" / "test-coverage-mapping" / "coverage-map.py"
)


def _run_script() -> subprocess.CompletedProcess[str]:
    """Run coverage-map.py from the repo root and return the result."""
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


class TestCoverageMapScript:
    """Verify coverage-map.py output meets acceptance criteria."""

    def test_script_exits_zero(self) -> None:
        result = _run_script()
        assert result.returncode == 0, f"Script failed: {result.stderr}"

    def test_output_is_valid_json(self) -> None:
        result = _run_script()
        data = json.loads(result.stdout)
        assert isinstance(data, dict)

    def test_output_contains_required_top_level_keys(self) -> None:
        result = _run_script()
        data = json.loads(result.stdout)

        assert "mapped" in data
        assert "gaps" in data
        assert "summary" in data

    def test_summary_counts_are_consistent(self) -> None:
        result = _run_script()
        data = json.loads(result.stdout)
        summary = data["summary"]

        assert summary["covered"] + summary["gaps"] == summary["total_source_files"]

    def test_summary_total_matches_testable_source_files(self) -> None:
        """total_source_files should match the count of testable .py files."""
        result = _run_script()
        data = json.loads(result.stdout)

        # Count testable files the same way the script should
        deny_names = {"__init__.py", "main.py"}
        deny_segments = {"static", "__pycache__"}
        src_dir = REPO_ROOT / "src" / "weather_app"
        expected = 0
        for p in src_dir.rglob("*.py"):
            if p.name in deny_names:
                continue
            if deny_segments & set(p.parts):
                continue
            expected += 1

        assert data["summary"]["total_source_files"] == expected

    def test_covered_modules_appear_in_mapped(self) -> None:
        """Modules that have corresponding test files must be in mapped."""
        result = _run_script()
        data = json.loads(result.stdout)

        mapped_sources = {entry["source"] for entry in data["mapped"]}

        known_covered = [
            "src/weather_app/utils/converters.py",
            "src/weather_app/repositories/location_repo.py",
            "src/weather_app/models.py",
            "src/weather_app/services/weather_service.py",
        ]
        for src in known_covered:
            assert src in mapped_sources, f"{src} should be in mapped"

    def test_uncovered_modules_appear_in_gaps(self) -> None:
        """Modules without test files must be in gaps."""
        result = _run_script()
        data = json.loads(result.stdout)

        gap_sources = {entry["source"] for entry in data["gaps"]}

        known_gaps = [
            "src/weather_app/config.py",
            "src/weather_app/dependencies.py",
            "src/weather_app/services/exceptions.py",
        ]
        for src in known_gaps:
            assert src in gap_sources, f"{src} should be in gaps"

    def test_mapped_entries_have_required_fields(self) -> None:
        result = _run_script()
        data = json.loads(result.stdout)

        for entry in data["mapped"]:
            assert "source" in entry
            assert "test" in entry
            assert "type" in entry
            assert entry["type"] in ("unit", "integration")

    def test_gap_entries_have_required_fields(self) -> None:
        result = _run_script()
        data = json.loads(result.stdout)

        for entry in data["gaps"]:
            assert "source" in entry
            assert "expected_test" in entry

    def test_router_files_mapped_as_integration(self) -> None:
        """Router source files should be mapped to integration tests."""
        result = _run_script()
        data = json.loads(result.stdout)

        for entry in data["mapped"]:
            if "routers/" in entry["source"]:
                assert entry["type"] == "integration"
