from datetime import datetime, timezone
from typing import Annotated

from jose import jwt, JWTError
from pydantic import create_model, BaseModel
from fastapi import Depends, Request, Cookie
from fastapi.security import OAuth2PasswordBearer

from app.dao.session import SessionDep
from app.auth.dao import UserDAO
from app.auth.pydantic_models import UserInfo

from app import api_exceptions



from app.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


class AccessTokenCookie(BaseModel):
    api_access_token: str | None


def get_token(cookies: Annotated[AccessTokenCookie, Cookie()]):
    token = cookies.api_access_token
    print(token)
    if not token:
        raise api_exceptions.TokenNotFound
    return token


async def get_current_user(
        token: Annotated[str, Depends(get_token)],
        session: SessionDep
    ) -> UserInfo:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGHORITHM])
        expire: str = payload.get('exp')
        expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
        if (not expire) or (expire_time < datetime.now(timezone.utc)):
            raise api_exceptions.TokenExpiredException
        user_id: str = payload.get("sub")
        if user_id is None:
            raise api_exceptions.NoUserIdException
        # token_data = TokenData(user_id=user_id)
    except JWTError:
        raise api_exceptions.NoJwtException
    FilterModel = create_model('FilterModel', id=(int, ...))
    user = await UserDAO.find_one_or_none(session, FilterModel(id=user_id))
    if not user:
        raise api_exceptions.NoUserIdException
    return UserInfo.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[UserInfo, Depends(get_current_user)],
) -> UserInfo:
    if current_user.disabled:
        raise api_exceptions.AccountDisabledException
    if not current_user.completed_registration:
        raise api_exceptions.AccountNotActivatedException
    return current_user


async def get_current_user_with_role(current_user: UserInfo, role_ids: list[int]):
    if current_user.role.id in role_ids:
        return current_user
    raise api_exceptions.ForbiddenException


async def get_current_teacher_user(current_user: UserInfo = Depends(get_current_user)):
    return get_current_user_with_role(current_user, [4])


async def get_current_admin_user(current_user: UserInfo = Depends(get_current_user)):
    return get_current_user_with_role(current_user, [5, 6])
