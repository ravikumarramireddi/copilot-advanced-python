# Coverage Analysis Workflow

This document provides a step-by-step procedural workflow for efficiently discovering and mapping test coverage using VS Code Copilot tools.

## Phase 1: Discovery

### Step 1.1: Discover Source Files

Use parallel file searches to gather all source files:

```
file_search: "src/**/*.py"
```

**Filter out:**
- `__init__.py` files (usually no logic)
- `__pycache__/` directories
- `static/` directory (frontend assets)

**Expected output:**
```
src/weather_app/config.py
src/weather_app/dependencies.py
src/weather_app/main.py
src/weather_app/models.py
src/weather_app/routers/locations.py
src/weather_app/routers/weather.py
src/weather_app/services/exceptions.py
src/weather_app/services/openweathermap.py
src/weather_app/services/weather_service.py
src/weather_app/repositories/location_repo.py
src/weather_app/utils/converters.py
```

### Step 1.2: Discover Test Files

Simultaneously search for test files:

```
file_search: "tests/**/*.py"
```

**Filter out:**
- `__init__.py` files
- `__pycache__/` directories
- Keep `conftest.py` and `factories.py` but flag as "support files"

**Expected output:**
```
tests/conftest.py          [support]
tests/factories.py         [support]
tests/unit/conftest.py     [support]
tests/unit/test_converters.py
tests/unit/test_location_repo.py
tests/unit/test_models.py
tests/unit/test_weather_service.py
tests/integration/conftest.py    [support]
tests/integration/test_locations_api.py
tests/integration/test_weather_api.py
```

### Step 1.3: Categorize Source Files by Layer

Group source files by architectural layer:

| Layer | Pattern | Priority |
|-------|---------|----------|
| Routers | `src/weather_app/routers/*.py` | P0 |
| Services | `src/weather_app/services/*.py` (exclude exceptions.py) | P0 |
| Repositories | `src/weather_app/repositories/*.py` | P0 |
| Utils | `src/weather_app/utils/*.py` | P1 |
| Models | `src/weather_app/models.py` | P1 |
| Dependencies | `src/weather_app/dependencies.py` | P1 |
| Config | `src/weather_app/config.py` | P2 |
| Main | `src/weather_app/main.py` | P2 |
| Exceptions | `src/weather_app/services/exceptions.py` | P2 |

## Phase 2: Mapping

### Step 2.1: Apply Naming Conventions

For each source file, derive the expected test file path:

**Unit test pattern:**
```
src/weather_app/{layer}/{module}.py → tests/unit/test_{module}.py
src/weather_app/{module}.py → tests/unit/test_{module}.py
```

**Integration test pattern:**
```
src/weather_app/routers/{feature}.py → tests/integration/test_{feature}_api.py
```

**Example mappings:**
```
src/weather_app/utils/converters.py 
  → EXPECT: tests/unit/test_converters.py

src/weather_app/services/weather_service.py 
  → EXPECT: tests/unit/test_weather_service.py

src/weather_app/routers/locations.py 
  → EXPECT: tests/integration/test_locations_api.py
  → OPTIONAL: tests/unit/test_locations_router.py (if complex logic)
```

### Step 2.2: Check for Test File Existence

For each expected test file, check if it exists in the discovered test files list:

| Source | Expected Test | Exists? | Status |
|--------|---------------|---------|--------|
| `services/weather_service.py` | `unit/test_weather_service.py` | ✅ Yes | Covered |
| `services/openweathermap.py` | `unit/test_openweathermap.py` | ❌ No | **GAP** |
| `routers/locations.py` | `integration/test_locations_api.py` | ✅ Yes | Covered |

### Step 2.3: Handle Special Cases

**Routers**: May need both unit and integration tests
- Integration (required): Test API contracts via TestClient
- Unit (optional): Test complex validation or business logic in router

**Exceptions**: Usually don't need tests (just class definitions)

**Main/Config**: Often tested indirectly through integration tests

## Phase 3: Depth Analysis (Optional)

If the user wants to know coverage depth, not just presence/absence:

### Step 3.1: Count Test Functions

For each test file that exists, use `grep_search` to count test functions:

```
grep_search: 
  query: "^def test_|^async def test_"
  isRegexp: true
  includePattern: "tests/unit/test_weather_service.py"
```

**Example output:**
```
tests/unit/test_weather_service.py:
  Line 15: def test_get_current_weather_valid_coordinates_returns_weather
  Line 28: def test_get_current_weather_api_error_raises_exception
  Line 41: async def test_get_forecast_converts_to_fahrenheit
  ... (12 matches total)
```

**Result**: `test_weather_service.py` has 12 test functions

### Step 3.2: Read Source File for Complexity Estimate

Optionally read the source file to understand its complexity:

```
grep_search:
  query: "^def |^async def |^class "
  isRegexp: true
  includePattern: "src/weather_app/services/weather_service.py"
```

**Example output:**
```
Line 10: class WeatherService:
Line 20:     async def get_current_weather(
Line 35:     async def get_forecast(
Line 50:     def _convert_units(
Line 65:     def _evaluate_alerts(
```

**Result**: 1 class, 4 methods (2 public, 2 private)

### Step 3.3: Assess Coverage Adequacy

Compare test count to source complexity:

| Source | Methods | Test Count | Ratio | Assessment |
|--------|---------|------------|-------|------------|
| `weather_service.py` | 4 methods | 12 tests | 3:1 | ✅ Good (multiple scenarios per method) |
| `converters.py` | 4 functions | 6 tests | 1.5:1 | ✅ Adequate |
| `location_repo.py` | 5 methods | 8 tests | 1.6:1 | ✅ Adequate |

**Guideline**: 2-4 tests per function/method is typically good coverage. Fewer might indicate gaps.

## Phase 4: Report Generation

### Step 4.1: Calculate Summary Statistics

```
Total source files: {count from Step 1.1}
Fully covered: {count with matching test files}
Partially covered: {count with some but incomplete coverage}
Not covered: {count with no test files}

Coverage percentage: (fully + partially) / total * 100
```

### Step 4.2: Categorize Gaps by Priority

Group uncovered files using the priority table from Step 1.3:

**P0 (Critical):**
- Services without tests
- Repositories without tests
- Routers without integration tests

**P1 (Important):**
- Utils without tests
- Models without validation tests
- Dependencies without tests

**P2 (Optional):**
- Config, main, exceptions

### Step 4.3: Format Using Template

Apply the [coverage matrix template](../assets/coverage-matrix-template.md):
- Full matrix for "analyze all coverage"
- Quick summary for "what's not tested?"
- Layer-focused for "services coverage"

## Optimization Tips

### Tool Selection

| Goal | Best Tool | Example |
|------|-----------|---------|
| Find all files matching pattern | `file_search` | `file_search: "src/**/*.py"` |
| Count occurrences | `grep_search` | Count `def test_` functions |
| Get file structure | `grep_search` | Find class/function definitions |
| Read specific content | `read_file` | Read file sections for detailed analysis |
| Check file existence | `file_search` | Search for specific filename |

### Parallel Operations

Maximize efficiency by running independent operations in parallel:

**Good (parallel):**
```
- file_search: "src/**/*.py"
- file_search: "tests/unit/**/*.py"
- file_search: "tests/integration/**/*.py"
```

**Slow (sequential):**
```
- file_search: "src/**/*.py"
- [wait for result]
- file_search: "tests/unit/**/*.py"
- [wait for result]
- file_search: "tests/integration/**/*.py"
```

### Avoid Over-Reading

Don't read entire files unless necessary:

**Efficient:**
1. Use `file_search` to find files
2. Use `grep_search` to count patterns (test functions, class definitions)
3. Only use `read_file` if you need detailed code analysis

**Wasteful:**
1. Search for files
2. Read every file completely
3. Count patterns manually from content

## Example Execution

**User request**: "What code isn't tested?"

**Agent workflow:**

1. **Discover** (parallel):
   - Search `src/**/*.py`
   - Search `tests/**/*.py`

2. **Categorize**:
   - Group source files by layer
   - Identify support vs. actual test files

3. **Map**:
   - For each source file, derive expected test path
   - Check if expected test exists

4. **Identify gaps**:
   - `services/openweathermap.py` → ❌ No `tests/unit/test_openweathermap.py`
   - All others → ✅ Found

5. **Prioritize**:
   - `openweathermap.py` is in services → P0 (critical)

6. **Report**:
   ```
   ## Coverage Gaps
   
   ❌ **Critical (P0):**
   - `src/weather_app/services/openweathermap.py` needs unit tests
   
   ✅ **All other files covered** (10/11 = 91% coverage)
   
   **Recommendation:**
   Create `tests/unit/test_openweathermap.py` to test:
   - API request construction
   - Response parsing
   - Error handling for HTTP failures
   - Rate limiting / timeout scenarios
   ```

---

## Troubleshooting

**Problem**: Can't find expected test file, but it might exist with different naming

**Solution**: Use semantic search to find related tests
```
semantic_search: "tests for weather service API client"
```

**Problem**: Too many files to analyze efficiently

**Solution**: Ask user to narrow scope to specific layer
```
"Would you like me to focus on a specific layer? (routers, services, repositories, utils)"
```

**Problem**: Unclear if file needs tests (might be simple)

**Solution**: Quick peek at file to check complexity
```
grep_search: "^class |^def " in the source file
If < 3 matches and no business logic keywords → P2 (optional)
```

---

## Iterative Refinement

For each coverage analysis run:

1. Start with **broad discovery** (all files)
2. **Narrow focus** based on user interest (layer, priority)
3. **Deepen analysis** if requested (test count, coverage depth)
4. **Provide actionable output** (specific files to create, what to test)

Don't do all steps unless asked — match depth to user request.
