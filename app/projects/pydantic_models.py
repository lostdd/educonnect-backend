from pydantic import BaseModel, Field, ConfigDict, computed_field

from app.auth.pydantic_models import UserInfo
from app.settings import get_settings

settings = get_settings()

# TODO

class Comment(BaseModel):
    user: UserInfo

class Task(BaseModel):
    title: str
    description: str
    status

class Label(BaseModel):
    name: str


class ProjectBase(BaseModel):
    name: str
    description: str
    labels: list[Label]
    tasks: list[Task]
