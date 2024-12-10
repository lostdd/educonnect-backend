from typing import List, Generic, TypeVar

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from pydantic import BaseModel

from app.dao.database import Base

# Объявляем типовой параметр T с ограничением, что это наследник pydantic.Base
T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]  # Устанавливается в дочернем классе

    # ADD

    @classmethod
    async def add(cls, session: AsyncSession, instance: BaseModel):
        """
        Добавление одной записи
        """
        new_instance = cls.model(**instance.model_dump(exclude_unset=True))
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[BaseModel]):
        """
        Добавление множества записей
        """
        new_instances = [cls.model(**instance.model_dump(exclude_unset=True)) for instance in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    # FIND

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        # Найти запись по ID
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise
    
    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        """
        Найти одну запись по фильтрам
        """
        filter_dict = filters.model_dump(exclude_unset=True)
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None):
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise

    # UPDATE

    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, data_id: int, values: BaseModel):
        values_dict = values.model_dump(exclude_unset=True)
        try:
            record = await session.get(cls.model, data_id)
            for key, value in values_dict.items():
                setattr(record, key, value)
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise
    
    @classmethod
    async def update_many(cls, session: AsyncSession, filter_criteria: BaseModel, values: BaseModel):
        filter_dict = filter_criteria.model_dump(exclude_unset=True)
        values_dict = values.model_dump(exclude_unset=True)
        try:
            stmt = (
                update(cls.model)
                .filter_by(**filter_dict)
                .values(**values_dict)
            )
            result = await session.execute(stmt)
            await session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            raise

    # DELETE

    @classmethod
    async def delete_one_by_id(cls, data_id: int, session: AsyncSession):
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise

    @classmethod
    async def delete_many(cls, session: AsyncSession, filters: BaseModel | None):
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
            stmt = delete(cls.model).filter_by(**filter_dict)
        else:
            stmt = delete(cls.model)
        try:
            result = await session.execute(stmt)
            await session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            raise
