import uuid

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from starlette import status

from .base import CRUDBaseService
from app.repositories import RepositoryActivity
from ..db.models import Activity
from ..repositories.base import ModelType
from ..schemas.activity import ActivityCreateSchema


class ActivityService(CRUDBaseService[RepositoryActivity]):
    """Сервис для RepositoryActivity"""

    async def create(self, obj_in: ActivityCreateSchema) -> ModelType:

        if not obj_in.parent_id:
            return await super().create(obj_in)

        depth = await self._repository.get_activity_depth(
            activity_id=obj_in.parent_id
        )
        if depth == 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'Max depth exceeded',
            )
        return await super().create(obj_in)

    async def get_activity_tree(
            self,
            activity_id: uuid.UUID,
            max_depth: int = 3,
            current_depth: int = 0
    ):

        if current_depth > max_depth:
            return []

        activity = await self._repository.get(
            id=activity_id,
            options=[selectinload(Activity.children)]
        )

        if not activity:
            return []

        child_activities = []
        for child in activity.children:
            child_activities.extend(
            await self.get_activity_tree(
                activity_id=child.id,
                max_depth=max_depth,
                current_depth=current_depth + 1
            )
        )

        return [activity.id] + child_activities
