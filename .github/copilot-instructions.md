# Copilot Instructions for Weather App

## Project Overview

This is a **GitHub Copilot exercise environment** — a fully working FastAPI weather
service.  The codebase is the substrate participants use to practice Copilot features.
All code is complete and tested; exercises focus on **extending** the application, not
fixing it.

## Architecture

**Layered structure with clear separation of concerns:**

- **Routers** (`src/weather_app/routers/`) — HTTP request handling only.  Validate
  input, call services, return responses.  No business logic here.
- **Services** (`src/weather_app/services/`) — Business logic layer.  `WeatherService`
  orchestrates the API client, handles unit conversion, and evaluates weather alerts.
  `OpenWeatherMapClient` handles all external HTTP communication.
- **Repositories** (`src/weather_app/repositories/`) — Data access layer.
  `LocationRepository` provides CRUD over an in-memory dict.  No database dependency.
- **Models** (`src/weather_app/models.py`) — Pydantic models shared across all layers.
  Used for request/response validation and internal data passing.
- **Utils** (`src/weather_app/utils/`) — Pure, stateless helper functions (converters).
- **Dependencies** (`src/weather_app/dependencies.py`) — FastAPI dependency injection
  wiring.  Provides factory functions for settings, services, and repositories.

## Key Conventions

- **Python 3.12+** with modern syntax (`str | None`, `list[T]`, `StrEnum`)
- **Ruff** for linting and formatting — config in `pyproject.toml`, line length 88
- **Type hints** on all function signatures; **Google-style docstrings** on all public
  functions and classes
- **Async** for all HTTP-facing code (routers, services, API client); repository is
  synchronous (in-memory dict)
- **Custom exceptions** in `services/exceptions.py` inherit from `WeatherAppError`;
  routers raise `fastapi.HTTPException`; global handlers in `main.py`

## Testing Overview

- **pytest + pytest-asyncio + pytest-httpx** — async tests auto-detected
- `tests/unit/` — isolated tests with mocked dependencies
- `tests/integration/` — full request/response with mocked external HTTP
- `tests/factories.py` — centralized test data factories for all models
- Every test module is marked `@pytest.mark.unit` or `@pytest.mark.integration`
- No real API calls — ever

## Dependencies

| Package            | Role                                     |
|--------------------|------------------------------------------|
| fastapi            | Web framework                            |
| uvicorn            | ASGI server                              |
| httpx              | Async HTTP client for OpenWeatherMap API |
| pydantic-settings  | Config from environment variables / .env |
| pytest / pytest-asyncio / pytest-httpx | Testing stack       |
| ruff               | Linting and formatting                   |

## Running

```bash
uv sync                                      # install dependencies
uv run pytest                                 # run all tests
uv run pytest -m unit                         # unit tests only
uv run pytest -m integration                  # integration tests only
uv run ruff check src/ tests/                 # lint
uv run ruff format src/ tests/                # format
uv run uvicorn weather_app.main:app --reload  # start dev server
```
