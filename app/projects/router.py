from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status, Response

from pydantic import create_model

from app import api_exceptions
from app.dao.session import SessionDep, TransactionSessionDep
from app.projects.dao import ProjectDAO, TaskDAO, LabelDAO, CommentDAO
from app.auth.depends import get_current_active_user

from app.settings import get_settings, AppSettings

# TODO!

# DbSessionDep: AsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
AppSettingsDep: AppSettings = Annotated[AppSettings, Depends(get_settings)]


router = APIRouter(prefix='/projects')

# PROJECTS

@router.get('/',
             response_model=None)
async def get_projects(db_session: SessionDep, user: get_current_active_user):
    ProjectDAO
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.post('/',
             response_model=None)
async def create_new_project(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)


@router.get('/{project_id:int}',
             response_model=None)
async def get_project(db_session: SessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.put('/{project_id:int}',
             response_model=None)
async def update_project(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.delete('/{project_id:int}',
             response_model=None)
async def delete_project(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

# TASKS

@router.get('/{project_id:int}/tasks',
             response_model=None)
async def get_project_tasks(db_session: SessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.post('/{project_id:int}/tasks',
             response_model=None)
async def create_new_task(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.get('/tasks/{task_id:int}',
             response_model=None)
async def get_task(db_session: SessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.put('/tasks/{task_id:int}',
             response_model=None)
async def update_task(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.delete('/tasks/{task_id:int}',
             response_model=None)
async def delete_task(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.put('/tasks/{task_id:int}/assign',
             response_model=None)
async def assign_user_to_task(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.delete('/tasks/{task_id:int}/unassign',
             response_model=None)
async def unassign_user_from_task(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

# COMMENTS

@router.get('/tasks/{task_id:int}/comments',
             response_model=None)
async def get_task_comments(db_session: SessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.post('/tasks/{task_id:int}/comments',
              response_model=None)
async def create_new_comment(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.put('/comments/{comment_id:int}',
             response_model=None)
async def update_comment(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.delete('/comments/{comment_id:int}',
             response_model=None)
async def delete_comment(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

# LABELS

@router.get('/labels',
             response_model=None)
async def get_labels(db_session: SessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.post('/labels',
              response_model=None)
async def create_new_label(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.put('/labels/{label_id:int}',
             response_model=None)
async def get_label(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.put('/labels/{label_id:int}',
             response_model=None)
async def update_label(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)

@router.delete('/labels/{label_id:int}',
             response_model=None)
async def delete_label(db_session: TransactionSessionDep, user: get_current_active_user):
    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED)
