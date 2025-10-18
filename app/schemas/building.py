from pydantic import BaseModel

from app.schemas.mixins import UUIDSchemaMixin


class BuildingBaseSchema(BaseModel):
    address: str
    latitude: float
    longitude: float


class BuildingCreateSchema(BuildingBaseSchema):
    pass


class BuildingSchema(BuildingBaseSchema, UUIDSchemaMixin):

    class Config:
        orm_mode = True
