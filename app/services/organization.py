import math
import uuid
from typing import List, Optional

import loguru
from fastapi import HTTPException
from sqlalchemy.sql.base import ExecutableOption
from starlette import status

from .base import CRUDBaseService, RepositoryType
from app.repositories import (
    RepositoryOrganization,
    RepositoryPhone,
    RepositoryActivity,
    RepositoryBuilding,
)
from ..db.models import Activity, Building, Organization
from ..repositories.base import ModelType
from ..schemas.organization import OrganizationCreateSchema, PhoneCreateSchema


class OrganizationService(CRUDBaseService[RepositoryOrganization]):
    """Сервис для RepositoryOrganization"""

    def __init__(
            self,
            repository_organization: RepositoryOrganization,
            repository_phone: RepositoryPhone,
            repository_activity: RepositoryActivity,
            repository_building: RepositoryBuilding,

    ):
        super().__init__(repository=repository_organization)
        self._repository_organization = repository_organization
        self._repository_phone = repository_phone
        self._repository_activity = repository_activity
        self._repository_building = repository_building


    async def create(self, obj_in: OrganizationCreateSchema) -> Organization:
        insert_data = await self.validate_object_insertion(obj_in)

        activities = await self.validate_activity_ids(obj_in.activity_ids)
        await self.validate_building_id(obj_in.building_id)

        insert_data.pop('activity_ids')
        insert_data.pop('phones')

        organization = await self._repository_organization.create(
            insert_data=insert_data,
        )

        if activities:
            await self._repository_organization.bulk_add_activities_to_organization(
                organization_id=organization.id,
                activity_ids=obj_in.activity_ids
            )

        if obj_in.phones:
            await self._repository_phone.bulk_create(
                organization_id=organization.id,
                phones=obj_in.phones
            )

        return organization

    async def validate_activity_ids(
            self,
            activity_ids: List[str | uuid.UUID]
    ) -> List[Activity]:
        requested_ids = set(str(activity_id) for activity_id in activity_ids)

        activities = await self._repository_activity.list(
            Activity.id.in_(activity_ids)
        )

        found_ids = set(str(activity.id) for activity in activities)
        missing_ids = requested_ids - found_ids

        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Activities with ids {list(missing_ids)} do not exist',
            )

        return activities

    async def validate_building_id(
            self,
            building_id: str | uuid.UUID
    ) -> Building:
        building = await self._repository_building.get(id=building_id)

        if not building:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Building with id {str(building_id)} do not exist',
            )

        return building

    async def get_organizations_by_activity_id(
            self,
            activity_id: uuid.UUID,
            options: List[ExecutableOption] = [],
            **kwargs,
    ) -> List[Organization]:
        return await self._repository_organization.get_organizations_by_activity_id(
            activity_id=activity_id,
            options=options,
            **kwargs
        )

    async def get_organizations_by_activity_ids(
            self,
            activity_ids: List[uuid.UUID],
            options: List[ExecutableOption] = [],
            **kwargs,
    ) -> List[Organization]:
        return await self._repository_organization.get_organizations_by_activity_ids(
            activity_ids=activity_ids,
            options=options,
            **kwargs
        )

    async def get_organizations_in_area(
            self,
            latitude: float,
            longitude: float,
            radius_km: Optional[float] = None,
            min_lat: Optional[float] = None,
            max_lat: Optional[float] = None,
            min_lon: Optional[float] = None,
            max_lon: Optional[float] = None,
    ):
        buildings_in_area = await self._repository_building.list()

        if radius_km:
            # Поиск в радиусе (упрощенная формула гаверсинуса)
            earth_radius = 6371  # km
            lat_rad = math.radians(latitude)
            lon_rad = math.radians(longitude)

            # Простая аппроксимация для небольшой области
            lat_diff = radius_km / 111.0
            lon_diff = radius_km / (111.0 * math.cos(lat_rad))

            buildings_in_area = await self._repository_building.list(
                Building.latitude.between(
                    latitude - lat_diff,
                    latitude + lat_diff
                ),
                Building.longitude.between(
                    longitude - lon_diff,
                    longitude + lon_diff
                )
            )
            query = query.join(models.Building).filter(

            )
        else:
            # Поиск в прямоугольной области
            query = query.join(models.Building).filter(
                models.Building.latitude.between(min_lat, max_lat),
                models.Building.longitude.between(min_lon, max_lon)
            )

        return query.all()

class PhoneService(CRUDBaseService[RepositoryPhone]):
    """Сервис для RepositoryPhone"""

    def __init__(self, repository: RepositoryPhone):
        super().__init__(repository)
        self._repository = repository

    async def bulk_create(
            self,
            objects_in: List[PhoneCreateSchema],
            returning: bool = False,
    ):
        return await self._repository.bulk_create(
            objects_in=objects_in,
            returning=returning
        )