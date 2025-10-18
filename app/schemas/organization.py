from typing import List, Optional

from pydantic import BaseModel

from app.schemas.activity import ActivitySchema
from app.schemas.building import BuildingSchema
from app.schemas.mixins import UUIDSchemaMixin


class PhoneBaseSchema(BaseModel):
    number: str


class PhoneCreateSchema(PhoneBaseSchema):
    pass


class PhoneSchema(PhoneBaseSchema, UUIDSchemaMixin):

    class Config:
        orm_mode = True


class OrganizationBaseSchema(BaseModel):
    name: str
    building_id: int


class OrganizationCreateSchema(OrganizationBaseSchema):
    activity_ids: List[int] = []
    phones: List[str] = []


class OrganizationSchema(OrganizationBaseSchema, UUIDSchemaMixin):
    building: BuildingSchema
    activities: List[ActivitySchema] = []
    phones: List[PhoneSchema] = []

    class Config:
        orm_mode = True


class OrganizationShortSchema(BaseModel, UUIDSchemaMixin):
    name: str

    class Config:
        orm_mode = True


class BuildingWithOrganizationsSchema(BuildingSchema):
    organizations: List[OrganizationShortSchema] = []


class ActivityWithOrganizationsSchema(ActivitySchema):
    organizations: List[OrganizationShortSchema] = []


class GeoSearchSchema(BaseModel):
    latitude: float
    longitude: float
    radius_km: Optional[float] = None
    min_lat: Optional[float] = None
    max_lat: Optional[float] = None
    min_lon: Optional[float] = None
    max_lon: Optional[float] = None