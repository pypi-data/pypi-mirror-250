from pydantic import BaseModel, Field, computed_field
from httpx import AsyncClient, Client

from openepi_client import openepi_settings, GeoLocation
from openepi_client.geocoding._geocoding_types import FeatureCollection


class GeocodeRequest(BaseModel):
    q: str = Field(..., description="The query string to geocode")
    geolocation: GeoLocation | None = Field(
        default=None, description="The geolocation to query for"
    )
    lang: str | None = Field(
        default=None,
        description="Set preferred language (e.g. 'default', 'en', 'de', 'fr')",
    )
    limit: int | None = Field(default=None, description="The maximum number of results")
    _geocode_endpoint = f"{openepi_settings.api_root_url}/geocoding/"

    @computed_field
    @property
    def _params(self) -> dict:
        return {
            k: v
            for k, v in {
                "q": self.q,
                "lon": self.geolocation.lon if self.geolocation else None,
                "lat": self.geolocation.lat if self.geolocation else None,
                "lang": self.lang,
                "limit": self.limit,
            }.items()
            if v is not None
        }

    def get_sync(self) -> FeatureCollection:
        with Client() as client:
            response = client.get(self._geocode_endpoint, params=self._params)
            return FeatureCollection(**response.json())

    async def get_async(self) -> FeatureCollection:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._geocode_endpoint, params=self._params
            )
            return FeatureCollection(**response.json())


class ReverseGeocodeRequest(BaseModel):
    geolocation: GeoLocation = Field(..., description="The geolocation to query for")
    lang: str | None = Field(
        default=None,
        description="Set preferred language (e.g. 'default', 'en', 'de', 'fr')",
    )
    limit: int | None = Field(default=None, description="The maximum number of results")
    _reverse_geocode_endpoint = f"{openepi_settings.api_root_url}/geocoding/reverse"

    @computed_field
    @property
    def _params(self) -> dict:
        return {
            k: v
            for k, v in {
                "lon": self.geolocation.lon,
                "lat": self.geolocation.lat,
                "lang": self.lang,
                "limit": self.limit,
            }.items()
            if v is not None
        }

    def get_sync(self) -> FeatureCollection:
        with Client() as client:
            response = client.get(self._reverse_geocode_endpoint, params=self._params)
            return FeatureCollection(**response.json())

    async def get_async(self) -> FeatureCollection:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._reverse_geocode_endpoint, params=self._params
            )
            return FeatureCollection(**response.json())


class GeocodeClient:
    @staticmethod
    def geocode(
        q: str,
        geolocation: GeoLocation | None = None,
        lang: str | None = None,
        limit: int | None = None,
    ) -> FeatureCollection:
        return GeocodeRequest(
            q=q, geolocation=geolocation, lang=lang, limit=limit
        ).get_sync()

    @staticmethod
    def reverse_geocode(
        geolocation: GeoLocation,
        lang: str | None = None,
        limit: int | None = None,
    ) -> FeatureCollection:
        return ReverseGeocodeRequest(
            geolocation=geolocation, lang=lang, limit=limit
        ).get_sync()


class AsyncGeocodeClient:
    @staticmethod
    async def geocode(
        q: str,
        geolocation: GeoLocation | None = None,
        lang: str | None = None,
        limit: int | None = None,
    ) -> FeatureCollection:
        return await GeocodeRequest(
            q=q, geolocation=geolocation, lang=lang, limit=limit
        ).get_async()

    @staticmethod
    async def reverse_geocode(
        geolocation: GeoLocation,
        lang: str | None = None,
        limit: int | None = None,
    ) -> FeatureCollection:
        return await ReverseGeocodeRequest(
            geolocation=geolocation, lang=lang, limit=limit
        ).get_async()
