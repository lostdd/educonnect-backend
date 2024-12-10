from typing import Type, T
import datetime

from sqlalchemy import func, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, create_async_engine, async_sessionmaker

from app.settings import get_settings


settings = get_settings()

engine = create_async_engine(settings.DATABASE_URL, echo=True)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False
)


async def init_db_if_required():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


# async def get_async_session() -> AsyncSession:
#     async with async_sessionmaker() as session:
#         yield session


# @db_connection wrapper
# def db_connection(method):
#     async def wrapper(*args, **kwargs):
#         async with get_async_session() as session:
#             try:
#                 # Явно не открываем транзакции, так как они уже есть в контексте
#                 return await method(*args, session=session, **kwargs)
#             except Exception as e:
#                 await session.rollback()  # Откатываем сессию при ошибке
#                 raise e
#             finally:
#                 await session.close()
#     return wrapper


def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T:
    return pydantic_model(**db_object.__dict__)
