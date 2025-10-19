from typing import List, Optional
from uuid import UUID

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
        from_attributes = True


class OrganizationBaseSchema(BaseModel):
    name: str


class OrganizationCreateSchema(OrganizationBaseSchema):
    activity_ids: List[UUID] = []
    building_id: UUID
    phones: List[str] = []


class OrganizationSchema(OrganizationBaseSchema, UUIDSchemaMixin):
    buildings: List[BuildingSchema]
    activities: List[ActivitySchema] = []
    phones: List[PhoneSchema] = []

    class Config:
        from_attributes = True


class OrganizationShortSchema(BaseModel, UUIDSchemaMixin):
    name: str

    class Config:
        from_attributes = True


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