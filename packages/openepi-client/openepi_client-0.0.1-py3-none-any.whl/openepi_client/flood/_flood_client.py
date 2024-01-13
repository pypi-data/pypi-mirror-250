from datetime import datetime

from httpx import AsyncClient, Client
from pydantic import BaseModel, Field, model_validator, computed_field

from openepi_client import openepi_settings, BoundingBox, GeoLocation
from openepi_client.flood._flood_types import (
    ThresholdResponseModel,
    SummaryResponseModel,
    DetailedResponseModel,
)


class ThresholdRequest(BaseModel):
    geolocation: GeoLocation | None = Field(
        default=None, description="The geolocation to query for"
    )

    bounding_box: BoundingBox | None = Field(
        default=None, description="The bounding box to query for"
    )

    _threshold_endpoint: str = f"{openepi_settings.api_root_url}/flood/threshold"

    @model_validator(mode="after")
    def check_mutually_exclusive(self) -> "ThresholdRequest":
        if not (self.geolocation is not None) ^ (self.bounding_box is not None):
            raise ValueError("Either specify a geolocation or a boundingbox.")

        return self

    @computed_field
    @property
    def _params(self) -> dict:
        if self.geolocation:
            return {"lat": self.geolocation.lat, "lon": self.geolocation.lon}
        else:
            return {
                "min_lat": self.bounding_box.min_lat,
                "max_lat": self.bounding_box.max_lat,
                "min_lon": self.bounding_box.min_lon,
                "max_lon": self.bounding_box.max_lon,
            }

    def get_sync(self) -> ThresholdResponseModel:
        with Client() as client:
            response = client.get(self._threshold_endpoint, params=self._params)
            return ThresholdResponseModel(**response.json())

    async def get_async(self) -> ThresholdResponseModel:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._threshold_endpoint, params=self._params
            )
            return ThresholdResponseModel(**response.json())


class SummaryRequest(BaseModel):
    geolocation: GeoLocation | None = Field(
        default=None, description="The geolocation to query for"
    )

    bounding_box: BoundingBox | None = Field(
        default=None, description="The bounding box to query for"
    )

    _summary_endpoint: str = f"{openepi_settings.api_root_url}/flood/summary"

    @model_validator(mode="after")
    def check_mutually_exclusive(self) -> "SummaryRequest":
        if not (self.geolocation is not None) ^ (self.bounding_box is not None):
            raise ValueError("Either specify a geolocation or a boundingbox.")

        return self

    @computed_field
    @property
    def _params(self) -> dict:
        if self.geolocation:
            return {"lat": self.geolocation.lat, "lon": self.geolocation.lon}
        else:
            return {
                "min_lat": self.bounding_box.min_lat,
                "max_lat": self.bounding_box.max_lat,
                "min_lon": self.bounding_box.min_lon,
                "max_lon": self.bounding_box.max_lon,
            }

    def get_sync(self) -> SummaryResponseModel:
        with Client() as client:
            response = client.get(self._summary_endpoint, params=self._params)
            return SummaryResponseModel(**response.json())

    async def get_async(self) -> SummaryResponseModel:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._summary_endpoint, params=self._params
            )
            return SummaryResponseModel(**response.json())


class DetailedRequest(BaseModel):
    geolocation: GeoLocation | None = Field(
        default=None, description="The geolocation to query for"
    )

    bounding_box: BoundingBox | None = Field(
        default=None, description="The bounding box to query for"
    )

    include_neighbours: bool | None = Field(
        default=False, description="Whether to include neighbouring locations"
    )

    start_date: datetime | None = Field(
        default=None, description="The start date of the query"
    )

    end_date: datetime | None = Field(
        default=None, description="The end date of the query"
    )

    _detailed_endpoint: str = f"{openepi_settings.api_root_url}/flood/detailed"

    @model_validator(mode="after")
    def check_mutually_exclusive(self) -> "DetailedRequest":
        if not (self.geolocation is not None) ^ (self.bounding_box is not None):
            raise ValueError("Either specify a geolocation or a boundingbox.")

        return self

    @computed_field
    @property
    def _params(self) -> dict:
        params = {
            "include_neighbours": self.include_neighbours,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }
        if self.geolocation:
            params.update({"lat": self.geolocation.lat, "lon": self.geolocation.lon})
        else:
            params.update(
                {
                    "min_lat": self.bounding_box.min_lat,
                    "max_lat": self.bounding_box.max_lat,
                    "min_lon": self.bounding_box.min_lon,
                    "max_lon": self.bounding_box.max_lon,
                }
            )
        return {k: v for k, v in params.items() if v is not None}

    def get_sync(self) -> DetailedResponseModel:
        with Client() as client:
            response = client.get(
                self._detailed_endpoint,
                params=self._params,
            )
            return DetailedResponseModel(**response.json())

    async def get_async(self) -> DetailedResponseModel:
        async with AsyncClient() as async_client:
            response = await async_client.get(
                self._detailed_endpoint,
                params=self._params,
            )
            return DetailedResponseModel(**response.json())


class FloodClient:
    @staticmethod
    def get_threshold(
        geolocation: GeoLocation | None = None, bounding_box: BoundingBox | None = None
    ) -> ThresholdResponseModel:
        return ThresholdRequest(
            geolocation=geolocation, bounding_box=bounding_box
        ).get_sync()

    @staticmethod
    def get_summary(
        geolocation: GeoLocation | None = None, bounding_box: BoundingBox | None = None
    ) -> SummaryResponseModel:
        return SummaryRequest(
            geolocation=geolocation, bounding_box=bounding_box
        ).get_sync()

    @staticmethod
    def get_detailed(
        geolocation: GeoLocation | None = None,
        bounding_box: BoundingBox | None = None,
        include_neighbours: bool | None = False,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> DetailedResponseModel:
        return DetailedRequest(
            geolocation=geolocation,
            bounding_box=bounding_box,
            include_neighbours=include_neighbours,
            start_date=start_date,
            end_date=end_date,
        ).get_sync()


class AsyncFloodClient:
    @staticmethod
    async def get_threshold(
        geolocation: GeoLocation | None = None, bounding_box: BoundingBox | None = None
    ) -> ThresholdResponseModel:
        return await ThresholdRequest(
            geolocation=geolocation, bounding_box=bounding_box
        ).get_async()

    @staticmethod
    async def get_summary(
        geolocation: GeoLocation | None = None, bounding_box: BoundingBox | None = None
    ) -> SummaryResponseModel:
        return await SummaryRequest(
            geolocation=geolocation, bounding_box=bounding_box
        ).get_async()

    @staticmethod
    async def get_detailed(
        geolocation: GeoLocation | None = None,
        bounding_box: BoundingBox | None = None,
        include_neighbours: bool | None = False,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
    ) -> DetailedResponseModel:
        return await DetailedRequest(
            geolocation=geolocation,
            bounding_box=bounding_box,
            include_neighbours=include_neighbours,
            start_date=start_date,
            end_date=end_date,
        ).get_async()
