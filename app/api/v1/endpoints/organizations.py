import math
from typing import List, Optional
from uuid import UUID

import loguru
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from sqlalchemy.orm import joinedload, selectinload

from app.api.v1.deps import verify_api_key
from app.core.container import Container
from app.db.models import Activity, Organization, Phone, Building
from app.db.transaction import atomic
from app.schemas.geo_search import RectangleSearch, RadiusSearch
from app.schemas.organization import (
    OrganizationSchema,
    OrganizationCreateSchema,
    OrganizationShortSchema,
)
from app.schemas.building import (
    BuildingSchema,
    BuildingCreateSchema,
)
from app.schemas.activity import (
    ActivitySchema,
    ActivityCreateSchema,
)
from app.services import OrganizationService, ActivityService, BuildingService
from app.services.geo_search import GeoService

router = APIRouter(
    prefix='/organizations'
)

@router.get('/by-activity')
@inject
@atomic
async def get_organizations_by_activity(
        activity_id: Optional[UUID],
        organization_service: OrganizationService = Depends(
            Provide[Container.organization_service]
        ),
        api_key=Depends(verify_api_key),
) -> List[OrganizationShortSchema]:

    organizations = await organization_service.get_organizations_by_activity_id(
        activity_id=activity_id
    )

    return organizations


@router.get('/by-building')
@inject
@atomic
async def get_organizations_by_building(
        building_id: Optional[UUID] = None,
        organization_service: OrganizationService = Depends(
            Provide[Container.organization_service]
        ),
        api_key=Depends(verify_api_key),
) -> List[OrganizationShortSchema]:
    organizations = await organization_service.list(
        building_id=building_id
    )

    return organizations


@router.get('/by-activity-tree')
@inject
async def search_organizations_by_activity_tree(
        activity_id: UUID,
        organization_service: OrganizationService = Depends(
            Provide[Container.organization_service]
        ),
        activity_service: ActivityService = Depends(
            Provide[Container.activity_service]
        ),
        api_key=Depends(verify_api_key),

) -> List[OrganizationShortSchema]:
    activity_ids = await activity_service.get_activity_tree(
        activity_id=activity_id
    )
    organizations = await organization_service.get_organizations_by_activity_ids(
        activity_ids=activity_ids,
        options=[
            joinedload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones),
        ]
    )
    return organizations


@router.get('/{organization_id}')
@inject
async def get_organization(
        organization_id: UUID,
        organization_service: OrganizationService = Depends(
            Provide[Container.organization_service]
        ),
        api_key = Depends(verify_api_key),
) -> OrganizationSchema:
    organization = await organization_service.get_object_or_404(
        id=organization_id,
        options=[
            joinedload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones),
        ]
    )
    organization_schema = organization.serialize(
        schema_class=OrganizationSchema,
        exclude_fields=('phones', )
    )
    phones = [phone.number for phone in organization.phones]
    organization_schema.phones = phones

    return organization_schema


@router.post(
    '/search/radius',
    summary='Поиск организаций в радиусе',
    description=(
        'Находит все организации, '
        'находящиеся в заданном радиусе от указанной точки'
    )
)
@inject
async def search_organizations_in_radius(
        search: RadiusSearch,
        geo_service: GeoService = Depends(
            Provide[Container.geo_service]
        ),
        api_key=Depends(verify_api_key),
) -> List[OrganizationSchema]:
    """
    Поиск организаций в радиусе от точки на карте
    """

    organizations = await geo_service.search_in_radius(
        search,
        options=[
            joinedload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones),
        ]
    )

    return organizations


@router.post(
    '/search/rectangle',
    summary='Поиск организаций в прямоугольной области',
    description=(
        'Находит все организации, '
        'находящиеся в заданной прямоугольной области на карте'
    )
)
@inject
async def search_organizations_in_rectangle(
        search: RectangleSearch,
        geo_service: GeoService = Depends(
            Provide[Container.geo_service]
        ),
        api_key=Depends(verify_api_key),
) -> List[OrganizationSchema]:
    """
    Поиск организаций в прямоугольной области на карте
    """

    organizations = await geo_service.search_in_rectangle(
        search,
        options=[
            joinedload(Organization.building),
            selectinload(Organization.activities),
            selectinload(Organization.phones),
        ]
    )

    return organizations


@router.post('')
@inject
@atomic
async def create_organization(
        organization_create_schema: OrganizationCreateSchema,
        organization_service: OrganizationService = Depends(
            Provide[Container.organization_service]
        ),
        api_key=Depends(verify_api_key),
) -> OrganizationShortSchema:
    organization: Organization = await organization_service.create(
        organization_create_schema
    )

    return organization


@router.post('/activities/')
@inject
@atomic
async def create_activity(
        activity_create_schema: ActivityCreateSchema,
        organization_service: OrganizationService = Depends(
            Provide[Container.organization_service]
        ),
        activity_service: ActivityService = Depends(
            Provide[Container.activity_service]
        ),
        api_key=Depends(verify_api_key),
) -> ActivitySchema:
    activity = await activity_service.create(activity_create_schema)

    return activity


@router.post('/buildings/')
@inject
@atomic
async def create_building(
        building: BuildingCreateSchema,
        building_service: BuildingService = Depends(
            Provide[Container.building_service]
        ),
        api_key=Depends(verify_api_key),
) -> BuildingSchema:
    created_building = await building_service.create(building)

    return created_building


