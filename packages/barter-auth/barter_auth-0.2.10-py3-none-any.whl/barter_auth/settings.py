from pydantic_settings import BaseSettings


class TokenSettings(BaseSettings):
    URL: str | None = None #'redis://localhost:6378/1'
    HOST: str = '127.0.0.1'
    PORT: int = 6379
    PASSWORD: str | None = None
    DB: int = 0
    DB_ADV_BLOGERS: int = 11
    ACCESS_PREFIX: str = 'bauth_access'
    REFRESH_PREFIX: str = 'bauth_refresh'
    TOTP_PREFIX: str = 'bauth_totp'
    TOKEN_STORAGE: str = 'headers'

    PROFILE_PREFIX: str = 'pbauth_rofile'
    ADVERTISER_PREFIX: str = 'bauth_advertiser'
    INSTAGRAM_PREFIX: str = 'bauth_instagram'


    class Config:
        env_prefix = 'REDIS_AUTH_'


app_settings = TokenSettings()

__all__ = [
    'app_settings',
]
