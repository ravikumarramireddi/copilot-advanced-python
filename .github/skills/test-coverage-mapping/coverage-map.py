#!/usr/bin/env python3
"""Deterministic coverage-map script.

Walks src/weather_app/ and tests/ to map source files to their expected
test counterparts, outputting valid JSON to stdout with keys:
``mapped``, ``gaps``, and ``summary``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

DENY_NAMES = {"__init__.py", "main.py"}
DENY_SEGMENTS = {"static", "__pycache__"}


def _is_testable(path: Path) -> bool:
    """Return True if the source file should have a corresponding test."""
    if path.name in DENY_NAMES:
        return False
    if DENY_SEGMENTS & set(part for part in path.parts):
        return False
    return True


def _discover_source_files(src_dir: Path) -> list[Path]:
    """Return sorted list of testable .py files under src_dir."""
    return sorted(p for p in src_dir.rglob("*.py") if _is_testable(p))


def _discover_test_files(test_dirs: list[Path]) -> set[str]:
    """Return set of relative test file paths (as strings) that exist."""
    files: set[str] = set()
    for d in test_dirs:
        if d.exists():
            for p in d.rglob("*.py"):
                if p.name.startswith("test_"):
                    files.add(str(p))
    return files


def _expected_test(source: Path, repo_root: Path) -> tuple[str, str]:
    """Return (expected_test_path, type) for a source file.

    Naming conventions:
    - routers/{feature}.py  -> tests/integration/test_{feature}_api.py (integration)
    - {layer}/{module}.py   -> tests/unit/test_{module}.py             (unit)
    - {module}.py           -> tests/unit/test_{module}.py             (unit)
    """
    rel = source.relative_to(repo_root / "src" / "weather_app")
    module = source.stem

    if len(rel.parts) >= 2 and rel.parts[0] == "routers":
        test_path = repo_root / "tests" / "integration" / f"test_{module}_api.py"
        return str(test_path), "integration"

    test_path = repo_root / "tests" / "unit" / f"test_{module}.py"
    return str(test_path), "unit"


def build_coverage_map(repo_root: Path) -> dict:
    """Build the coverage map data structure."""
    src_dir = repo_root / "src" / "weather_app"
    test_dirs = [repo_root / "tests" / "unit", repo_root / "tests" / "integration"]

    source_files = _discover_source_files(src_dir)
    existing_tests = _discover_test_files(test_dirs)

    mapped: list[dict[str, str]] = []
    gaps: list[dict[str, str]] = []

    for src in source_files:
        rel_src = str(src.relative_to(repo_root))
        expected_test, test_type = _expected_test(src, repo_root)

        if expected_test in existing_tests:
            mapped.append(
                {
                    "source": rel_src,
                    "test": str(Path(expected_test).relative_to(repo_root)),
                    "type": test_type,
                }
            )
        else:
            gaps.append(
                {
                    "source": rel_src,
                    "expected_test": str(Path(expected_test).relative_to(repo_root)),
                }
            )

    return {
        "mapped": mapped,
        "gaps": gaps,
        "summary": {
            "total_source_files": len(source_files),
            "covered": len(mapped),
            "gaps": len(gaps),
        },
    }


def main() -> None:
    """Entry point: resolve repo root, build map, print JSON."""
    repo_root = Path.cwd()
    data = build_coverage_map(repo_root)
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
