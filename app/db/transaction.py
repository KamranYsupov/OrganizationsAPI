from functools import wraps

from dependency_injector.wiring import inject, Provide
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container


@inject
def atomic(func):
    @wraps(func)
    @inject
    async def wrapper(
            session: AsyncSession = Depends(Provide[Container.session]),
            *args,
            **kwargs
    ):
        try:
            result = await func(*args, **kwargs)
            await session.commit()
            return result
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

    return wrapper