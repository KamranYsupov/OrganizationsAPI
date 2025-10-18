from .base import CRUDBaseService
from app.repositories import (
    RepositoryOrganization,
    RepositoryPhone
)


class OrganizationService(CRUDBaseService[RepositoryOrganization]):
    """Сервис для RepositoryOrganization"""
    pass

class PhoneService(CRUDBaseService[RepositoryPhone]):
    """Сервис для RepositoryPhone"""
    pass