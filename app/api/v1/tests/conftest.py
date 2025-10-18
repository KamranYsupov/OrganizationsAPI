from typing import Dict, List, Any, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.exc import OperationalError

from app.main import app
from app.core.config import settings
from app.db.manager import db_manager
from app.db.models import Base


@pytest.fixture(scope='function', autouse=True)
async def setup_db():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with db_manager.engine.begin() as conn:

        try:
            await conn.run_sync(Base.metadata.drop_all)
        except OperationalError:
            pass



@pytest.fixture(scope='function')
def fastapi_app() -> FastAPI:
    return app


@pytest.fixture(scope='function')
async def async_client(fastapi_app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
            transport=ASGITransport(app=fastapi_app),
            base_url=f'{settings.base_url}{settings.api_v1_prefix}',
    ) as ac:
        yield ac
