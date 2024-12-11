import enum

from sqlalchemy import ForeignKey, UniqueConstraint, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dao.database import Base
from app.auth.models import User

from app.projects.pydantic_models import TaskStatusEnum


class Label(Base):
    __tablename__ = "labels"
    name: Mapped[str] = mapped_column(String(64), unique=True)
    tasks: Mapped[list["Task"]] = relationship(
        secondary="tasks_labels",
        back_populates="labels"
    )


class TaskLabel(Base):
    __tablename__ = "tasks_labels"
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id', ondelete="CASCADE"))
    label_id: Mapped[int] = mapped_column(ForeignKey('labels.id', ondelete="CASCADE"))
    __table_args__ = (
        UniqueConstraint('task_id', 'label_id', name='uq_task_label_id'),
    )


class Comment(Base):
    __tablename__ = "comments"

    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id', ondelete="CASCADE"))
    task: Mapped["Task"] = relationship(
        "Task",
        back_populates="comments",
        lazy="joined"
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments",
        uselist=False,
        lazy="joined"
    )

    content: Mapped[str]


class Task(Base):
    __tablename__ = "tasks"

    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id', ondelete="CASCADE"))
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="tasks",
        lazy="joined"
    )

    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TaskStatusEnum] = mapped_column(
        default=TaskStatusEnum.PENDING.name,
        server_default=text("'PENDING'")
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="task",
        lazy="joined"
    )
    labels: Mapped[list["Label"]] = relationship(
        secondary="tasks_labels",
        back_populates="tasks",
        lazy="joined"
    )


class Project(Base):
    __tablename__ = "projects"

    name: Mapped[str]
    description: Mapped[str]

    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    owner: Mapped["User"] = relationship(
        "User",
        back_populates="projects",
        uselist=False,
        lazy="joined"
    )

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="project",
        lazy="joined"
    )
