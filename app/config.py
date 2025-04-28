from typing import Literal, Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")
    
    class Config:
        # TODO: alembic doesn't like this path, use "./envs/.env"
        env_file = "./envs/.env"


settings = Settings()
