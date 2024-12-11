from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.projects.models import Project, Task, Comment, Label
# TODO!


class ProjectDAO(BaseDAO):
    model = Project
    @classmethod
    async def get_full_blog_info(cls, session: AsyncSession, project_id: int):
        query = (
            select(cls.model)
            .options(
                joinedload(Project.owner),
                selectinload(Project.tasks)
            )
            .filter_by(id=project_id)
        )

        result = await session.execute(query)
        project = result.scalar_one_or_none()

        if not project:
            return {
                'message': f"",
                'status': 'error'
            }

        return project


class TaskDAO(BaseDAO):
    model = Task


class CommentDAO(BaseDAO):
    model = Comment


class LabelDAO(BaseDAO):
    model = Label

    @classmethod
    async def add_labels(cls, session: AsyncSession, label_names: list[str]) -> list[int]:
        label_ids = []
        for label_name in label_names:
            label_name = label_name.lower()
            stmt = select(cls.model).filter_by(name=label_name)
            result = await session.execute(stmt)
            label = result.scalars().first()

            if label:
                label_ids.append(label.id)
            else:
                new_label = cls.model(name=label_name)
                session.add(new_label)
                try:
                    await session.flush()
                    label_ids.append(new_label.id)
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

        return label_ids
