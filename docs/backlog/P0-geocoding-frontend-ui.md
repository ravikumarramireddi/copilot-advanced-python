# [P0] Integrate city search in frontend UI

**GitHub Issue:** [#2](https://github.com/ravikumarramireddi/copilot-advanced-python/issues/2) | **Status:** ✅ Completed

**As a** user, **I want** to search for locations by city name in the UI **so that** I don't have to manually look up and enter latitude/longitude coordinates.

**Acceptance Criteria:**
- [ ] Displays new city search input field above coordinate inputs
- [ ] Search input shows placeholder "Search by city (e.g., London, New York)"
- [ ] Displays "Search" button next to city input field
- [ ] Clicking Search button calls `/api/locations/search` API with entered city name
- [ ] Shows loading indicator while search is in progress
- [ ] Displays search results in dropdown below search input (max 5 visible)
- [ ] Each result shows format: "City, State, Country" (state optional)
- [ ] Clicking a result populates lat/lon inputs and triggers weather fetch
- [ ] Clicking outside dropdown or pressing Escape key closes results
- [ ] Shows "No results found" message when API returns empty array
- [ ] Shows error message when API call fails
- [ ] Existing coordinate-based search flow continues to work without changes

**TDD Requirements:**
- [ ] Manual browser testing (no automated frontend tests in current project)
  - Test search for "London" displays multiple results
  - Test clicking first result populates lat/lon fields
  - Test clicking result triggers automatic weather fetch and display
  - Test search for "asdfqwerzxcv" shows "No results found" message
  - Test network error shows user-friendly error message
  - Test dropdown closes when clicking outside
  - Test dropdown closes when pressing Escape key
  - Test existing coordinate search (lat/lon + Search button) still works
  - Test search with empty input shows validation message
  - Test loading indicator appears during search

**Definition of Done:**
- [ ] All acceptance criteria met
- [ ] Manual browser testing completed and documented in test notes
- [ ] No JavaScript console errors during manual testing
- [ ] UI is responsive on mobile and desktop viewports
- [ ] Error states display user-friendly messages
- [ ] Follows existing design patterns from `style.css`

**Effort Estimate:** S

**Files likely touched:**
- `src/weather_app/static/index.html` — Add city search input, button, and results dropdown container
- `src/weather_app/static/app.js` — Add `searchCityName()`, `showSearchResults()`, `handleResultClick()` functions
- `src/weather_app/static/style.css` — Style search dropdown, results list, loading state, error messages

**Dependencies:** 
- "[P0] Implement geocoding API endpoint (backend)" must be completed first

**Impacted layers:**
- Models: None
- Services: None
- Routers: None
- Repositories: None
- Tests: Manual browser testing only
- Frontend: HTML structure, JavaScript event handlers, CSS styling

**Technical Notes:**
- Add input debouncing (300ms delay) to reduce API calls while user is typing
- Use `fetch('/api/locations/search?q=' + encodeURIComponent(cityInput.value))` for API call
- Show dropdown only when results array length > 0
- Dropdown HTML structure: `<ul class="search-results"><li>City, Country</li></ul>`
- On result click: `latInput.value = result.lat; lonInput.value = result.lon; fetchWeather(result.lat, result.lon)`
- Add keyboard navigation: arrow keys to navigate results, Enter to select, Escape to close
- Loading state: disable search button and show spinner icon during fetch
- Error handling: catch fetch errors and display in `<div id="search-error" class="error">` element
- Follow existing CSS patterns for `.error`, `.hidden` classes
- Close dropdown by adding `display: none` or `.hidden` class when clicking outside or on Escape
