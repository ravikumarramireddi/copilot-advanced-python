# Weather App Backlog

## Project Assessment: Improvement Areas

After analyzing the codebase, the following improvement areas have been identified:

### 1. **Location Management UX** ⭐ HIGH PRIORITY
- **Issue**: Users must manually find and enter latitude/longitude coordinates
- **Impact**: Poor UX; non-technical users don't know coordinates for cities
- **Opportunity**: Add geocoding to search locations by city name

### 2. **Data Optimization**
- **Issue**: No caching; every request hits the external OpenWeatherMap API
- **Impact**: Slower responses, higher API usage, potential rate limiting
- **Opportunity**: Add response caching with TTL (e.g., 5-10 minutes for current weather)

### 3. **Enhanced Location Features**
- **Issue**: Can't mark locations as favorite/default; no sorting/filtering options
- **Impact**: Users with many saved locations have difficulty organizing them
- **Opportunity**: Add favorite flag and custom sorting (alphabetical, by creation, by favorite)

### 4. **Weather Data Enrichment**
- **Issue**: Missing available OpenWeatherMap data: air quality, UV index, precipitation probability
- **Impact**: Limited weather insights compared to competitors
- **Opportunity**: Integrate additional OpenWeatherMap endpoints (Air Quality API, One Call API)

### 5. **Multi-Location Comparison**
- **Issue**: Can't view or compare weather across multiple saved locations simultaneously
- **Impact**: Users must click through locations one-by-one
- **Opportunity**: Add comparison view showing current weather for all saved locations

### 6. **Historical Data & Trends**
- **Issue**: No historical weather data or trend analysis
- **Impact**: Users can't see patterns or compare current conditions to past averages
- **Opportunity**: Store weather snapshots over time; visualize trends

### 7. **Notification System**
- **Issue**: Weather alerts are passive (must refresh page); no proactive notifications
- **Impact**: Users might miss severe weather warnings
- **Opportunity**: Add WebSocket or polling for real-time alert notifications

### 8. **Data Export**
- **Issue**: No way to export saved locations or weather data
- **Impact**: Users can't backup their data or use it in other tools
- **Opportunity**: Add CSV/JSON export for locations and weather snapshots

---

## Selected Feature: City Name Geocoding

**Rationale**: This feature addresses the highest-priority UX pain point. It's been split into two properly-scoped backlog items that can each be implemented within a single agent context window. The backend API can be implemented and tested independently, then the frontend can consume it.

See individual backlog items:
- [P0-geocoding-api-backend.md](./backlog/P0-geocoding-api-backend.md)
- [P0-geocoding-frontend-ui.md](./backlog/P0-geocoding-frontend-ui.md)

---

## Active Backlog Items

Individual backlog items are maintained as separate files in `docs/backlog/` for better tracking and reusability:

### Priority 0 (Critical)
1. **[P0-geocoding-api-backend.md](./backlog/P0-geocoding-api-backend.md)** — Implement geocoding API endpoint (backend)  
   _Status: ✅ Completed | Issue: [#1](https://github.com/ravikumarramireddi/copilot-advanced-python/issues/1) | Effort: M | Dependencies: None_

2. **[P0-geocoding-frontend-ui.md](./backlog/P0-geocoding-frontend-ui.md)** — Integrate city search in frontend UI  
   _Status: ✅ Completed | Issue: [#2](https://github.com/ravikumarramireddi/copilot-advanced-python/issues/2) | Effort: S | Dependencies: Backend API completion_

### Priority 2 (Maintenance/Tooling)
3. **[P2-test-coverage-mapping-script.md](./backlog/P2-test-coverage-mapping-script.md)** — Add coverage-map.py script  
   _Status: ✅ Completed | Issue: [#3](https://github.com/ravikumarramireddi/copilot-advanced-python/issues/3) | Effort: XS | Dependencies: None_

---

## Backlog Grooming Notes

**Sprint Status: ✅ COMPLETE**
- ✅ P0 geocoding feature delivered (backend + frontend integration)
- ✅ OpenWeatherMap Geocoding API successfully integrated
- ✅ Test coverage mapping script delivered for future development workflow
- ✅ Pattern established for future search/autocomplete enhancements

**Validation Required:**
1. Run full test suite: `uv run pytest -v --tb=short`
2. Manual browser testing of city search UI
3. Run coverage mapping script: `python3 .github/skills/test-coverage-mapping/coverage-map.py`

**Next Sprint Planning:**
Ready to select next feature from improvement areas above. Top candidates:
1. **Data Optimization (Caching)** — Add HTTP response caching with TTL (5-10 min)
2. **Enhanced Location Features** — Add favorite/default location markers
3. **Multi-Location Comparison** — Dashboard view of all saved locations
4. **Weather Data Enrichment** — Add air quality, UV index, precipitation probability

**Future Enhancements (City Search):**
- Autocomplete for city search (requires frontend debouncing + backend caching)
- Recent searches history (localStorage or user preferences)
- Geolocation API integration to detect user's current location
- Rate limiting on search endpoint to prevent API abuse
