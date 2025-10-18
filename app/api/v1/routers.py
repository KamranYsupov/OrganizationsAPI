from fastapi import APIRouter

from app.api.v1.endpoints.task import router as task_router


def get_api_router():
    api_router = APIRouter()

    api_router.include_router(task_router)

    return api_router




