from pydantic_settings import BaseSettings
from pydantic import BaseModel, Field


class OpenEpiSettings(BaseSettings):
    api_root_url: str = "https://api-test.openepi.io"


openepi_settings = OpenEpiSettings()


class GeoLocation(BaseModel):
    lat: float = Field(..., description="Latitude of the location")
    lon: float = Field(..., description="Longitude of the location")
    alt: float | None = Field(default=None, description="Altitude of the location")


class BoundingBox(BaseModel):
    min_lat: float = Field(..., description="Minimum latitude of the bounding box")
    max_lat: float = Field(..., description="Maximum latitude of the bounding box")
    min_lon: float = Field(..., description="Minimum longitude of the bounding box")
    max_lon: float = Field(..., description="Maximum longitude of the bounding box")
