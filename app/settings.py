from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    
    
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # app_name: str = "Awesome API"
    # APP_ENV: str = "DEVELOPMENT"

    BASE_URL: str = "http://localhost:8000"

    DOMAIN: str = None
    ROOT_URL: str = None

    DATABASE_URL: str = None

    TELEGRAM_BOT_TOKEN: str = "7804659295:AAGQuUuzqeeWroX_1S4OqBqSY7xED0duGzU"

    PASSWORD_CHECK: bool = True
    PASSWORD_MIN_LENGTH: int = 16
    PASSWORD_MAX_LENGTH: int = 64
    PASSLIB_CRYPT_CONTEXT_SCHEMES: list[str] = ["bcrypt"]

    # openssl rand -hex 32 or python secrets.token_hex(32)
    JWT_SECRET_KEY: str = None
    JWT_ALGHORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), env_ignore_empty=True)
    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), env_ignore_empty=True)

@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()