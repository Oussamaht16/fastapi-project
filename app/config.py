# hadih lmaktaba ta3 pydantic_settings rah tnadam l enviremenet variables
from pydantic_settings import BaseSettings
from typing import Optional


""" class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_hostname: str
    database_port: int
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int """


class Settings(BaseSettings):
    database_username: Optional[str] = None
    database_password: Optional[str] = None
    database_hostname: Optional[str] = None
    database_port: Optional[int] = None
    database_name: Optional[str] = None
    secret_key: Optional[str] = None
    algorithm: Optional[str] = None
    access_token_expire_minutes: Optional[int] = None

    # hna hado dok gae rahom .env doka lazam neaytolhom
    class Config:
        env_file = ".env"


settings = Settings()


print(
    "DATABASE = ",
    settings.database_password,
    settings.database_username,
    settings.database_hostname,
    settings.database_port,
    settings.database_name,
)
