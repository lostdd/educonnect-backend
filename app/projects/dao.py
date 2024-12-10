from app.dao.base import BaseDAO
from app.projects.models import Project, Task, Comment, Label
# TODO!


class ProjectDAO(BaseDAO):
    model = Project


class TaskDAO(BaseDAO):
    model = Task


class CommentDAO(BaseDAO):
    model = Comment


class LabelDAO(BaseDAO):
    model = Label
