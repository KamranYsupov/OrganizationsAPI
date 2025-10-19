from typing import List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.models import Base
from app.db.models.mixins import UUIDMixin

organization_activity = Table(
    'organization_activity',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('activity_id', Integer, ForeignKey('activities.id'))
)
organization_building = Table(
    'organization_building',
    Base.metadata,
    Column('organization_id', Integer, ForeignKey('organizations.id')),
    Column('building_id', Integer, ForeignKey('buildings.id'))
)


class Organization(Base, UUIDMixin):
    name: Mapped[str] = mapped_column(String, nullable=False)
    building_id: Mapped[int] = mapped_column(Integer, ForeignKey('buildings.id'))

    buildings = relationship(
        'Building',
        secondary=organization_building,
        back_populates='organizations'
    )
    activities = relationship(
        'Activity',
        secondary=organization_activity,
        back_populates='organizations'
    )
    phones = relationship('Phone', back_populates='organization')


class Phone(Base, UUIDMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String, nullable=False)
    organization_id: Mapped[int] = mapped_column(Integer, ForeignKey('organizations.id'))

    organization = relationship('Organization', back_populates='phones')
