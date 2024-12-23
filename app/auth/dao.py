from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.auth.models import User, Role


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_if_user_exists_by_login_and_tg(cls, session: AsyncSession, login: str, telegram_id: int):
        """
        Найти одну запись по фильтрам
        """
        try:
            query = select(cls.model).filter(or_(cls.model.login == login, cls.model.telegram_id == telegram_id))
            result = await session.execute(query)
            record = result.scalars().all()
            return bool(record)
            # return record
        except SQLAlchemyError as e:
            raise e

class RoleDAO(BaseDAO):
    model = Role
