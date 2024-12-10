from pydantic import BaseModel, Field
from typing import Optional

class JobBase(BaseModel):
    title: str = Field(..., description="Название вакансии")
    description: str = Field(..., description="Описание вакансии")
    requirements: Optional[str] = Field(None, description="Требования к кандидату")
    salary: Optional[float] = Field(None, description="Зарплата")
    phone: str = Field(..., description="Телефон работодателя")

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary: Optional[float] = None
    phone: Optional[str] = None

class JobInResponse(JobBase):
    id: int

    class Config:
        orm_mode = True
