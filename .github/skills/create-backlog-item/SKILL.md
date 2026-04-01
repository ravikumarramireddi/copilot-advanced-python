---
name: create-backlog-item
description: 'Create backlog items for the weather app using the canonical template. Use when: creating user stories, adding features to backlog, documenting implementation tasks, writing sprint items, planning development work.'
argument-hint: 'Brief description of the feature or task'
---

# Create Backlog Item

## When to Use

Use this skill when creating backlog items for the weather app project. This ensures all backlog items follow the same structure and include all necessary planning details.

**Trigger phrases:**
- "Add a backlog item for..."
- "Create a user story for..."
- "Write a backlog item about..."
- "Plan a task for..."
- "Document implementation for..."

## Procedure

### 1. Load the Template

Read the [backlog item template](./assets/backlog-item-template.md) to understand the canonical structure.

### 2. Gather Requirements

Collect the following information from the user or conversation context:
- Feature/task description
- Priority level (P0, P1, P2, etc.)
- Target user or persona
- Expected outcome
- Technical scope and complexity

If information is missing, ask clarifying questions before proceeding.

### 3. Fill the Template

Use the template structure exactly as defined. Include:
- **Title** with priority marker
- **User story format** (As a... I want... so that...)
- **Acceptance criteria** as checkboxes
- **TDD requirements** with specific test cases
- **Definition of Done** checklist
- **Effort estimate** (XS, S, M, L, XL)
- **Files likely touched** with descriptions
- **Dependencies** if any
- **Impacted layers** (models, services, routers, tests, etc.)
- **Technical notes** with implementation guidance

### 4. Align with Project Conventions

Ensure the backlog item follows the weather app's architecture:
- **Layered structure**: routers → services → repositories
- **Testing approach**: TDD with unit and integration tests
- **Code standards**: Python 3.12+, type hints, Google-style docstrings
- **Tools**: pytest, ruff, FastAPI conventions

Refer to `.github/copilot-instructions.md` for project-specific conventions.

### 5. Review for Completeness

Before presenting the backlog item, verify:
- [ ] User story is clear and describes value
- [ ] Acceptance criteria are testable and specific
- [ ] TDD requirements cover all acceptance criteria
- [ ] Effort estimate reflects complexity realistically
- [ ] Files list helps developers understand scope
- [ ] Technical notes provide implementation guidance
- [ ] Item can fit in a single PR/development session

## Output Format

Present the completed backlog item using the exact markdown structure from the template. Do not add extra sections or remove required fields.

## Best Practices

**Scope appropriately**: Each item should be completable in one agent session or PR. Break large features into multiple items (e.g., backend API + frontend integration).

**Be specific in tests**: List exact test scenarios, not just "write tests". This helps with TDD implementation.

**Include file paths**: Help developers quickly locate where changes are needed.

**Add technical context**: Include API endpoints, model names, validation rules — any detail that reduces implementation ambiguity.

**Cross-reference**: If the item depends on other work, explicitly state it in the Dependencies section.

## Example Usage

User: "Add a backlog item for implementing weather alerts notification system"

Agent response:
1. Loads backlog-item-template.md
2. Asks clarifying questions about notification mechanism (WebSocket, polling, etc.)
3. Fills template with complete details
4. Returns formatted markdown ready to append to docs/backlog.md
