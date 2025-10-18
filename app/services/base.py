import uuid
from uuid import UUID
from typing import (
    List,
    Tuple,
    Sequence,
    TypeVar,
    Type,
    Optional, Generic, Union,
)

from fastapi import HTTPException
from starlette import status

from app.repositories.base import ModelType

RepositoryType = TypeVar('RepositoryType')


class CRUDBaseService(Generic[RepositoryType, ]):
    """Класс с базовым CRUD для сервисов"""

    def __init__(
            self,
            repository: Type[RepositoryType],
            unique_fields: Optional[Sequence[str]] = None,
    ):
        self._repository = repository
        self.unique_fields = unique_fields

    async def get(self, **kwargs) -> ModelType:
        return await self.get_object_or_404(**kwargs)

    async def create(self, obj_in) -> ModelType:
        insert_data = await self.validate_object_insertion(obj_in)
        return await self._repository.create(
            insert_data=insert_data,
        )

    async def update(self, *, obj_id: UUID, obj_in) -> ModelType:
        await self.get_object_or_404(id=obj_id)
        insert_data = await self.validate_object_insertion(
            obj_in=obj_in,
            obj_to_update_id=obj_id,
        )
        return await self._repository.update(
            obj_id=obj_id,
            insert_data=insert_data,
        )

    async def list(
            self,
            *args,
            skip: Optional[int] = None,
            limit: Optional[int] = None,
            **kwargs
    ) -> list[ModelType]:
        return await self._repository.list(
            *args,
            skip=skip,
            limit=limit,
            **kwargs
        )

    async def delete(self, obj_id: UUID) -> None:
        await self.get_object_or_404(id=obj_id)
        return await self._repository.delete(id=obj_id)

    async def exists(self, *args, **kwargs) -> Optional[ModelType]:
        return await self._repository.exists(*args, **kwargs)

    async def validate_object_insertion(
            self,
            obj_in,
            obj_to_update_id: Optional[Union[uuid.UUID, str]] = None
    ) -> dict:
        insert_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump()
        if not self.unique_fields:
            return insert_data

        unique_kwargs = {
            field: insert_data.get(field) for field in self.unique_fields
        }
        conditions: List[bool] = [
            getattr(self._repository.model, field) == value
            for field, value in unique_kwargs.items()
        ]

        existing_obj = await self._repository.exists(*conditions)
        if existing_obj and existing_obj.id != obj_to_update_id:
            formatted_fields_string = ' or '.join(self.unique_fields).capitalize()
            exception_detail = f'{formatted_fields_string} is already taken'

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=exception_detail
            )

        return insert_data

    async def get_object_or_404(self, **kwargs):
        obj = await self._repository.get(**kwargs)

        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return obj

