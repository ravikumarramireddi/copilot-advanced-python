"""Unit tests for OpenWeatherMapClient.

These tests verify the geocode method on the API client using mocked
HTTP responses (via ``pytest-httpx``).
"""

import re

import httpx
import pytest

from tests.factories import make_owm_geocoding_response
from weather_app.config import Settings
from weather_app.services.exceptions import (
    WeatherAPIConnectionError,
    WeatherAPIError,
    WeatherAPINotFoundError,
)
from weather_app.services.openweathermap import OpenWeatherMapClient

pytestmark = pytest.mark.unit


@pytest.fixture
def owm_client(test_settings: Settings) -> OpenWeatherMapClient:
    """An ``OpenWeatherMapClient`` wired to test settings."""
    return OpenWeatherMapClient(test_settings)


# ---------------------------------------------------------------------------
# geocode
# ---------------------------------------------------------------------------


class TestGeocode:
    """Tests for OpenWeatherMapClient.geocode()."""

    async def test_geocode_valid_response_returns_parsed_results(
        self, owm_client: OpenWeatherMapClient, httpx_mock
    ) -> None:
        """Successful geocoding returns a list of location dicts."""
        httpx_mock.add_response(
            url=re.compile(r".*/geo/1\.0/direct.*"),
            json=make_owm_geocoding_response(),
        )

        result = await owm_client.geocode("London", limit=5)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["name"] == "London"
        assert result[0]["country"] == "GB"
        assert result[0]["lat"] == 51.5074
        assert result[0]["lon"] == -0.1278

    async def test_geocode_404_response_raises_not_found_error(
        self, owm_client: OpenWeatherMapClient, httpx_mock
    ) -> None:
        """A 404 response raises WeatherAPINotFoundError."""
        httpx_mock.add_response(
            url=re.compile(r".*/geo/1\.0/direct.*"),
            status_code=404,
            json={"message": "not found"},
        )

        with pytest.raises(WeatherAPINotFoundError):
            await owm_client.geocode("Nowhere", limit=5)

    async def test_geocode_500_response_raises_api_error(
        self, owm_client: OpenWeatherMapClient, httpx_mock
    ) -> None:
        """A 500 response raises WeatherAPIError."""
        httpx_mock.add_response(
            url=re.compile(r".*/geo/1\.0/direct.*"),
            status_code=500,
            json={"message": "internal server error"},
        )

        with pytest.raises(WeatherAPIError):
            await owm_client.geocode("London", limit=5)

    async def test_geocode_timeout_raises_connection_error(
        self, owm_client: OpenWeatherMapClient, httpx_mock
    ) -> None:
        """A timeout raises WeatherAPIConnectionError."""
        httpx_mock.add_exception(
            httpx.TimeoutException("Connection timed out"),
            url=re.compile(r".*/geo/1\.0/direct.*"),
        )

        with pytest.raises(WeatherAPIConnectionError):
            await owm_client.geocode("London", limit=5)

    async def test_geocode_url_includes_api_key_and_query_params(
        self, owm_client: OpenWeatherMapClient, httpx_mock
    ) -> None:
        """The request URL includes the API key and query parameters."""
        httpx_mock.add_response(
            url=re.compile(r".*/geo/1\.0/direct.*"),
            json=make_owm_geocoding_response(),
        )

        await owm_client.geocode("London", limit=5)

        request = httpx_mock.get_request()
        assert "appid=test-api-key-not-real" in str(request.url)
        assert "q=London" in str(request.url)
        assert "limit=5" in str(request.url)
