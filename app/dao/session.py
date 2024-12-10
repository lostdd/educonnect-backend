from fastapi import Depends

from contextlib import asynccontextmanager
from typing import Callable, Optional, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from functools import wraps

from typing import Optional, Annotated
from app.dao.database import async_session_maker # get_async_session


class DatabaseSessionManager:

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_maker = session_maker

    @asynccontextmanager
    async def create_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            try:
                yield session
            except Exception as e:
                raise
            finally:
                await session.close()

    @asynccontextmanager
    async def transaction(self, session: AsyncSession) -> AsyncGenerator[None, None]:
        try:
            yield
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.create_session() as session:
            yield session

    async def get_transaction_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.create_session() as session:
            async with self.transaction(session):
                yield session

    @property
    def session_dependency(self) -> Callable:
        return Depends(self.get_session)

    @property
    def transaction_session_dependency(self) -> Callable:
        return Depends(self.get_transaction_session)


session_manager = DatabaseSessionManager(async_session_maker)


SessionDep: AsyncSession = Annotated[AsyncSession, session_manager.session_dependency]
TransactionSessionDep: AsyncSession = Annotated[AsyncSession, session_manager.transaction_session_dependency]
