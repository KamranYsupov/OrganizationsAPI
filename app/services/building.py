from .base import CRUDBaseService
from app.repositories import (
    RepositoryBuilding,
)


class BuildingService(CRUDBaseService[RepositoryBuilding]):
    """Сервис для RepositoryBuilding"""
    pass