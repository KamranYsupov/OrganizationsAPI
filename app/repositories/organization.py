from app.db.models import Organization, Phone
from app.repositories.base import RepositoryBase


class RepositoryOrganization(RepositoryBase[Organization]):
    """Репозиторий модели Organization"""
    pass

class RepositoryPhone(RepositoryBase[Phone]):
    """Репозиторий модели Phone"""
    pass