from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DS_CLIENT_ID: str
    DS_USER_ID: str
    DS_AUTHORIZATION_SERVER: str
    LOG_TOKEN: str

    class Config:
        env_file = ".env"
