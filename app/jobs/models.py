from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey
from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey
from app.dao.database import Base

class Job(Base):
    __tablename__ = "jobs"
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False)
    description: str = Column(Text, nullable=False)
    requirements: str | None = Column(Text, nullable=True)
    salary: float | None = Column(Float, nullable=True)
    phone: str = Column(String, nullable=False)

    employer_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)  # Только внешние ключ
