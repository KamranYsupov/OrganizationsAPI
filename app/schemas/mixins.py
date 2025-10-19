import datetime
import uuid

from pydantic import BaseModel


class UUIDSchemaMixin:
    id: uuid.UUID


class TimeStampedSchemaMixin:
    created_at: datetime.datetime
    updated_at: datetime.datetime