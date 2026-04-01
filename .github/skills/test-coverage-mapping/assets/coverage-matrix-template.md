# Coverage Matrix Template

Use this template to present test coverage mapping results in a clear, structured format.

## Full Coverage Matrix

```markdown
# Test Coverage Matrix

**Generated**: {DATE}
**Project**: {PROJECT_NAME}
**Source Root**: {SOURCE_ROOT}
**Test Root**: {TEST_ROOT}

---

## Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| Total Source Files | {TOTAL} | 100% |
| ✅ Fully Covered | {FULL} | {FULL_PCT}% |
| ⚠️ Partially Covered | {PARTIAL} | {PARTIAL_PCT}% |
| ❌ Not Covered | {NONE} | {NONE_PCT}% |

---

## Coverage by Layer

| Layer | Total | Covered | Coverage % | Priority |
|-------|-------|---------|------------|----------|
| Routers | {R_TOTAL} | {R_COVERED} | {R_PCT}% | P0 |
| Services | {S_TOTAL} | {S_COVERED} | {S_PCT}% | P0 |
| Repositories | {RP_TOTAL} | {RP_COVERED} | {RP_PCT}% | P0 |
| Utils | {U_TOTAL} | {U_COVERED} | {U_PCT}% | P1 |
| Models | {M_TOTAL} | {M_COVERED} | {M_PCT}% | P1 |
| Config | {C_TOTAL} | {C_COVERED} | {C_PCT}% | P2 |

---

## Detailed Mapping

### ✅ Fully Covered

Files with comprehensive test coverage (both unit and integration where appropriate):

| Source File | Test File(s) | Test Count | Last Updated |
|-------------|--------------|------------|--------------|
| `{source_path}` | `{test_path}` | {count} tests | {date} |

### ⚠️ Partially Covered

Files with some tests but missing expected coverage:

| Source File | Existing Tests | Missing Coverage | Priority |
|-------------|----------------|------------------|----------|
| `{source_path}` | `{test_path}` | {gap_description} | {priority} |

**Example:**
| Source File | Existing Tests | Missing Coverage | Priority |
|-------------|----------------|------------------|----------|
| `routers/weather.py` | `integration/test_weather_api.py` | No unit tests for validation logic | P1 |
| `services/weather_service.py` | `unit/test_weather_service.py` (3 tests) | Missing error condition tests | P0 |

### ❌ Not Covered

Files with no test coverage:

#### P0 - Critical (Must Fix)

| Source File | Layer | Suggested Test File | Test Type | Reason |
|-------------|-------|---------------------|-----------|--------|
| `{source_path}` | {layer} | `{suggested_test}` | {type} | {reason} |

**Example:**
| Source File | Layer | Suggested Test File | Test Type | Reason |
|-------------|-------|---------------------|-----------|--------|
| `services/openweathermap.py` | Services | `tests/unit/test_openweathermap.py` | Unit | External API client with complex error handling |
| `services/geocoding.py` | Services | `tests/unit/test_geocoding.py` | Unit | Coordinate parsing and validation logic |

#### P1 - Important (Should Add)

| Source File | Layer | Suggested Test File | Test Type | Reason |
|-------------|-------|---------------------|-----------|--------|
| `{source_path}` | {layer} | `{suggested_test}` | {type} | {reason} |

#### P2 - Optional (Nice to Have)

| Source File | Layer | Suggested Test File | Test Type | Reason |
|-------------|-------|---------------------|-----------|--------|
| `{source_path}` | {layer} | `{suggested_test}` | {type} | {reason} |

---

## Test Files Without Clear Source Mapping

Identify test files that don't map to a specific source module (fixtures, factories, helpers):

| Test File | Purpose | Status |
|-----------|---------|--------|
| `tests/conftest.py` | Shared fixtures | ✅ Expected |
| `tests/factories.py` | Test data builders | ✅ Expected |
| `tests/unit/conftest.py` | Unit test fixtures | ✅ Expected |
| `tests/integration/conftest.py` | Integration fixtures | ✅ Expected |

---

## Recommendations

### Immediate Actions (P0 - Critical Gaps)

1. **Create `{test_file}`**
   - **Covers**: `{source_file}`
   - **Focus**: {what_to_test}
   - **Effort**: {effort_estimate}

2. **Create `{test_file}`**
   - **Covers**: `{source_file}`
   - **Focus**: {what_to_test}
   - **Effort**: {effort_estimate}

### Short-term Actions (P1 - Important Gaps)

1. {recommendation}
2. {recommendation}

### Long-term Improvements

1. {recommendation}
2. {recommendation}

---

## Coverage Trends

*(Optional - if previous analysis exists)*

| Date | Total Coverage | P0 Gaps | P1 Gaps |
|------|----------------|---------|---------|
| {date_1} | {pct_1}% | {p0_1} | {p1_1} |
| {date_2} | {pct_2}% | {p0_2} | {p1_2} |

---

## Notes

- Test counts reflect number of test functions, not assertions
- "Last Updated" based on file modification timestamp
- Priority levels defined in [mapping conventions](../references/mapping-conventions.md)
- Integration tests verify API contracts; unit tests verify business logic
```

---

## Quick Summary Template

For brief coverage requests, use this condensed format:

```markdown
## Test Coverage Summary

**Coverage**: {COVERED}/{TOTAL} files ({PCT}%)

### ❌ Missing Tests (Priority Order)

**P0 - Critical:**
- `{file_1}` - {reason}
- `{file_2}` - {reason}

**P1 - Important:**
- `{file_3}` - {reason}

### ✅ Well Covered
- `{file_a}` → `{test_a}` ({count} tests)
- `{file_b}` → `{test_b}` ({count} tests)

### Next Steps
1. {action_1}
2. {action_2}
```

---

## Layer-Focused Template

When analyzing a specific layer (e.g., "services only"):

```markdown
## {LAYER} Layer Coverage Analysis

**Total files in {layer}**: {TOTAL}
**Tested**: {COVERED} ({PCT}%)

| Source File | Test File | Status | Test Count |
|-------------|-----------|--------|------------|
| `{file_1}` | `{test_1}` | ✅ | {count} |
| `{file_2}` | `{test_2}` | ⚠️ | {count} |
| `{file_3}` | - | ❌ | 0 |

### Gaps in {LAYER}

**Critical:**
- `{uncovered_file}` needs `{suggested_test}` - {reason}

**Recommendations:**
1. {specific_action}
2. {specific_action}
```

---

## Usage Notes

- Replace `{PLACEHOLDERS}` with actual analysis data
- Choose template based on user request scope (full, quick, or layer-focused)
- Include actual file paths, not just placeholders
- Use emoji indicators (✅⚠️❌) for visual clarity
- Link to source files when showing results in VS Code chat
- Include test count to indicate coverage depth
- Prioritize actionability: what specifically should be created or improved
