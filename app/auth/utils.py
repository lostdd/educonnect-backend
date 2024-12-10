from datetime import datetime, timedelta, timezone
import re

from passlib.context import CryptContext
from jose import jwt

from app.settings import get_settings

settings = get_settings()

def verify_password(plain_password, hashed_password) -> bool:
    return CryptContext(schemes=settings.PASSLIB_CRYPT_CONTEXT_SCHEMES, deprecated="auto").verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
    return CryptContext(schemes=settings.PASSLIB_CRYPT_CONTEXT_SCHEMES, deprecated="auto").hash(password)

def password_check(password, min_length: int = 8):
    # from https://stackoverflow.com/a/32542964
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8/min_length characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < min_length

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # searching for whitespaces
    whitespace_error = len(password.strip()) != len(password)

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error or whitespace_error )

    return {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }


def create_jwt_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGHORITHM)
    return encoded_jwt
