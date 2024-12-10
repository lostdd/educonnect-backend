from sqlalchemy import Column, String, Text, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.dao.database import Base
from app.auth.models import User


class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
    salary: Mapped[float | None] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=False)

    employer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    employer: Mapped["User"] = relationship("User", back_populates="jobs")
