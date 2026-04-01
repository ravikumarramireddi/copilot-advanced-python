#!/usr/bin/env python3
"""Smart Gatekeeper: PreToolUse firewall for terminal commands.

Reads a PreToolUse event from stdin, classifies the shell command as
allow / ask / deny, and writes a permissionDecision JSON response to stdout.

Policy precedence (first match wins):
  1. deny  — team config deny-list        → hard-blocked, no override
  2. allow — allow-list (config or built-in) → auto-approved, no prompt
  3. ask   — ask-list  (config or built-in) → pause for human approval
  4. None  — everything else               → VS Code default approval flow

Config file: .github/hooks/gatekeeper-config.json
  Provide "allow", "ask", and/or "deny" keys to override the built-in
  defaults for each list.  Omit a key to keep the built-in default.
  The "deny" list is empty by default; add patterns to hard-block commands.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Built-in policy defaults
# ---------------------------------------------------------------------------

_DEFAULT_ALLOW: list[str] = [
    r"^pytest\b",
    r"^uv\s+run\s+pytest\b",
    r"^ls\b",
    r"^cat\b",
    r"^head\b",
    r"^tail\b",
    r"^grep\b",
    r"^find\b",
    r"^wc\b",
]

_DEFAULT_ASK: list[str] = [
    r"\brm\b",
    r"^pip\s+install\b",
    r"^curl\b",
    r"^wget\b",
    r"^git\s+push\b",
    r"^git\s+reset\b",
]

_DECISION_REASONS: dict[str, str] = {
    "allow": "Read-only or test command — auto-approved by Smart Gatekeeper.",
    "ask": "Destructive, network-reaching, or irreversible — human approval required.",
    "deny": "Command blocked by team policy (gatekeeper-config.json).",
}

_CONFIG_PATH = Path(__file__).parent / "gatekeeper-config.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_config() -> dict:
    """Load team policy overrides from gatekeeper-config.json.

    Returns:
        Parsed policy dict, or empty dict if the config file is absent.
    """
    if _CONFIG_PATH.exists():
        with _CONFIG_PATH.open() as fh:
            return json.load(fh)
    return {}


def _match_any(command: str, patterns: list[str]) -> bool:
    """Return True if command matches at least one pattern (case-insensitive).

    Args:
        command: Shell command string to test.
        patterns: List of Python regex patterns.

    Returns:
        True if any pattern matches, False otherwise.
    """
    return any(re.search(p, command, re.IGNORECASE) for p in patterns)


def _classify(command: str, config: dict) -> str | None:
    """Classify a command as allow / ask / deny / None (pass-through).

    Resolution order:
      1. deny-list from config (hard-block)
      2. allow-list from config, else built-in _DEFAULT_ALLOW
      3. ask-list  from config, else built-in _DEFAULT_ASK
      4. None → pass through to VS Code default approval flow

    Args:
        command: Shell command string to classify.
        config: Parsed team policy dict (may be empty).

    Returns:
        "allow", "ask", "deny", or None for pass-through.
    """
    deny_patterns: list[str] = config.get("deny", [])
    allow_patterns: list[str] = config.get("allow", _DEFAULT_ALLOW)
    ask_patterns: list[str] = config.get("ask", _DEFAULT_ASK)

    if _match_any(command, deny_patterns):
        return "deny"
    if _match_any(command, allow_patterns):
        return "allow"
    if _match_any(command, ask_patterns):
        return "ask"
    return None


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Read a PreToolUse event from stdin and emit a permissionDecision."""
    event: dict = json.load(sys.stdin)

    # Only gate run_in_terminal calls; let all other tools pass through.
    if event.get("toolName") != "run_in_terminal":
        sys.exit(0)

    command: str = event.get("toolInput", {}).get("command", "").strip()
    if not command:
        sys.exit(0)

    config = _load_config()
    decision = _classify(command, config)

    if decision is None:
        # No opinion — let VS Code's default approval flow handle it.
        sys.exit(0)

    response = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": _DECISION_REASONS[decision],
        }
    }
    print(json.dumps(response))


if __name__ == "__main__":
    main()
