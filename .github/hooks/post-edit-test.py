#!/usr/bin/env python3
"""Post-Edit Test Hook: PostToolUse hook that runs the test suite after file edits.

Runs 'uv run pytest --tb=short -q' after any file editing operation and
injects the results as additional context so the Implementer agent can
react to failures immediately — without waiting for an explicit test run.

Event: PostToolUse
Scope: Agent-scoped (Implementer only, via implementer.agent.md frontmatter)
"""

from __future__ import annotations

import json
import subprocess
import sys

# Tools that modify files
_FILE_EDIT_TOOLS = {
    "create_file",
    "replace_string_in_file",
    "multi_replace_string_in_file",
}


def _run_pytest(cwd: str) -> tuple[bool, str]:
    """Run the full pytest suite and capture output.

    Args:
        cwd: Working directory to run pytest in.

    Returns:
        Tuple of (passed: bool, output: str).
    """
    try:
        result = subprocess.run(
            ["uv", "run", "pytest", "--tb=short", "-q"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=cwd,
        )

        output = (result.stdout + result.stderr).strip()
        passed = result.returncode == 0
        return passed, output

    except subprocess.TimeoutExpired:
        return False, "pytest timed out after 120 seconds"
    except FileNotFoundError:
        return False, "uv not found in PATH — cannot run pytest"
    except Exception as e:
        return False, f"pytest runner error: {e}"


def main() -> None:
    """Read PostToolUse event, run tests, and inject results as context."""
    try:
        event: dict = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = event.get("toolName", "")

    # Only trigger on file edit operations
    if tool_name not in _FILE_EDIT_TOOLS:
        sys.exit(0)

    cwd = event.get("cwd", ".")
    passed, output = _run_pytest(cwd)

    status = "✓ All tests passed" if passed else "✗ Tests failed"
    summary = f"{status} after editing files.\n\n```\n{output}\n```"

    response = {
        # Visible banner in the chat UI
        "systemMessage": status,
        # Full output injected into the agent's context window
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": summary,
        },
        # Never block — the TDD approval gate is the user's job, not this hook
        "continue": True,
    }

    print(json.dumps(response))
    sys.exit(0)


if __name__ == "__main__":
    main()
