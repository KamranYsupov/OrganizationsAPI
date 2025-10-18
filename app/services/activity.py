from .base import CRUDBaseService
from app.repositories import RepositoryActivity


class ActivityService(CRUDBaseService[RepositoryActivity]):
    """Сервис для RepositoryActivity"""
    pass