from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class RadiusSearch(BaseModel):
    """Схема для поиска в радиусе"""
    latitude: float = Field(
        ge=-90,
        le=90,
        description="Широта центра поиска",
        examples=[55.7520]
    )
    longitude: float = Field(
        ge=-180,
        le=180,
        description="Долгота центра поиска",
        examples=[37.6175]
    )
    radius_km: float = Field(
        gt=0,
        le=100,
        description="Радиус поиска в километрах (максимум 100 км)",
        examples=[5.0]
    )

    @field_validator('radius_km')
    @classmethod
    def validate_radius(cls, v):
        if v > 100:
            raise ValueError('Максимальный радиус поиска - 100 км')
        return v

class RectangleSearch(BaseModel):
    """Схема для поиска в прямоугольной области"""
    min_lat: float = Field(
        ge=-90,
        le=90,
        description="Минимальная широта",
        examples=[55.5731]
    )
    max_lat: float = Field(
        ge=-90,
        le=90,
        description="Максимальная широта",
        examples=[55.9100]
    )
    min_lon: float = Field(
        ge=-180,
        le=180,
        description="Минимальная долгота",
        examples=[37.3696]
    )
    max_lon: float = Field(
        ge=-180,
        le=180,
        description="Максимальная долгота",
        examples=[37.8553]
    )

    @field_validator('max_lat')
    @classmethod
    def validate_lat_bounds(cls, v, info):
        if 'min_lat' in info.data and info.data['min_lat'] >= v:
            raise ValueError("min_lat должен быть меньше max_lat")
        return v

    @field_validator('max_lon')
    @classmethod
    def validate_lon_bounds(cls, v, info):
        if 'min_lon' in info.data and info.data['min_lon'] >= v:
            raise ValueError("min_lon должен быть меньше max_lon")
        return v