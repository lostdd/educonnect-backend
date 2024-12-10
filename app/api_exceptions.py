from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                           detail='Пользователь уже существует')

PasswordIsNotOK = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Пароль не соответствует требованиям')

IncorrectLoginOrPasswordException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                                  detail='Неверный логин или пароль')

TokenExpiredException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен просрочен', headers={"WWW-Authenticate": "Bearer"})

TokenNotFound = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Токен просрочен', headers={"WWW-Authenticate": "Bearer"})

NoJwtException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                           detail="Токен невалиден!",
                           headers={"WWW-Authenticate": "Bearer"},
)

NoUserIdException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не найден ID пользователя')

ForbiddenException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав!')

AccountAlreadyActivatedException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Аккаунт уже активирован')

AccountNotActivatedException = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Аккаунт не активирован или отключен')

AccountDisabledException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Аккаунт не активирован или отключен')

AccountWrongResetException = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Неверная пара логин/код')
