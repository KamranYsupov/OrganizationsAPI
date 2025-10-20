# services/geo_service.py
from math import radians, sin, cos, sqrt, atan2
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.db.models import Organization, Building
from app.schemas.geo_search import RectangleSearch, RadiusSearch


class GeoService:
    def __init__(
            self,
            session: AsyncSession,
    ) -> None:
        self._session = session

    @staticmethod
    def _calculate_distance(
            lat1: float,
            lon1: float,
            lat2: float,
            lon2: float
    ) -> float:
        """Расчет расстояния между двумя точками по формуле гаверсинуса (в км)"""
        R = 6371.0  # Радиус Земли в км

        lat1_rad = radians(lat1)
        lon1_rad = radians(lon1)
        lat2_rad = radians(lat2)
        lon2_rad = radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    async def search_in_radius(
            self,
            search: RadiusSearch,
            options: List[ExecutableOption] = [],
    ) -> List[Organization]:
        """
        Поиск организаций в радиусе от центральной точки
        """
        center_lat = search.latitude
        center_lon = search.longitude
        radius_km = search.radius_km

        # Быстрая предварительная фильтрация по прямоугольной области
        lat_degree_per_km = 1 / 111.0
        lon_degree_per_km = 1 / (111.0 * cos(radians(center_lat)))

        lat_offset = radius_km * lat_degree_per_km
        lon_offset = radius_km * lon_degree_per_km

        min_lat = center_lat - lat_offset
        max_lat = center_lat + lat_offset
        min_lon = center_lon - lon_offset
        max_lon = center_lon + lon_offset

        # Получаем организации в прямоугольной области
        statement = select(Organization).join(Building).where(
            Building.latitude.between(min_lat, max_lat),
            Building.longitude.between(min_lon, max_lon)
        ).options(*options)

        result = await self._session.execute(statement)
        candidates = result.scalars().all()

        # Точная фильтрация по расстоянию
        organizations_in_radius = []
        for org in candidates:
            distance = self._calculate_distance(
                center_lat, center_lon,
                org.building.latitude, org.building.longitude
            )
            if distance <= radius_km:
                organizations_in_radius.append(org)

        return organizations_in_radius

    async def search_in_rectangle(
            self,
            search: RectangleSearch,
            options: List[ExecutableOption] = [],
    ) -> List[Organization]:
        """
        Поиск организаций в прямоугольной области
        """
        statement = select(Organization).join(Building).where(
            Building.latitude.between(search.min_lat, search.max_lat),
            Building.longitude.between(search.min_lon, search.max_lon)
        ).options(*options)

        result = await self._session.execute(statement)
        return result.scalars().all()