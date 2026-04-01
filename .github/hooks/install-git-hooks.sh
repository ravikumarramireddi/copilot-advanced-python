#!/usr/bin/env bash
# Install all git hooks for this repository
#
# Run this script after cloning the repository to set up git hooks.
# This ensures pre-commit formatting and other git-based automation.

set -e

echo "Installing git hooks..."

# Install pre-commit hook
if [ -f .github/hooks/git-pre-commit ]; then
    ln -sf ../../.github/hooks/git-pre-commit .git/hooks/pre-commit
    chmod +x .git/hooks/pre-commit
    echo "✓ Installed pre-commit hook (ruff format)"
fi

echo ""
echo "Git hooks installed successfully!"
echo ""
echo "Active hooks:"
echo "  - pre-commit: Runs 'ruff format' on staged Python files"
