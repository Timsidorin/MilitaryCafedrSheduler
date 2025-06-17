from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os


class Configs(BaseSettings):
    # ------------ БД ------------
    DB_HOST: Optional[str] = Field(default="localhost", env="DB_HOST")
    DB_PORT: Optional[int] = Field(default=5432, env="DB_PORT")
    DB_USER: Optional[str] = Field(default="postgres", env="DB_USER")
    DB_NAME: Optional[str] = Field(default="postgres", env="DB_NAME")
    DB_PASS: Optional[str] = Field(default="admin", env="DB_PASS")

configs = Configs()

def get_db_url():
    return (
        f"postgresql://{configs.DB_USER}:{configs.DB_PASS}@{configs.DB_HOST}:{configs.DB_PORT}/{configs.DB_NAME}"
    )

