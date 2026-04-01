---
name: run-tests
description: "Run the project test suite using uv run pytest and interpret results. Use when: verifying implementation correctness, checking tests pass after a change, running unit or integration tests selectively, auditing test health, confirming TDD red/green cycles."
argument-hint: "Optional: scope to run (unit, integration, or a specific test file/module path)"
---

# Run Tests

## When to Use

Use this skill any time an agent needs to execute the test suite and interpret
the results deterministically.

**Trigger phrases / situations:**
- "Run the tests"
- "Are all tests passing?"
- "Check my implementation"
- "Run unit tests only"
- "Run integration tests"
- "Verify the test suite is green"
- After implementing a feature or fixing a bug

---

## Project Test Layout

```
tests/
├── conftest.py          # shared fixtures: test_settings, app, client, location_repo
├── factories.py         # factory functions for all Pydantic models
├── unit/
│   ├── conftest.py
│   ├── test_converters.py       → src/weather_app/utils/converters.py
│   ├── test_location_repo.py    → src/weather_app/repositories/location_repo.py
│   ├── test_models.py           → src/weather_app/models.py
│   └── test_weather_service.py  → src/weather_app/services/weather_service.py
└── integration/
    ├── conftest.py
    ├── test_locations_api.py    → src/weather_app/routers/locations.py
    └── test_weather_api.py      → src/weather_app/routers/weather.py
```

**Key facts:**
- `asyncio_mode = "auto"` — no `@pytest.mark.asyncio` decorator needed.
- `testpaths = ["tests"]` — pytest auto-discovers from `tests/`.
- Two registered markers: `unit` and `integration`.
- No real HTTP or API calls anywhere — external HTTP is mocked via `pytest-httpx`.

---

## Commands

### Run the full suite
```bash
uv run pytest
```

### Run only unit tests
```bash
uv run pytest -m unit
```
Use this after changing business logic, models, utilities, or repository code.

### Run only integration tests
```bash
uv run pytest -m integration
```
Use this after changing routers, middleware, dependency wiring, or `main.py`.

### Run a specific test file
```bash
uv run pytest tests/unit/test_weather_service.py
```

### Run a specific test by name (substring match)
```bash
uv run pytest -k "test_get_current_weather"
```

### Verbose output with short summary
```bash
uv run pytest -v --tb=short
```
This is the recommended form when diagnosing failures — it shows the full test
name, pass/fail status, and a concise traceback.

---

## Procedure

### Step 1 — Choose the scope

| What changed | Command |
|---|---|
| `src/weather_app/utils/` | `uv run pytest -m unit` |
| `src/weather_app/repositories/` | `uv run pytest -m unit` |
| `src/weather_app/services/` | `uv run pytest -m unit` |
| `src/weather_app/models.py` | `uv run pytest -m unit` |
| `src/weather_app/routers/` | `uv run pytest -m integration` |
| `src/weather_app/main.py` or `dependencies.py` | `uv run pytest` |
| Multiple layers touched | `uv run pytest` |
| After a complete TDD cycle | `uv run pytest` |

When in doubt, run the **full suite**.

### Step 2 — Execute and capture output

Run with `-v --tb=short` to get structured, parseable output:

```bash
uv run pytest -v --tb=short 2>&1
```

### Step 3 — Parse the result summary

pytest always prints a summary line at the end.  Look for the **last line** of
output:

| Pattern | Meaning |
|---|---|
| `N passed` | All tests passed — suite is green. |
| `N passed, M warnings` | Passing with non-fatal warnings — acceptable. |
| `N failed, M passed` | Some tests are failing — investigate. |
| `N error` | Collection errors (import failures, fixture errors) — fix before the test run is meaningful. |
| `no tests ran` | Wrong marker, wrong path, or all tests are deselected — check your command. |

### Step 4 — Extract failing test names

If any test fails, extract each failing test's **fully qualified name** from the
`FAILED` lines in verbose output:

```
FAILED tests/unit/test_weather_service.py::test_get_current_weather_invalid_coords_raises_error
```

Report these names exactly so they can be re-run individually or used to
locate the failing code.

### Step 5 — Report structured results

After running, produce a structured summary in this format:

```
Test run: <scope>
Command:  <exact command used>
Result:   PASS | FAIL | ERROR

Counts:
  passed:   N
  failed:   N
  errors:   N
  warnings: N

Failing tests:
  - tests/unit/test_weather_service.py::test_name_here
  - tests/integration/test_weather_api.py::test_name_here

Next action: <what to do based on result>
```

If the suite is fully green, the `Failing tests` section can be omitted.

---

## TDD Workflow Integration

This skill supports a strict **red → green → refactor** cycle:

1. **Red phase**: Write a failing test, then run `uv run pytest -v --tb=short`
   and confirm exactly one new failure with the expected test name.

2. **Green phase**: Implement the minimum code to pass, then run the same
   command and confirm the failure is gone *and no previously-passing tests
   broke*.

3. **Refactor phase**: Clean up the implementation, then run `uv run pytest`
   (full suite) to confirm everything remains green.

> **Never skip the full-suite run at refactor phase.** A targeted run hides
> regressions introduced by changes to shared code (models, converters, etc.).

---

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ImportError` during collection | Missing import or circular dependency | Fix the import in the source or test file |
| `fixture 'X' not found` | Fixture defined in wrong conftest or misspelled | Check `tests/conftest.py` and `tests/unit/conftest.py` |
| `WARNINGS: PytestUnraisableExceptionWarning` | Async teardown issue | Usually benign; ignore unless it causes a failure |
| `no tests ran` when using `-m unit` | Test module missing `pytestmark = pytest.mark.unit` | Add the marker at top of the test module |
| `AssertionError` on a factory value | Factory default changed | Override the field explicitly in the test call |

---

## Linting (Optional Pre-check)

Before running tests, optionally verify code style to catch obvious errors
early:

```bash
uv run ruff check src/ tests/
```

Auto-fix safe issues with:

```bash
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/
```

Linting failures do **not** cause `pytest` to fail, but they should be
resolved before merging.
