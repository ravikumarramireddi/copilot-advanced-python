# [P0] Implement geocoding API endpoint (backend)

**GitHub Issue:** [#1](https://github.com/ravikumarramireddi/copilot-advanced-python/issues/1) | **Status:** ✅ Completed

**As a** developer, **I want** a backend API endpoint to search locations by city name **so that** the frontend can provide users with a better location-entry experience.

**Acceptance Criteria:**
- [ ] Returns 200 with array of location results when query is valid
- [ ] Validates query parameter is at least 2 characters long
- [ ] Returns 400 with error message when query is empty or too short
- [ ] Accepts optional `limit` query parameter (default: 5, max: 10)
- [ ] Returns empty array (200) when OpenWeatherMap finds no matches
- [ ] Each result includes: name, country, state (optional), lat, lon
- [ ] Integrates OpenWeatherMap Geocoding API endpoint in client layer
- [ ] Service layer validates query and enforces limit constraints

**TDD Requirements:**
- [ ] Unit test: `OpenWeatherMapClient.geocode()` method with mocked httpx responses
  - Test successful parse of valid OpenWeatherMap geocoding response
  - Test handling of 404 response (location not found)
  - Test handling of 500 response (API server error)
  - Test handling of timeout exception
  - Test URL construction includes API key and query params
- [ ] Unit test: `WeatherService.search_locations()` method with mocked OpenWeatherMapClient
  - Test successful search returns list of LocationSearchResult models
  - Test search with no results returns empty list
  - Test query validation raises exception for empty string
  - Test query validation raises exception for single character
  - Test limit parameter defaults to 5
  - Test limit parameter enforces maximum of 10
  - Test query string is trimmed of whitespace
- [ ] Integration test: `GET /api/locations/search` endpoint
  - Test 200 response with valid city name "London"
  - Test 400 response for empty query parameter
  - Test 400 response for query with 1 character
  - Test 200 with empty array when no results found
  - Test default limit of 5 results
  - Test custom limit parameter (e.g., limit=3)
  - Test limit parameter rejects values > 10 (422)
  - Test query whitespace trimming ("  Paris  " works)
- Tests must be written first and fail before implementation begins

**Definition of Done:**
- [ ] All acceptance criteria met
- [ ] All TDD requirements implemented and passing (`uv run pytest`)
- [ ] No new lint violations (`uv run ruff check src/ tests/`)
- [ ] No source files modified without a corresponding test change
- [ ] API documented with OpenAPI examples in route docstrings
- [ ] Can be tested with curl or Postman without frontend changes

**Effort Estimate:** M

**Files likely touched:**
- `src/weather_app/models.py` — Add `LocationSearchResult` Pydantic model with name, country, state, lat, lon fields
- `src/weather_app/services/openweathermap.py` — Add `geocode(query: str, limit: int)` async method
- `src/weather_app/services/weather_service.py` — Add `search_locations(query: str, limit: int)` orchestration method
- `src/weather_app/routers/locations.py` — Add `GET /api/locations/search` endpoint with query validation
- `tests/unit/test_weather_service.py` — Unit tests for search_locations with mocked client
- `tests/unit/test_openweathermap.py` — New file: unit tests for geocode method (or add to existing if present)
- `tests/integration/test_locations_api.py` — Integration tests for search endpoint with mocked httpx

**Dependencies:** None

**Impacted layers:**
- Models: New `LocationSearchResult` model with fields: name, country, state (optional), lat, lon
- Services: New `geocode()` method in `OpenWeatherMapClient` + `search_locations()` in `WeatherService`
- Routers: New `GET /api/locations/search` endpoint in locations router
- Repositories: None
- Tests: Unit tests (OpenWeatherMapClient + WeatherService) and integration tests (API endpoint)
- Frontend: None

**Technical Notes:**
- Use OpenWeatherMap Geocoding API: `GET http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit={limit}&appid={API_key}`
- API response format: `[{"name": "London", "lat": 51.5074, "lon": -0.1278, "country": "GB", "state": "England"}]`
- Query validation: Strip whitespace with `.strip()`, check `len(query) >= 2` before calling API
- Limit validation: Use FastAPI `Query(ge=1, le=10, default=5)` for automatic validation
- Return empty list (not 404) when OpenWeatherMap returns empty array
- Handle OpenWeatherMap API errors by raising appropriate exceptions (WeatherAPIError, WeatherAPIConnectionError)
- Service layer should convert raw dict responses to `LocationSearchResult` models
