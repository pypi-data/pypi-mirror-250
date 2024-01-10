from pydantic_settings import BaseSettings


class TokenSettings(BaseSettings):
    URL: str | None = None #'redis://localhost:6378/1'
    HOST: str = '127.0.0.1'
    PORT: int = 6379
    PASSWORD: str | None = None
    DB: int = 0
    DB_ADV_BLOGERS: int = 11
    ACCESS_PREFIX: str = 'access'
    REFRESH_PREFIX: str = 'refresh'
    TOTP_PREFIX: str = 'totp'
    TOKEN_STORAGE: str = 'headers'

    PROFILE_PREFIX: str = 'profile'
    ADVERTISER_PREFIX: str = 'advertiser'
    INSTAGRAM_PREFIX: str = 'instagram'

    class Config:
        env_prefix = 'REDIS_AUTH_'


app_settings = TokenSettings()

__all__ = [
    'app_settings',
]
