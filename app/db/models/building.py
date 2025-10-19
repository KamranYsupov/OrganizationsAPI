from typing import List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.models import Base
from app.db.models.mixins import UUIDMixin
from app.db.models.organization import organization_building


class Building(Base, UUIDMixin):
    address: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    organizations = relationship(
        'Organization',
        secondary=organization_building,
        back_populates='buildings'
    )
