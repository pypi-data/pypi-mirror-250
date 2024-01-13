import httpx
from pydantic import BaseModel, Field, computed_field, model_validator
from httpx import AsyncClient, Client

from openepi_client import openepi_settings, GeoLocation, BoundingBox
from openepi_client.deforestation._deforestation_types import DeforestationBasinGeoJSON


class BasinRequest(BaseModel):
    geolocation: GeoLocation | None = Field(
        default=None, description="The geolocation to query for"
    )

    bounding_box: BoundingBox | None = Field(
        default=None, description="The bounding box to query for"
    )

    start_year: int | None = Field(
        default=None, description="The start year to query for"
    )

    end_year: int | None = Field(default=None, description="The end year to query for")

    _basin_endpoint: str = f"{openepi_settings.api_root_url}/deforestation/basin"

    @model_validator(mode="after")
    def check_mutually_exclusive(self) -> "BasinRequest":
        if not (self.geolocation is not None) ^ (self.bounding_box is not None):
            raise ValueError("Either specify a geolocation or a boundingbox.")

        return self

    @computed_field
    @property
    def _params(self) -> dict:
        if self.geolocation:
            p = {
                "lat": self.geolocation.lat,
                "lon": self.geolocation.lon,
                "start_year": self.start_year,
                "end_year": self.end_year,
            }
        else:
            p = {
                "min_lat": self.bounding_box.min_lat,
                "max_lat": self.bounding_box.max_lat,
                "min_lon": self.bounding_box.min_lon,
                "max_lon": self.bounding_box.max_lon,
                "start_year": self.start_year,
                "end_year": self.end_year,
            }

        return {k: v for k, v in p.items() if v is not None}

    def get_sync(self) -> DeforestationBasinGeoJSON:
        with Client() as client:
            response = client.get(
                self._basin_endpoint, params=self._params, timeout=httpx.Timeout(None)
            )
            return DeforestationBasinGeoJSON(**response.json())

    async def get_async(self) -> DeforestationBasinGeoJSON:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._basin_endpoint,
                params=self._params,
                timeout=httpx.Timeout(None),
            )
            return DeforestationBasinGeoJSON(**response.json())


class DeforestationClient:
    @staticmethod
    def get_basin(
        geolocation: GeoLocation | None = None,
        bounding_box: BoundingBox | None = None,
        start_year: int | None = None,
        end_year: int | None = None,
    ) -> DeforestationBasinGeoJSON:
        return BasinRequest(
            geolocation=geolocation,
            bounding_box=bounding_box,
            start_year=start_year,
            end_year=end_year,
        ).get_sync()


class AsyncDeforestationClient:
    @staticmethod
    async def get_basin(
        geolocation: GeoLocation | None = None,
        bounding_box: BoundingBox | None = None,
        start_year: int | None = None,
        end_year: int | None = None,
    ) -> DeforestationBasinGeoJSON:
        return await BasinRequest(
            geolocation=geolocation,
            bounding_box=bounding_box,
            start_year=start_year,
            end_year=end_year,
        ).get_async()
