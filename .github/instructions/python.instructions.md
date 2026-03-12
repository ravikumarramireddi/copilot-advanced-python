---
name: "Python Source"
description: "Coding conventions for Python application source code in the weather app"
applyTo: "src/**/*.py"
---

# Python Source Code Conventions

## Language & Syntax

- **Python 3.12+** — use modern union syntax (`str | None`), generic builtins
  (`list[T]`, `dict[K, V]`), and `StrEnum` for string enumerations.
- Type-hint **every** function signature (parameters and return type).
- Add **Google-style docstrings** to all public functions and classes.  Keep them
  brief: one summary line, then `Args:` / `Returns:` / `Raises:` sections only
  when the signature alone isn't self-explanatory.

## Formatting & Imports

- **Ruff** handles linting and formatting — config lives in `pyproject.toml`.
- **Line length**: 88 characters.
- **Import order** (enforced by Ruff isort rules): standard library → third-party
  → first-party (`weather_app.*`).  Group with a blank line between each.
- Prefer explicit imports over star imports.

## Naming

| Element          | Convention          | Example                   |
|------------------|---------------------|---------------------------|
| Files            | `snake_case.py`     | `weather_service.py`      |
| Classes          | `PascalCase`        | `WeatherService`          |
| Functions / vars | `snake_case`        | `get_current_weather`     |
| Constants        | `UPPER_SNAKE_CASE`  | `_COMPASS_POINTS`         |
| Private members  | `_` prefix          | `_parse_current_weather`  |

## Layer Responsibilities

Respect the layered architecture — keep each layer focused:

- **Routers** — HTTP concern only.  Validate input via `Annotated[..., Query()]`
  or Pydantic models, call the service, return the response model.  Never
  contain business logic.  Example pattern:

  ```python
  @router.get("/current", response_model=CurrentWeather)
  async def get_current_weather(
      lat: Annotated[float, Query(ge=-90, le=90)],
      service: WeatherService = Depends(get_weather_service),
  ) -> CurrentWeather:
  ```

- **Services** — Business logic.  Orchestrate calls to `OpenWeatherMapClient`,
  perform unit conversion, evaluate alert thresholds.  Services receive
  dependencies via constructor injection.
- **Repositories** — Data access only.  The `LocationRepository` is synchronous
  (in-memory dict); do not add async to repository methods.
- **Utils** — Pure, stateless functions.  No side effects, no I/O.
- **Models** — Pydantic `BaseModel` subclasses.  Use `Field(...)` for validation
  constraints and descriptions.

## Async Patterns

- All HTTP-facing code (routers, services, API client) must be `async def`.
- Use `httpx.AsyncClient` for outgoing HTTP — never `requests` or synchronous
  `httpx`.
- Repository methods are synchronous — `def`, not `async def`.

## Error Handling

- **Domain exceptions** live in `services/exceptions.py` and inherit from
  `WeatherAppError`.  Each exception stores a `message` attribute.
- Never raise `fastapi.HTTPException` from service or repository code.
- Routers catch domain exceptions and translate them to `HTTPException`,
  or rely on the global exception handlers registered in `main.py`.
- When adding a new domain exception: subclass the closest existing one
  (`WeatherAPIError`, `WeatherAppError`), keep the pattern of storing
  `status_code` and `message`.

## Dependency Injection

- Factory functions live in `dependencies.py` and are used via
  `Depends(get_weather_service)`.
- `get_settings()` is cached with `@lru_cache(maxsize=1)`.
- Tests override dependencies via `app.dependency_overrides`.

## Pydantic Models

- Use `Field(...)` with `description` for API-visible fields.
- Prefer `default_factory` over mutable defaults.
- Enums use `StrEnum` so they serialize to readable strings.
- Shared across all layers — defined once in `models.py`, imported everywhere.
