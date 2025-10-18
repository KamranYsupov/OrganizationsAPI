import copy
from typing import Dict, Sequence, TypeVar, Optional, Type, Union

from sqlalchemy import func, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from app.core.config import settings

SchemaType = TypeVar('SchemaType')


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.metadata_naming_convention
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'

    def serialize(
            self,
            schema_class,
            model_dump: bool = False,
            exclude_fields: Sequence[str] = [],
    ) -> Optional[Union[Dict, SchemaType]]:
        serialized_data = {}
        schema_fields = schema_class.model_fields.keys()
        data = copy.deepcopy(self.__dict__)

        for field in schema_fields:
            serialized_data[field] = data.get(field)

        if not exclude_fields:
            return self.get_serialized(
                schema_class,
                serialized_data,
                model_dump,
            )

        for field in exclude_fields:
            serialized_data.pop(field)

        return self.get_serialized(
            schema_class,
            serialized_data,
            model_dump,
        )

    @staticmethod
    def get_serialized(
            schema_class,
            serialized_data: Dict,
            model_dump: bool = False,
    ):
        if model_dump:
            return serialized_data

        return schema_class(**serialized_data)

