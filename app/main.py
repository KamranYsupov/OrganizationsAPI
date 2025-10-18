import loguru
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.api.v1 import routers
from app.core.config import settings
from app.core.container import Container


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title=settings.project_name,
        default_response_class=ORJSONResponse,
    )
    container = Container()
    container.wire(modules=settings.container_wiring_modules)
    fastapi_app.container = container

    api_router = routers.get_api_router()
    fastapi_app.include_router(api_router, prefix=settings.api_v1_prefix)

    return fastapi_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app='app.main:app', host='0.0.0.0', reload=True)