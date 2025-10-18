import datetime
import uuid

from pydantic import BaseModel


class UUIDSchemaMixin(BaseModel):
    id: uuid.UUID


class TimeStampedSchemaMixin(BaseModel):
    created_at: datetime.datetime
    updated_at: datetime.datetime