#!/usr/bin/env python3
"""Auto-Lint Hook: PostToolUse hook that enforces linting after file edits.

Automatically runs 'uv run ruff check --fix' on Python files after any
file editing operation (create_file, replace_string_in_file,
multi_replace_string_in_file). Provides immediate feedback on lint errors
and automatically fixes auto-fixable issues.

Event: PostToolUse
Scope: Global (all agents)
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


# Tools that modify files
_FILE_EDIT_TOOLS = {
    "create_file",
    "replace_string_in_file",
    "multi_replace_string_in_file",
}


def _extract_python_files(tool_name: str, tool_input: dict) -> list[Path]:
    """Extract Python file paths from tool input.

    Args:
        tool_name: Name of the tool that was invoked.
        tool_input: Input parameters passed to the tool.

    Returns:
        List of Path objects for Python files that were edited.
    """
    python_files: list[Path] = []

    if tool_name == "create_file":
        file_path = tool_input.get("filePath", "")
        if file_path.endswith(".py"):
            python_files.append(Path(file_path))

    elif tool_name == "replace_string_in_file":
        file_path = tool_input.get("filePath", "")
        if file_path.endswith(".py"):
            python_files.append(Path(file_path))

    elif tool_name == "multi_replace_string_in_file":
        replacements = tool_input.get("replacements", [])
        for replacement in replacements:
            file_path = replacement.get("filePath", "")
            if file_path.endswith(".py"):
                python_files.append(Path(file_path))

    return python_files


def _run_ruff_check(files: list[Path]) -> tuple[bool, str]:
    """Run ruff check --fix on the specified files.

    Args:
        files: List of Python files to lint.

    Returns:
        Tuple of (success: bool, output: str)
    """
    if not files:
        return True, "No Python files to lint"

    # Convert to strings for subprocess
    file_paths = [str(f) for f in files]

    try:
        result = subprocess.run(
            ["uv", "run", "ruff", "check", "--fix"] + file_paths,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout.strip() or result.stderr.strip()

        if result.returncode == 0:
            if output:
                return True, f"✓ Linted {len(files)} file(s): {output}"
            else:
                return True, f"✓ Linted {len(files)} file(s): All checks passed"
        else:
            return False, f"✗ Lint errors in {len(files)} file(s): {output}"

    except subprocess.TimeoutExpired:
        return False, f"✗ Ruff check timed out on {len(files)} file(s)"
    except FileNotFoundError:
        return False, "✗ uv or ruff not found in PATH"
    except Exception as e:
        return False, f"✗ Lint failed: {str(e)}"


def main() -> None:
    """Read PostToolUse event, lint Python files, and report results."""
    try:
        event: dict = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Not valid JSON; exit silently
        sys.exit(0)

    tool_name = event.get("toolName", "")

    # Only process file edit tools
    if tool_name not in _FILE_EDIT_TOOLS:
        sys.exit(0)

    tool_input = event.get("toolInput", {})
    python_files = _extract_python_files(tool_name, tool_input)

    # No Python files to lint
    if not python_files:
        sys.exit(0)

    # Run ruff check --fix
    success, message = _run_ruff_check(python_files)

    # Output system message to agent
    response = {
        "systemMessage": message,
        "continue": True,
    }

    print(json.dumps(response))

    # Exit 0 (success) even if lint errors found - we don't want to block
    # the agent workflow, just inform about the results
    sys.exit(0)


if __name__ == "__main__":
    main()
