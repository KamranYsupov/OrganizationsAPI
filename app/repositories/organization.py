import uuid
from typing import Type, List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.db.models import Organization, Phone, Activity
from app.db.models.organization import OrganizationActivity
from app.repositories.base import RepositoryBase, ModelType


class RepositoryOrganization(RepositoryBase[Organization]):
    """Репозиторий модели Organization"""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        super().__init__(model, session)

    async def bulk_add_activities_to_organization(
            self,
            organization_id: uuid.UUID,
            activity_ids: List[uuid.UUID],
    ):
        organization_activities_data = [
            {'organization_id': organization_id, 'activity_id': activity_id}
            for activity_id in activity_ids
        ]

        statement = insert(OrganizationActivity)
        await self._session.execute(statement, organization_activities_data)


    async def get_organizations_by_activity_id(
            self,
            activity_id: uuid.UUID,
            options: List[ExecutableOption] = [],
            **kwargs,

    ) -> List[Organization]:
        """Получает организации по ID деятельности"""
        statement = (
            select(Organization)
            .options(*options)
            .join(Organization.activities)
            .where(Activity.id == activity_id)
            .filter_by(**kwargs)
        )
        result = await self._session.execute(statement)
        organizations = result.scalars().all()
        return organizations


    async def get_organizations_by_activity_ids(
            self,
            activity_ids: List[uuid.UUID],
            options: List[ExecutableOption] = [],
            **kwargs,

    ) -> List[Organization]:
        """Получает организации по ID деятельности"""
        statement = (
            select(Organization)
            .options(*options)
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
            .filter_by(**kwargs)
        )
        result = await self._session.execute(statement)
        organizations = result.scalars().all()
        return organizations



class RepositoryPhone(RepositoryBase[Phone]):
    """Репозиторий модели Phone"""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        super().__init__(model, session)

    async def bulk_create(
            self,
            organization_id: uuid.UUID,
            phones: List[str],
            returning: bool = False,
    ):
        phones_schemas = [
            {'organization_id': organization_id, 'number': phone_number}
            for phone_number in phones
        ]
        statement = insert(Phone)

        if returning:
            statement = statement.returning(Phone)

        result = await self._session.execute(statement, phones_schemas)

        if returning:
            return result.scalars().all()


