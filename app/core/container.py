from dependency_injector import containers, providers

from app.db import DataBaseManager
from app.core.config import settings
from app.repositories import (
    RepositoryPhone,
    RepositoryActivity,
    RepositoryBuilding,
    RepositoryOrganization
)
from app.services import (
    PhoneService,
    OrganizationService,
    ActivityService,
    BuildingService
)
from app.db.models import (
    Phone,
    Organization,
    Building,
    Activity,
)
from app.services.geo_search import GeoService


class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_phone = providers.Factory(
        RepositoryPhone,
        model=Phone,
        session=session,
    )
    repository_organization = providers.Factory(
        RepositoryOrganization,
        model=Organization,
        session=session,
    )
    repository_activity = providers.Factory(
        RepositoryActivity,
        model=Activity,
        session=session,
    )
    repository_building = providers.Factory(
        RepositoryBuilding,
        model=Building,
        session=session,
    )
    # endregion

    # region services
    phone_service = providers.Factory(
        PhoneService,
        repository=repository_phone,
    )
    organization_service = providers.Factory(
        OrganizationService,
        repository_organization=repository_organization,
        repository_phone=repository_phone,
        repository_activity=repository_activity,
        repository_building=repository_building
    )
    activity_service = providers.Factory(
        ActivityService,
        repository=repository_activity,
    )
    building_service = providers.Factory(
        BuildingService,
        repository=repository_building,
        unique_fields=('address', )
    )
    geo_service = providers.Factory(
        GeoService,
        session=session
    )
    # endregion



