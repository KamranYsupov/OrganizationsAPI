import uuid

from pydantic import BaseModel
from typing import List, Optional

from app.schemas.mixins import UUIDSchemaMixin


class ActivityBaseSchema(BaseModel):
    name: str


class ActivityCreateSchema(ActivityBaseSchema):
    parent_id: Optional[uuid.UUID] = None


class ActivitySchema(ActivityBaseSchema, UUIDSchemaMixin):
    parent_id: Optional[uuid.UUID]
    children: List['ActivitySchema'] = []

    class Config:
        from_attributes = True




