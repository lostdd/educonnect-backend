from typing import Annotated
from secrets import token_urlsafe

from fastapi import APIRouter, HTTPException, Depends, status, Response, Body

from pydantic import create_model

from app import api_exceptions
from app.dao.session import TransactionSessionDep
from app.auth.dao import UserDAO
from app.auth.pydantic_models import Login, UserBase, UserAddDB, UserReg, UserAuth, UserActivate, UserResetPassword, UserPut
from app.auth.depends import get_current_user, get_current_active_user
import app.auth.utils
from app.settings import get_settings, AppSettings


# DbSessionDep: AsyncSession = Annotated[AsyncSession, Depends(get_async_session)]
AppSettingsDep: AppSettings = Annotated[AppSettings, Depends(get_settings)]


router = APIRouter(prefix='/auth')


@router.post('/register',
             response_model=UserBase)
async def register_user(db_session: TransactionSessionDep,
                        app_settings: AppSettingsDep,
                        reg_form: UserReg
    ) -> UserBase:
    user = await UserDAO.find_if_user_exists_by_login_and_tg(db_session, login=reg_form.login, telegram_id=reg_form.telegram_id)
    if user:
        raise api_exceptions.UserAlreadyExistsException
    if app_settings.PASSWORD_CHECK:
        if app.auth.utils.password_check(reg_form.password, app_settings.PASSWORD_MIN_LENGTH)['password_ok']:
            # Password is not OK - minimum {app_settings.password_min_length} characters required
            # raise HTTPException(status.HTTP_400_BAD_REQUEST,
            #                     detail=f'Password is not OK - minimum {app_settings.PASSWORD_MIN_LENGTH} characters without whitespaces required '
            #                            f'(including at least one uppercase, lowercase, special symbol and digit)'
            # )
            raise api_exceptions.PasswordIsNotOK
    user = UserAddDB(
        login=reg_form.login,
        name=reg_form.name,
        surname=reg_form.surname,
        telegram_id=reg_form.telegram_id,
        password=app.auth.utils.get_password_hash(reg_form.password),
        reset_token=token_urlsafe(128))
    await UserDAO.add(db_session, user)
    return user

@router.post('/me/activate')
async def activate_user(db_session: TransactionSessionDep,
                        activation_form: UserActivate) -> dict:
    user = await UserDAO.find_one_or_none(db_session, Login(login=activation_form.login))
    if user:
        if user.reset_token == activation_form.reset_token:
            match user.completed_registration, user.disabled:
                case False, False:
                    ValuesModel = create_model('ValuesModel', completed_registration=(bool, ...))
                    await UserDAO.update_one_by_id(
                        db_session,
                        user.id,
                        ValuesModel(completed_registration=True)
                    )
                    return {"detail": "Аккаунт успешно активирован!"}
                case True, False:
                    raise api_exceptions.AccountAlreadyActivatedException
                case _, True:
                    raise api_exceptions.AccountDisabledException
                case _, _:
                    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Защита от потенциального брутфорса - если токен неверный, то перегенерируем
        ValuesModel = create_model('ValuesModel', reset_token = (str, ...))
        await UserDAO.update_one_by_id(
            db_session,
            user.id,
            ValuesModel(reset_token=token_urlsafe(128))
        )
        await db_session.commit()
    raise api_exceptions.AccountWrongResetException

@router.delete('/me')
async def deactivate_user(db_session: TransactionSessionDep,
                          activation_form: UserActivate) -> dict:
    user = await UserDAO.find_one_or_none(db_session, Login(login=activation_form.login))
    if user:
        if user.reset_token == activation_form.reset_token:
            match user.completed_registration, user.disabled:
                case True, False:
                    ValuesModel = create_model('ValuesModel', disabled=(bool, ...))
                    await UserDAO.update_one_by_id(db_session, user.id, ValuesModel(disabled=True))
                    return {"detail": "Аккаунт успешно деактивирован!"}
                case _, True:
                    raise api_exceptions.AccountDisabledException
                case _, _:
                    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Защита от потенциального брутфорса - если токен неверный, то перегенерируем
        ValuesModel = create_model('ValuesModel', reset_token = (str, ...))
        await UserDAO.update_one_by_id(
            db_session, user.id, ValuesModel(reset_token=token_urlsafe(128))
        )
        await db_session.commit()
    raise api_exceptions.AccountWrongResetException

@router.put('/me')
async def edit_user(put_data: UserPut,
                    db_session: TransactionSessionDep,
                    user: UserBase = Depends(get_current_active_user)) -> UserBase:
    await UserDAO.update_one_by_id(db_session, user.id, put_data)
    await db_session.commit()
    return UserBase.model_validate(await UserDAO.find_one_or_none_by_id(db_session, user.id))

@router.put('/me/telegram_id')
async def update_telegram(db_session: TransactionSessionDep,
                          telegram_id: int = Body(..., embed=True),
                          user: UserBase = Depends(get_current_active_user)) -> UserBase:
    ValuesModel = create_model(
        'ValuesModel',
        telegram_id = (int, ...),
        completed_registration = (bool, ...)
    )
    await UserDAO.update_one_by_id(
        db_session,
        user.id,
        ValuesModel(telegram_id=telegram_id, completed_registration=False)
    )
    await db_session.commit()
    return UserBase.model_validate(await UserDAO.find_one_or_none_by_id(db_session, user.id))

@router.post('/me/reset_password')
async def reset_password(db_session: TransactionSessionDep,
                         app_settings: AppSettingsDep,
                         reset_form: UserResetPassword) -> dict:
    user = await UserDAO.find_one_or_none(db_session, Login(login=reset_form.login))
    if user:
        if user.reset_token == reset_form.reset_token:
            match user.completed_registration, user.disabled:
                case True, False:
                    ValuesModel = create_model('ValuesModel', password=(str, ...))
                    if app_settings.PASSWORD_CHECK:
                        if not app.auth.utils.password_check(reset_form.password, app_settings.PASSWORD_MIN_LENGTH)['password_ok']:
                            raise api_exceptions.PasswordIsNotOK
                    await UserDAO.update_one_by_id(
                        db_session,
                        user.id,
                        ValuesModel(password=app.auth.utils.get_password_hash(reset_form.password))
                    )
                    return {"detail": "Пароль успешно изменен!"}
                case _, True:
                    raise api_exceptions.AccountDisabledException
                case _, _:
                    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Защита от потенциального брутфорса - если токен неверный, то перегенерируем
        ValuesModel = create_model('ValuesModel', reset_token = (str, ...))
        await UserDAO.update_one_by_id(
            db_session, user.id, ValuesModel(reset_token=token_urlsafe(128))
        )
        await db_session.commit()
    raise api_exceptions.AccountWrongResetException

@router.post('/login')
async def login(response: Response, auth_form: UserAuth, db_session: TransactionSessionDep):
    user = await UserDAO.find_one_or_none(db_session, Login(login=auth_form.login))
    if user and (not user.completed_registration or user.disabled):
        raise api_exceptions.AccountDisabledException
    elif user and app.auth.utils.verify_password(auth_form.password, user.password):
        access_token = app.auth.utils.create_jwt_access_token({"sub": str(user.id)})
        response.set_cookie(key="api_access_token", value=access_token, httponly=True)
        return {"message": "Авторизация успешна!", "ok": True, "access_token": access_token}
    raise api_exceptions.IncorrectLoginOrPasswordException

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="api_access_token")
    return {"message": "Выход!", "ok": True}

@router.get('/me', response_model=UserBase)
async def me(user_data: UserBase = Depends(get_current_user)):
    return user_data
