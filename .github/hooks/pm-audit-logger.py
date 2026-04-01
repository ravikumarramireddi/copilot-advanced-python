#!/usr/bin/env python3
"""PM Audit Logger: PostToolUse hook for Project Manager agent.

Appends a timestamped entry to .github/pm-audit.log every time the
Project Manager agent produces output. Reads a PostToolUse event from
stdin and logs tool name, timestamp, and output summary.

Log file: .github/pm-audit.log
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path


_LOG_PATH = Path(__file__).parent.parent / "pm-audit.log"


def _truncate(text: str, max_len: int = 100) -> str:
    """Truncate text to max_len chars, adding ellipsis if needed.

    Args:
        text: Text to truncate.
        max_len: Maximum length before truncation.

    Returns:
        Truncated text with ellipsis if longer than max_len.
    """
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def main() -> None:
    """Read a PostToolUse event from stdin and append to audit log."""
    event: dict = json.load(sys.stdin)

    tool_name = event.get("toolName", "unknown")
    tool_output = event.get("toolOutput", "")

    # Extract first line or truncate output for summary
    if isinstance(tool_output, str):
        summary = tool_output.split("\n")[0] if tool_output else "(empty)"
        summary = _truncate(summary)
    else:
        summary = _truncate(str(tool_output))

    timestamp = datetime.now().isoformat()

    log_entry = f"[{timestamp}] {tool_name}: {summary}\n"

    # Append to log file (create if doesn't exist)
    with _LOG_PATH.open("a") as fh:
        fh.write(log_entry)


if __name__ == "__main__":
    main()
