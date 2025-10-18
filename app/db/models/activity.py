from typing import List, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.models import Base
from app.db.models.mixins import UUIDMixin
from app.db.models.organization import organization_activity


class Activity(Base, UUIDMixin):
    __tablename__ = 'activities'

    name: Mapped[str] = mapped_column(String, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('activities.id'),
        nullable=True
    )

    parent = relationship(
        'Activity',
        remote_side=[id],
        back_populates='children'
    )
    children = relationship(
        'Activity',
        back_populates='parent'
    )
    organizations = relationship(
        'Organization',
        secondary=organization_activity,
        back_populates='activities'
    )
