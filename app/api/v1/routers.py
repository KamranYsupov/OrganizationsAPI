from fastapi import APIRouter

from app.api.v1.endpoints.organizations import (
    router as organizations_router
)


def get_api_router():
    api_router = APIRouter()

    api_router.include_router(organizations_router)

    return api_router




