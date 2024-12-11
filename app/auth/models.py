import secrets

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dao.database import Base


# 1 - посетитель/ученик
# 2 - зарезерв
# 3 - работодатель
# 4 - учитель
# 5 - администратор
# 6 - суперадминистратор
class Role(Base):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship(back_populates="role")


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    telegram_id: Mapped[int]
    password: Mapped[str]
    reset_token: Mapped[str] = mapped_column(
        default=secrets.token_urlsafe(128), onupdate=secrets.token_urlsafe(128)
    )
    completed_registration: Mapped[bool] = mapped_column(default=False)
    disabled: Mapped[bool] = mapped_column(default=False)

    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id'), default=1, server_default=text("1")
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users", lazy="joined")

    projects: Mapped[list["Project"]] = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete-orphan")

    # access_tokens: Mapped[list["AccessToken"]] = relationship(
    #     "AccessToken",
    #     back_populates="user",
    #     cascade="all, delete-orphan"
    # )
