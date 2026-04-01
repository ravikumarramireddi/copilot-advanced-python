# Backlog Item Template

Use this template for all backlog items in the weather app project.

---

## [PRIORITY] Title of Feature/Task

**As a** [user type/persona], **I want** [feature/capability] **so that** [business value/outcome].

**Acceptance Criteria:**
- [ ] Criterion 1: Specific, testable outcome
- [ ] Criterion 2: Another testable outcome
- [ ] Criterion 3: Additional requirement
- [ ] [Add more as needed]

**TDD Requirements:**
- [ ] Unit test: [Component/method name] with [test scenario]
  - Test case 1: Expected behavior
  - Test case 2: Error handling
  - Test case 3: Edge case
- [ ] Unit test: [Another component] with [test scenario]
  - Test case 1: Expected behavior
  - Test case 2: Error handling
- [ ] Integration test: [Endpoint or feature] 
  - Test case 1: Happy path scenario
  - Test case 2: Error response scenario
  - Test case 3: Validation scenario
- Tests must be written first and fail before implementation begins

**Definition of Done:**
- [ ] All acceptance criteria met
- [ ] All TDD requirements implemented and passing (`uv run pytest`)
- [ ] No new lint violations (`uv run ruff check src/ tests/`)
- [ ] No source files modified without a corresponding test change
- [ ] API documented with examples in docstrings (if applicable)
- [ ] Can be tested [manually/via API/with curl] without [dependent work]

**Effort Estimate:** [XS | S | M | L | XL]

**Files likely touched:**
- `path/to/file1.py` — Description of changes
- `path/to/file2.py` — Description of changes
- `path/to/test_file.py` — Test coverage
- [Add more as needed]

**Dependencies:** [None | List of prerequisite work]

**Impacted layers:**
- Models: [Description of changes or "None"]
- Services: [Description of changes or "None"]
- Routers: [Description of changes or "None"]
- Repositories: [Description of changes or "None"]
- Tests: [Description of test coverage]
- Frontend: [Description of UI changes or "None"]

**Technical Notes:**
- [Implementation guidance, API details, validation rules, etc.]
- [External API endpoints or documentation links]
- [Specific patterns or conventions to follow]
- [Performance considerations or constraints]

---

## Template Usage Guidelines

### Priority Levels
- **P0**: Critical, blocks other work
- **P1**: High priority, major feature or fix
- **P2**: Medium priority, improvement or enhancement
- **P3**: Low priority, nice-to-have

### Effort Estimates
- **XS**: <2 hours, trivial change
- **S**: 2-4 hours, small focused task
- **M**: 4-8 hours, medium complexity
- **L**: 1-2 days, significant feature
- **XL**: 2+ days, should be broken down into smaller items

### Writing Acceptance Criteria
- Start with action verb (Returns, Displays, Validates, etc.)
- Be specific and measurable
- Focus on user-facing behavior, not implementation
- Each criterion should be independently testable

### TDD Requirements Structure
- Group by test type (unit, integration)
- Name the component/method being tested
- List specific test scenarios as sub-bullets
- Include happy path, error cases, and edge cases
- Mention the testing approach (mocked dependencies, etc.)

### Definition of Done Checklist
Standard items that apply to all backlog items:
- Acceptance criteria completion
- Test coverage (pytest passing)
- Code quality (ruff checks)
- Documentation updates
- Independent verification possible

### Files Likely Touched
- List actual file paths relative to project root
- Add brief description of what changes in each file
- Include both source and test files
- Helps developers estimate scope quickly

### Dependencies
- List other backlog items that must be completed first
- Reference by title or ID if available
- State "None" explicitly if no dependencies exist

### Impacted Layers
Follows the weather app architecture:
- **Models**: Pydantic models in `models.py`
- **Services**: Business logic in `services/`
- **Routers**: HTTP endpoints in `routers/`
- **Repositories**: Data access in `repositories/`
- **Tests**: Coverage in `tests/unit/` and `tests/integration/`
- **Frontend**: UI changes in `static/`

### Technical Notes
- API endpoint URLs and HTTP methods
- Model field names and validation rules
- External API integration details
- Performance targets or constraints
- Security considerations
- Error handling approach
- Any non-obvious implementation detail that reduces ambiguity
