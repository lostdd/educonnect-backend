from datetime import datetime, timezone
from typing import Annotated

from jose import jwt, JWTError
from pydantic import create_model
from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer

from app.dao.session import SessionDep
from app.auth.dao import UserDAO
from app.auth.pydantic_models import UserExt

from app import api_exceptions



from app.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_token(request: Request):
    token = request.cookies.get('api_access_token')
    if not token:
        raise api_exceptions.TokenNotFound
    return token

async def get_current_user(
        token: Annotated[str, Depends(get_token)],
        session: SessionDep
    ) -> UserExt:
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
    return UserExt.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[UserExt, Depends(get_current_user)],
) -> UserExt:
    if current_user.disabled:
        raise api_exceptions.AccountDisabledException
    elif not current_user.completed_registration:
        raise api_exceptions.AccountNotActivatedException
    return current_user

