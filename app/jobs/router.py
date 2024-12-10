from fastapi import APIRouter, HTTPException, Depends, status
from app.dao.session import TransactionSessionDep
from app.jobs.dao import JobDAO
from app.jobs.pydantic_models import JobCreate, JobUpdate, JobInResponse
from app.auth.depends import get_current_user
import app.api_exceptions

router = APIRouter(prefix='/jobs')

@router.post("/jobs_create", response_model=JobInResponse)
async def create_job(
    db_session: TransactionSessionDep,
    job_create: JobCreate,
    current_user: int = Depends(get_current_user)
):
    """Создание вакансии."""
    job = JobCreate(**job_create.dict())
    job.employer_id = current_user.id
    await JobDAO.add(db_session, job)
    return job

@router.get("/{job_id}", response_model=JobInResponse)
async def get_job(job_id: int, db_session: TransactionSessionDep):
    """Получить вакансию по ID."""
    job = await JobDAO.find_by_id(db_session, job_id)
    if not job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=JobInResponse)
async def update_job(
    job_id: int, 
    db_session: TransactionSessionDep, 
    job_update: JobUpdate
):
    """Обновление вакансии."""
    job = await JobDAO.find_by_id(db_session, job_id)
    if not job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    # Обновляем поля вакансии
    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(job, key, value)
    
    await JobDAO.update(db_session, job)
    return job

@router.delete("/{job_id}")
async def delete_job(job_id: int, db_session: TransactionSessionDep):
    """Удалить вакансию."""
    job = await JobDAO.find_by_id(db_session, job_id)
    if not job:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    await JobDAO.delete(db_session, job)
    return {"message": "Job deleted successfully"}
