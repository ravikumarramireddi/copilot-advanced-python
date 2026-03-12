---
name: "Python Tests"
description: "Testing conventions and patterns for pytest test files"
applyTo: "tests/**/*.py"
---

# Testing Conventions

## Framework & Configuration

- **pytest + pytest-asyncio + pytest-httpx** is the testing stack.
- Async tests are auto-detected (`asyncio_mode = "auto"` in `pyproject.toml`)
  — no `@pytest.mark.asyncio` decorator needed.
- **No real API calls** — ever.  Unit tests mock at the service boundary;
  integration tests mock outgoing HTTP via `pytest-httpx`.

## Test Organisation

- `tests/unit/` — isolated tests with mocked dependencies.
- `tests/integration/` — full request/response through the FastAPI app with
  external HTTP mocked.
- `tests/factories.py` — centralized test data factories for all models.
- `tests/conftest.py` — shared fixtures: `test_settings`, `app`, `client`,
  `location_repo`.

## Module-Level Markers

Every test module must declare its marker at the top, after imports:

```python
pytestmark = pytest.mark.unit        # or pytest.mark.integration
```

This enables `pytest -m unit` / `pytest -m integration` filtering.

## Naming

`test_{feature}_{scenario}_{expected_outcome}`

Examples:
- `test_get_current_weather_valid_coordinates_returns_weather`
- `test_create_location_duplicate_name_raises_error`

## AAA Pattern

Structure every test as **Arrange → Act → Assert**, separated by blank lines:

```python
async def test_get_forecast_converts_to_fahrenheit(weather_service, mock_client):
    # Arrange
    mock_client.get_forecast.return_value = ("London", [make_forecast_day()])

    # Act
    result = await weather_service.get_forecast(51.51, -0.13, units=TemperatureUnit.FAHRENHEIT)

    # Assert
    assert result.units == TemperatureUnit.FAHRENHEIT
```

One behavior per test — each test verifies exactly one thing.

## Factories Over Raw Dicts

Use factory functions from `tests/factories.py` instead of constructing raw
dicts or models inline.  Every factory accepts keyword overrides:

```python
make_location(name="Paris", lat=48.86)
make_current_weather(temperature=30.0, wind_speed=25.0)
```

See [tests/factories.py](../../tests/factories.py) for the full set of
available factories (`make_location`, `make_current_weather`,
`make_forecast_day`, `make_weather_alert`, `make_owm_current_weather_response`,
etc.).

## Parametrize

Use `@pytest.mark.parametrize` for multiple input/output cases.  This avoids
test duplication and makes edge cases explicit:

```python
@pytest.mark.parametrize("celsius, expected", [(0, 32.0), (100, 212.0), (-40, -40.0)])
def test_celsius_to_fahrenheit(celsius, expected):
    assert celsius_to_fahrenheit(celsius) == expected
```

## Mocking Strategy

### Unit Tests

- Inject `AsyncMock(spec=OpenWeatherMapClient)` into `WeatherService`.
- The `mock_client` and `weather_service` fixtures in `tests/unit/conftest.py`
  wire this up.  Use them rather than creating mocks manually.
- Mock at the **service boundary** — mock the client's methods, not internal
  HTTP calls.

### Integration Tests

- Use the `httpx_mock` fixture (from `pytest-httpx`) to intercept outgoing
  `httpx` requests made by `OpenWeatherMapClient`.
- Build mock responses using the `make_owm_*_response` factory functions.
- The `app` and `client` fixtures in `tests/conftest.py` provide a FastAPI
  app with dependency overrides and an async test client.

### Dependency Overrides

```python
application.dependency_overrides[get_settings] = lambda: test_settings
application.dependency_overrides[get_location_repository] = lambda: location_repo
```

This pattern isolates each test from real configuration and shared state.

## Fixtures

- Prefer **narrow-scope** fixtures (function-level) to avoid state leakage.
- Shared fixtures go in `tests/conftest.py`; test-category-specific fixtures
  go in `tests/unit/conftest.py` or `tests/integration/conftest.py`.
- Yield fixtures should clean up in the teardown phase (after `yield`).

## Running Tests

```bash
uv run pytest                    # all tests
uv run pytest -m unit            # unit tests only
uv run pytest -m integration     # integration tests only
uv run pytest -v                 # verbose output
```
