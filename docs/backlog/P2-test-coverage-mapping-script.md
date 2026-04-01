# [P2] Add deterministic coverage-map.py script to test-coverage-mapping skill

**GitHub Issue:** [#3](https://github.com/ravikumarramireddi/copilot-advanced-python/issues/3) | **Status:** ✅ Completed

**As a** developer using the `test-coverage-mapping` skill, **I want** a deterministic shell script to discover source and test files **so that** coverage gap analysis is consistent and reproducible rather than relying on the LLM to scan files itself.

**Acceptance Criteria:**
- [ ] `.github/skills/test-coverage-mapping/coverage-map.py` exists and is executable with `python3`
- [ ] Script walks `src/weather_app/` and collects all testable `.py` files (excludes `__init__.py`, `main.py`, files under `static/`, files under `__pycache__/`)
- [ ] Script walks `tests/unit/` and `tests/integration/` and discovers all existing test files
- [ ] Script applies naming conventions (`test_{module}.py` for unit, `test_{feature}_api.py` for integration/routers) to link each source file to its expected test counterpart
- [ ] Script outputs valid JSON to stdout with three top-level keys: `mapped`, `gaps`, and `summary`
- [ ] `mapped` contains source→test file pairs that exist; `gaps` lists source files with no matching test; `summary` contains counts
- [ ] `SKILL.md` steps 2 and 3 (which instruct the agent to use file search tools) are replaced with a single step that runs `python3 .github/skills/test-coverage-mapping/coverage-map.py` and instructs the agent to consume the JSON output

**TDD Requirements:**
- No application code is modified; this item is purely tooling. Verification is done by running the script and inspecting output:
  - Run `python3 .github/skills/test-coverage-mapping/coverage-map.py` from the repo root — exits 0 and prints valid JSON
  - Output contains `mapped`, `gaps`, and `summary` keys
  - `summary.total_source_files` matches the number of testable source modules
  - `summary.covered` + `summary.gaps` == `summary.total_source_files`
  - All currently-tested modules (e.g., `converters`, `location_repo`, `models`, `weather_service`) appear in `mapped`
  - Modules without tests (e.g., `config`, `dependencies`, `exceptions`, `openweathermap`) appear in `gaps`
- Tests must be written first and fail before implementation begins

**Definition of Done:**
- [ ] All acceptance criteria met
- [ ] Script runs successfully from repo root (`python3 .github/skills/test-coverage-mapping/coverage-map.py`)
- [ ] JSON output is valid and contains all three required keys
- [ ] `SKILL.md` no longer instructs the agent to scan files manually in steps 2–3
- [ ] No new lint violations (`uv run ruff check src/ tests/`)
- [ ] Can be verified independently without any application code changes

**Effort Estimate:** XS

**Files likely touched:**
- `.github/skills/test-coverage-mapping/coverage-map.py` — New script: walks source and test trees, maps files by naming convention, outputs JSON
- `.github/skills/test-coverage-mapping/SKILL.md` — Replace steps 2–3 with a single step invoking the script and consuming its JSON output

**Dependencies:** None

**Impacted layers:**
- Models: None
- Services: None
- Routers: None
- Repositories: None
- Tests: None (tooling only; no pytest tests required)
- Frontend: None

**Technical Notes:**
- Use `pathlib.Path.rglob("*.py")` to walk directories; filter with a deny-list: `{"__init__.py", "main.py"}` and skip paths containing `static` or `__pycache__`
- Naming convention logic:
  - For `src/weather_app/{layer}/{module}.py` → expected unit test: `tests/unit/test_{module}.py`
  - For `src/weather_app/routers/{feature}.py` → expected integration test: `tests/integration/test_{feature}_api.py`
  - Top-level modules (e.g., `models.py`, `config.py`) → expected unit test: `tests/unit/test_{module}.py`
- JSON schema example:
  ```json
  {
    "mapped": [
      {"source": "src/weather_app/utils/converters.py", "test": "tests/unit/test_converters.py", "type": "unit"}
    ],
    "gaps": [
      {"source": "src/weather_app/config.py", "expected_test": "tests/unit/test_config.py"}
    ],
    "summary": {
      "total_source_files": 9,
      "covered": 4,
      "gaps": 5
    }
  }
  ```
- Script must use only Python standard library (no third-party dependencies)
- Output must go to stdout; all debug/log output (if any) must go to stderr
- After updating `SKILL.md`, the new step 2 should read: "Run `python3 .github/skills/test-coverage-mapping/coverage-map.py` from the repo root and capture the JSON output. Use the `mapped`, `gaps`, and `summary` fields to proceed — do not scan files manually."
