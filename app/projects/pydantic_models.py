import enum

from pydantic import BaseModel, Field, ConfigDict, computed_field

from app.auth.pydantic_models import UserInfo
from app.settings import get_settings

settings = get_settings()

# TODO

class TaskStatusEnum(str, enum.Enum):
    PENDING = "Отложена"
    IN_PROGRESS = "В процессе"
    COMPLETED = "Завершена"


class LabelBase(BaseModel):
    id: int
    name: str


class CommentBase(BaseModel):
    id: int
    user: UserInfo = Field(exclude=True)

    @computed_field
    def user_id(self) -> int:
        return self.user.id

    # task: Task = Field(exclude=True)
    content: str


class CommentExt(CommentBase):
    task_id: int


class TaskBase(BaseModel):
    id: int
    title: str
    description: str
    status: str
    comments: list[CommentBase] | None


class TaskExt(TaskBase):
    project_id: int


class ProjectBase(BaseModel):
    name: str
    description: str
    labels: list[LabelBase] | None
    tasks: list[TaskBase] | None


class ProjectExt(ProjectBase):
    id: int
