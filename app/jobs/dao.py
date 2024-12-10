from app.dao.base import BaseDAO
from app.jobs.models import Job
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class JobDAO(BaseDAO):
    model = Job

    @classmethod
    async def find_job_by_title(cls, session: AsyncSession, title: str):
        """Поиск вакансии по названию."""
        try:
            query = select(cls.model).filter(cls.model.title == title)
            result = await session.execute(query)
            job = result.scalars().first()
            return job
        except SQLAlchemyError as e:
            raise
