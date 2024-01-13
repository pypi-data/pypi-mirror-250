from pydantic import BaseModel, Field, model_validator, computed_field
from httpx import AsyncClient, Client
from datetime import datetime
from openepi_client.weather._weather_types import METJSONSunrise, METJSONForecast
from openepi_client import openepi_settings, GeoLocation


class SunriseRequest(BaseModel):
    geolocation: GeoLocation = Field(..., description="The geolocation to query for")
    date: datetime | None = Field(
        default_factory=datetime.today, description="The date to query for"
    )
    _sunrise_endpoint = f"{openepi_settings.api_root_url}/weather/sunrise"

    @computed_field
    @property
    def _params(self) -> dict:
        return {
            "lat": self.geolocation.lat,
            "lon": self.geolocation.lon,
            "date": self.date.strftime("%Y-%m-%d"),
        }

    def get_sync(self) -> METJSONSunrise:
        with Client() as client:
            response = client.get(self._sunrise_endpoint, params=self._params)
            return METJSONSunrise(**response.json())

    async def get_async(self) -> METJSONSunrise:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._sunrise_endpoint, params=self._params
            )
            return METJSONSunrise(**response.json())


class LocationForecastRequest(BaseModel):
    geolocation: GeoLocation = Field(..., description="The geolocation to query for")
    _location_forecast_endpoint = (
        f"{openepi_settings.api_root_url}/weather/locationforecast"
    )

    @computed_field
    @property
    def _params(self) -> dict:
        return {
            "lat": self.geolocation.lat,
            "lon": self.geolocation.lon,
            "altitude": self.geolocation.alt,
        }

    def get_sync(self) -> METJSONForecast:
        with Client() as client:
            response = client.get(self._location_forecast_endpoint, params=self._params)
            return METJSONForecast(**response.json())

    async def get_async(self) -> METJSONForecast:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._location_forecast_endpoint, params=self._params
            )
            return METJSONForecast(**response.json())


class WeatherClient:
    @staticmethod
    def get_sunrise(
        geolocation: GeoLocation,
        date: datetime | None = datetime.today(),
    ) -> METJSONSunrise:
        return SunriseRequest(geolocation=geolocation, date=date).get_sync()

    @staticmethod
    def get_location_forecast(geolocation: GeoLocation) -> METJSONForecast:
        return LocationForecastRequest(geolocation=geolocation).get_sync()


class AsyncWeatherClient:
    @staticmethod
    async def get_sunrise(
        geolocation: GeoLocation,
        date: datetime | None = datetime.today(),
    ) -> METJSONSunrise:
        return await SunriseRequest(geolocation=geolocation, date=date).get_async()

    @staticmethod
    async def get_location_forecast(
        geolocation: GeoLocation,
    ) -> METJSONForecast:
        return await LocationForecastRequest(geolocation=geolocation).get_async()
