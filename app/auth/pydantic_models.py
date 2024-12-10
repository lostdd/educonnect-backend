from pydantic import BaseModel, Field, ConfigDict, computed_field

from app.settings import get_settings

settings = get_settings()


class Login(BaseModel):
    login: str = Field(description="Логин")
    model_config = ConfigDict(from_attributes=True)

class UserBase(Login):
    name: str
    surname: str
    telegram_id: int = Field(description="ID аккаунта Telegram")

class UserExt(UserBase):
    reset_token: str = Field(description="Служебный секретный токен для активации аккаунта и сброса пароля")
    completed_registration: bool = False
    disabled: bool = False

class UserAddDB(UserExt):
    password: str = Field(min_length=settings.PASSWORD_MIN_LENGTH, description="Хеш-строка пароля")


class UserAuth(Login):
    password: str = Field(min_length=settings.PASSWORD_MIN_LENGTH,
                          max_length=settings.PASSWORD_MAX_LENGTH,
                          description="Пароль; длина задается директивами settings.PASSWORD_MIN_LENGTH и settings.PASSWORD_MAX_LENGTH")

class UserActivate(Login):
    reset_token: str = Field(description="Служебный секретный токен для активации аккаунта и сброса пароля")

class UserResetPassword(UserAuth):
    reset_token: str = Field(description="Служебный секретный токен для активации аккаунта и сброса пароля")

class UserReg(UserBase):
    password: str = Field(min_length=settings.PASSWORD_MIN_LENGTH,
                          max_length=settings.PASSWORD_MAX_LENGTH,
                          description="Пароль; длина задается директивами settings.PASSWORD_MIN_LENGTH и settings.PASSWORD_MAX_LENGTH")

class UserPut(BaseModel):
    name: str
    surname: str

class RoleModel(BaseModel):
    id: int = Field(description="Идентификатор роли")
    name: str = Field(description="Название роли")
    model_config = ConfigDict(from_attributes=True)

class UserInfo(UserExt):
    id: int = Field(description="Идентификатор пользователя")
    role: RoleModel = Field(exclude=True)

    @computed_field
    def role_name(self) -> str:
        return self.role.name

    @computed_field
    def role_id(self) -> int:
        return self.role.id

class TokenBase(BaseModel):
    id: int
    user_id: int
    type: str
    access_token: str

class TokenData(BaseModel):
    user_id: int | None = None