import uuid
from typing import List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.models import Base
from app.db.models.mixins import UUIDMixin


class OrganizationActivity(Base, UUIDMixin):
    __tablename__ = 'organization_activity'
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('organizations.id'))
    activity_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('activities.id'))


class Organization(Base, UUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('buildings.id'))

    building = relationship(
        'Building',
        back_populates='organizations'
    )
    activities = relationship(
        'Activity',
        secondary='organization_activity',
        back_populates='organizations'
    )
    phones = relationship('Phone', back_populates='organization')


class Phone(Base, UUIDMixin):
    number: Mapped[str] = mapped_column(String, nullable=False)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('organizations.id'))

    organization = relationship('Organization', back_populates='phones')
