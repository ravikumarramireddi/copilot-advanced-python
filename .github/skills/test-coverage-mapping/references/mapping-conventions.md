# Test-Source Mapping Conventions

This document defines how test files map to source files in the weather app project.

## Project Structure

### Source Code Organization

```
src/weather_app/
├── models.py              # Pydantic models (request/response schemas)
├── config.py              # Settings and configuration
├── dependencies.py        # FastAPI dependency injection
├── main.py                # Application entry point
├── routers/               # HTTP endpoint handlers
│   ├── __init__.py
│   ├── locations.py       # /locations endpoints
│   └── weather.py         # /weather endpoints
├── services/              # Business logic layer
│   ├── __init__.py
│   ├── exceptions.py      # Custom exception classes
│   ├── openweathermap.py  # External API client
│   └── weather_service.py # Core weather business logic
├── repositories/          # Data access layer
│   ├── __init__.py
│   └── location_repo.py   # Location CRUD operations
├── utils/                 # Pure utility functions
│   ├── __init__.py
│   └── converters.py      # Unit conversion helpers
└── static/                # Frontend assets (HTML/CSS/JS)
    ├── index.html
    ├── style.css
    └── app.js
```

### Test Code Organization

```
tests/
├── __init__.py            # Test package marker
├── conftest.py            # Shared fixtures (settings, app, client)
├── factories.py           # Test data factories for all models
├── unit/                  # Isolated tests with mocked dependencies
│   ├── __init__.py
│   ├── conftest.py        # Unit test fixtures
│   ├── test_converters.py
│   ├── test_location_repo.py
│   ├── test_models.py
│   └── test_weather_service.py
└── integration/           # End-to-end API tests
    ├── __init__.py
    ├── conftest.py        # Integration test fixtures
    ├── test_locations_api.py
    └── test_weather_api.py
```

## Mapping Rules

### Unit Tests (Isolated Component Testing)

**Pattern**: `tests/unit/test_{module}.py` → `src/weather_app/{layer}/{module}.py`

| Source File | Expected Test File | Type |
|-------------|-------------------|------|
| `src/weather_app/utils/converters.py` | `tests/unit/test_converters.py` | Unit |
| `src/weather_app/repositories/location_repo.py` | `tests/unit/test_location_repo.py` | Unit |
| `src/weather_app/services/weather_service.py` | `tests/unit/test_weather_service.py` | Unit |
| `src/weather_app/services/openweathermap.py` | `tests/unit/test_openweathermap.py` | Unit |
| `src/weather_app/models.py` | `tests/unit/test_models.py` | Unit |
| `src/weather_app/config.py` | `tests/unit/test_config.py` | Unit |
| `src/weather_app/dependencies.py` | `tests/unit/test_dependencies.py` | Unit |

**When to use unit tests:**
- Services (business logic, orchestration, calculations)
- Repositories (data access, CRUD operations)
- Utilities (pure functions, conversions, formatters)
- Models (validation rules, computed properties)
- Configuration (settings loading, validation)

**Characteristics:**
- Mock all external dependencies
- Fast execution (no I/O)
- Test single units in isolation
- Focus on edge cases and error conditions

### Integration Tests (API Contract Testing)

**Pattern**: `tests/integration/test_{feature}_api.py` → `src/weather_app/routers/{feature}.py`

| Source File | Expected Test File | Type |
|-------------|-------------------|------|
| `src/weather_app/routers/locations.py` | `tests/integration/test_locations_api.py` | Integration |
| `src/weather_app/routers/weather.py` | `tests/integration/test_weather_api.py` | Integration |
| `src/weather_app/main.py` | `tests/integration/test_app.py` | Integration |

**When to use integration tests:**
- Routers (HTTP endpoints, request/response flow)
- Application setup (middleware, exception handlers)
- Full request-to-response cycles

**Characteristics:**
- Test through FastAPI TestClient
- Mock only external HTTP calls (pytest-httpx)
- Validate API contracts (status codes, response schemas)
- Test dependency injection wiring

### Test Support Files (Not Mapped to Source)

These files support testing but don't map to specific source modules:

| Test File | Purpose |
|-----------|---------|
| `tests/conftest.py` | Shared fixtures across all tests |
| `tests/unit/conftest.py` | Unit test-specific fixtures |
| `tests/integration/conftest.py` | Integration test-specific fixtures |
| `tests/factories.py` | Test data builders (Weather, Location, etc.) |
| `tests/__init__.py` | Package markers |

## Coverage Expectations

### Required Coverage

These source files **MUST** have tests:

1. **Services** (`src/weather_app/services/`)
   - Core business logic
   - Requires thorough unit testing
   - Should test all public methods, error conditions, edge cases

2. **Repositories** (`src/weather_app/repositories/`)
   - Data access layer
   - Requires unit tests for CRUD operations
   - Should test constraints, validations, error handling

3. **Routers** (`src/weather_app/routers/`)
   - API contracts
   - Requires integration tests for all endpoints
   - Should test HTTP status codes, request/response schemas, error responses

4. **Utilities** (`src/weather_app/utils/`)
   - Pure functions
   - Requires comprehensive unit tests
   - Should test edge cases, boundary conditions, type conversions

### Recommended Coverage

These source files **SHOULD** have tests when they contain logic:

1. **Models** (`src/weather_app/models.py`)
   - Test validation rules if they exist
   - Test computed properties or custom methods
   - Skip simple data classes without logic

2. **Dependencies** (`src/weather_app/dependencies.py`)
   - Test factory functions if they have logic
   - Integration tests verify wiring works

3. **Configuration** (`src/weather_app/config.py`)
   - Test validation rules for settings
   - Test environment variable parsing if complex

### Optional Coverage

These files typically don't need dedicated tests:

1. **Initialization** (`__init__.py` files)
   - Usually just imports
   - No testable logic

2. **Entry Point** (`src/weather_app/main.py`)
   - Application assembly
   - Tested indirectly through integration tests

3. **Frontend Assets** (`src/weather_app/static/`)
   - HTML/CSS/JS files
   - Not covered by Python tests
   - Would require frontend testing tools (Jest, Playwright)

## Naming Conventions

### Test File Names

- **Unit tests**: `test_{module_name}.py`
  - Example: `test_weather_service.py` for `weather_service.py`
  
- **Integration tests**: `test_{feature}_api.py`
  - Example: `test_locations_api.py` for locations endpoints

### Test Function Names

Pattern: `test_{feature}_{scenario}_{expected_outcome}`

Examples:
- `test_get_current_weather_valid_coordinates_returns_weather`
- `test_create_location_duplicate_name_raises_error`
- `test_fahrenheit_to_celsius_converts_correctly`

## Coverage Gap Identification

### Algorithm

1. **Discover** all `.py` files under `src/weather_app/` (excluding `__init__.py`, `static/`)
2. **Categorize** each file by layer (routers, services, repositories, utils, models, etc.)
3. **Search** for corresponding test files using the mapping patterns above
4. **Flag** files with:
   - ❌ No test file found
   - ⚠️ Test file exists but might be incomplete (fewer than 3 test functions)
   - ✅ Test file exists with comprehensive coverage

### Priority Classification

**P0 (Critical) - Must have tests:**
- All files in `services/` except `exceptions.py`
- All files in `repositories/`
- All files in `routers/`

**P1 (Important) - Should have tests:**
- Files in `utils/`
- `models.py` if it has validation or computed properties
- `dependencies.py` if factory functions have logic

**P2 (Nice to have) - Optional tests:**
- `config.py` for complex validation
- `exceptions.py` (just class definitions)
- `main.py` (tested via integration tests)

### Example Gap Report

```markdown
## Coverage Analysis Results

### ✅ Fully Covered (5 files)
- `services/weather_service.py` → `unit/test_weather_service.py` (12 tests)
- `repositories/location_repo.py` → `unit/test_location_repo.py` (8 tests)
- `utils/converters.py` → `unit/test_converters.py` (6 tests)
- `routers/locations.py` → `integration/test_locations_api.py` (7 tests)
- `routers/weather.py` → `integration/test_weather_api.py` (9 tests)

### ❌ Not Covered - P0 (1 file)
- `services/openweathermap.py` - **CRITICAL**: External API client needs unit tests

### ⚠️ Partially Covered - P1 (2 files)
- `models.py` → `unit/test_models.py` (2 tests) - May need more validation tests
- `dependencies.py` - No dedicated tests (covered indirectly via integration)

### P2 - Optional (1 file)
- `config.py` - Settings class (validation tested indirectly)
```

## Adapting to Other Projects

To use this skill on a different project, update these patterns:

1. **Source root**: Change from `src/weather_app/` to your source directory
2. **Test root**: Change from `tests/` to your test directory
3. **Layer names**: Adjust `routers/`, `services/`, etc. to your architecture
4. **Naming convention**: Update `test_{module}.py` pattern if needed
5. **Test types**: Add or remove test categories (e.g., `e2e/`, `functional/`)

Update this reference file when project conventions change.
