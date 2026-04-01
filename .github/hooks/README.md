# Copilot Hooks

This directory contains hook scripts for GitHub Copilot agent customization.

## Global Hooks

### smart-gatekeeper.py (PreToolUse)

Firewall for terminal commands. Classifies commands as allow/ask/deny based on configurable patterns.

- **Event**: PreToolUse
- **Scope**: Global (all agents)
- **Config**: `gatekeeper-config.json`
- **Registration**: `smart-gatekeeper.json`

### auto-lint.py (PostToolUse)

Automatic linting enforcement after file edits. Runs `uv run ruff check --fix` on Python files immediately after any file editing operation.

- **Event**: PostToolUse
- **Scope**: Global (all agents)
- **Triggers**: File edit tools (`create_file`, `replace_string_in_file`, `multi_replace_string_in_file`)
- **Target**: Python files only (*.py)
- **Registration**: `auto-lint.json`
- **Behavior**: Auto-fixes lint issues, reports results via system message, never blocks workflow

## Agent-Scoped Hooks

### pm-audit-logger.py (PostToolUse)

Audit logger for Project Manager agent. Appends timestamped entries to `.github/pm-audit.log` for every tool invocation.

- **Event**: PostToolUse
- **Scope**: Project Manager agent only
- **Output**: `.github/pm-audit.log` (gitignored)
- **Registration**: `.github/agents/project-manager.agent.md` (hooks section in frontmatter)

### Log Format

```
[2026-03-30T14:32:05.123456] read_file: src/weather_app/models.py (lines 1-50)
[2026-03-30T14:32:08.456789] semantic_search: weather service patterns
[2026-03-30T14:32:12.789012] create_file: docs/backlog/P1-feature.md
```

Each entry includes:
- ISO 8601 timestamp
- Tool name
- Truncated summary of tool output (first line or first 100 chars)

---

## Git Hooks (Traditional)

### git-pre-commit (Git Pre-Commit)

Enforces code formatting before git commits. Automatically runs `ruff format` on all staged Python files and re-stages them if formatting changes are made.

- **Event**: Git pre-commit (traditional git hook, not Copilot)
- **Scope**: All git commits in this repository
- **Target**: Staged Python files only (*.py)
- **Script**: `.github/hooks/git-pre-commit`
- **Installed**: `.git/hooks/pre-commit` (symlinked)
- **Behavior**: Formats staged files, re-stages them, blocks commit if formatting fails

#### Installation

The hook is already installed via symlink. To reinstall or set up on a fresh clone:

```bash
ln -sf ../../.github/hooks/git-pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

#### Testing

Try committing a Python file with poor formatting:

```bash
echo "def test( ):    pass" > test_formatting.py
git add test_formatting.py
git commit -m "Test formatting hook"
# Should see: "Running ruff format on staged Python files..."
# File will be auto-formatted and re-staged
```
