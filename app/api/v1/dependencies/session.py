from asyncio import Lock
from http import HTTPStatus
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import session


async def get_session() -> AsyncGenerator[tuple[AsyncSession, Lock], None]:
    if session.session_factory_cache is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="impossible to create session")

    async with session.session_factory_cache() as db_session:
        try:
            yield db_session, Lock()
        except Exception as exc:
            await db_session.rollback()
            raise exc


AsyncSessionDependencyType = Annotated[tuple[AsyncSession, Lock], Depends(get_session)]
