import uuid
from typing import Type, List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Organization, Phone
from app.db.models.organization import OrganizationActivity
from app.repositories.base import RepositoryBase, ModelType
from app.schemas.organization import PhoneCreateSchema
from app.db.models import Activity
from app.repositories.base import RepositoryBase


class RepositoryActivity(RepositoryBase[Activity]):
    """Репозиторий модели Activity"""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        super().__init__(model, session)

    async def get_activity_depth(self, activity_id: uuid.UUID) -> int:
        """Рекурсивно вычисляет глубину"""
        depth = 0
        current_id = activity_id

        while current_id:
            statement = select(Activity).where(Activity.id == current_id)
            result = await self._session.execute(statement)
            activity: Activity = result.scalar_one_or_none()

            if not activity:
                break

            depth += 1
            if not activity.parent_id:
                break

            current_id = activity.parent_id

            if depth > 10:
                break

        return depth