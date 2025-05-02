from http import HTTPStatus
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if session.session_factory_cache is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="impossible to create session")

    async with session.session_factory_cache() as db_session:
        try:
            yield db_session
        except Exception as exc:
            await db_session.rollback()
            raise exc


AsyncSessionDependencyType = Annotated[AsyncSession, Depends(get_session)]
