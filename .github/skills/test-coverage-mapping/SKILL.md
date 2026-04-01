---
name: test-coverage-mapping
description: 'Map test files to source files and identify coverage gaps. Use when: analyzing test coverage, finding untested code, discovering missing tests, auditing test completeness, identifying coverage gaps, planning test work.'
argument-hint: 'Optional: specific module or layer to analyze (e.g., "services" or "routers")'
---

# Test Coverage Mapping

## When to Use

Use this skill to analyze which source files have corresponding tests and identify coverage gaps.

**Trigger phrases:**
- "What files aren't tested?"
- "Map tests to source files"
- "Find coverage gaps"
- "Which source files need tests?"
- "Analyze test coverage"
- "Show me untested code"
- "Identify missing test files"

## Procedure

### 1. Understand the Mapping Convention

Load the [test-source mapping reference](./references/mapping-conventions.md) to understand how test files map to source files in this project.

**Quick reference for this project:**
- Unit tests: `tests/unit/test_{module}.py` → `src/weather_app/{layer}/{module}.py`
- Integration tests: `tests/integration/test_{feature}_api.py` → `src/weather_app/routers/{feature}.py`

### 2. Run the Coverage-Map Script

Run `python3 .github/skills/test-coverage-mapping/coverage-map.py` from the repo root and capture the JSON output. Use the `mapped`, `gaps`, and `summary` fields to proceed — do not scan files manually.

### 4. Build the Mapping Matrix

Create a mapping between source files and test files following the [matrix template](./assets/coverage-matrix-template.md).

For each source file, identify:
- ✅ **Fully covered**: Has both unit and integration tests where appropriate
- ⚠️ **Partially covered**: Has some tests but missing unit or integration coverage
- ❌ **Not covered**: No corresponding test file exists

### 5. Analyze Coverage Depth

For files that have tests, optionally analyze whether coverage is comprehensive:

1. Read the source file to identify:
   - Number of functions/classes
   - Key business logic paths
   - Error conditions

2. Read the corresponding test file to count:
   - Number of test cases
   - Scenarios covered
   - Edge cases tested

3. Flag potential gaps where test cases seem sparse relative to complexity.

### 6. Categorize Gaps by Priority

Sort uncovered or under-tested files by priority:

**P0 - Critical gaps:**
- Services with business logic
- Routers handling API contracts
- Repository layer with data operations

**P1 - Important gaps:**
- Utility functions used across the app
- Model validation logic
- Configuration handling

**P2 - Nice to have:**
- Simple wrappers
- Initialization files (`__init__.py`)
- Static content

### 7. Generate Actionable Report

Present findings in a structured format:

```markdown
## Test Coverage Analysis

### Coverage Summary
- Total source files: X
- Fully tested: Y (Z%)
- Partially tested: A (B%)
- Untested: C (D%)

### Coverage Details

#### ✅ Fully Covered
- `src/weather_app/utils/converters.py` → `tests/unit/test_converters.py`
- `src/weather_app/services/weather_service.py` → `tests/unit/test_weather_service.py`

#### ⚠️ Partially Covered
- `src/weather_app/routers/weather.py` → `tests/integration/test_weather_api.py` (missing unit tests)

#### ❌ Not Covered (Priority Order)
**P0 - Critical:**
- `src/weather_app/services/openweathermap.py` - External API client, needs unit tests

**P1 - Important:**
- `src/weather_app/models.py` - Model validation needs testing
- `src/weather_app/dependencies.py` - Dependency injection logic

**P2 - Nice to have:**
- `src/weather_app/config.py` - Settings configuration
- `src/weather_app/main.py` - App initialization

### Recommendations
1. Create `tests/unit/test_openweathermap.py` to test API client
2. Add model validation tests to `tests/unit/test_models.py`
3. Consider integration tests for dependency injection
```

### 8. Suggest Next Actions

Based on the analysis, recommend specific test files to create with brief descriptions of what they should cover.

## Configuration

The skill looks for the following project patterns:
- **Source root**: `src/weather_app/`
- **Test root**: `tests/`
- **Test subdirectories**: `unit/`, `integration/`
- **Naming pattern**: `test_{module}.py` for source module

These can be customized in the [mapping conventions reference](./references/mapping-conventions.md).

## Best Practices

**Start broad, then narrow**: If user specifies a layer (e.g., "services"), focus only on that subset. Otherwise, analyze the entire codebase.

**Consider test types**: Different layers need different test strategies. Routers need integration tests, services need unit tests, utilities need both.

**Use actual file reads sparingly**: Build the initial mapping from file searches. Only read file contents when analyzing coverage depth.

**Prioritize by risk**: Business logic layers (services, repositories) are higher priority than configuration or initialization files.

**Check test markers**: Verify tests are properly marked as `@pytest.mark.unit` or `@pytest.mark.integration` per project conventions.

## Tool Usage Optimization

1. **Parallel file discovery**: Use file_search for source and test files simultaneously
2. **Batch reads**: If analyzing depth, read multiple files in parallel
3. **Pattern matching**: Use glob patterns to quickly identify test/source pairs
4. **Semantic search**: If mapping patterns are unclear, use semantic search to find examples

## Example Usage

**User:** "What files in the services layer aren't tested?"

**Agent response:**
1. Load mapping conventions
2. Search for `src/weather_app/services/*.py`
3. Search for `tests/unit/test_*.py` and `tests/integration/test_*.py`
4. Build mapping for services layer only
5. Report that `openweathermap.py` lacks unit tests
6. Suggest creating `tests/unit/test_openweathermap.py` with specific test scenarios

**User:** "Find all coverage gaps"

**Agent response:**
1. Load mapping conventions
2. Discover all source files across all layers
3. Discover all test files
4. Build complete coverage matrix
5. Categorize gaps by priority
6. Generate full coverage report with recommendations
