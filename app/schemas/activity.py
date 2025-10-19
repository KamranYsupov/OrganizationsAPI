import uuid
from uuid import UUID

from pydantic import BaseModel
from typing import List, Optional

from app.schemas.mixins import UUIDSchemaMixin


class ActivityBaseSchema(BaseModel):
    name: str


class ActivityCreateSchema(ActivityBaseSchema):
    parent_id: Optional[UUID] = None


class ActivitySchema(ActivityBaseSchema, UUIDSchemaMixin):
    id: uuid.UUID
    parent_id: Optional[int]
    children: List['ActivitySchema'] = []

    class Config:
        from_attributes = True




