from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional, List
import os

from dataclasses import dataclass





class Configs(BaseSettings):
    # ------------ БД ------------
    DB_HOST: Optional[str] = Field(default="localhost", env="DB_HOST")
    DB_PORT: Optional[int] = Field(default=5432, env="DB_PORT")
    DB_USER: Optional[str] = Field(default="postgres", env="DB_USER")
    DB_NAME: Optional[str] = Field(default="postgres", env="DB_NAME")
    DB_PASS: Optional[str] = Field(default="admin", env="DB_PASS")

    BOT_TOKEN: Optional[str] = Field(default="7235849573:AAHBKmG4FYL-DFv7etvsRJYrXrVf2JxuW7A", env="BOT_TOKEN")
    ADMINS: Optional[List[str]] = Field(default=["1007781768"], env="ADMINS")



configs = Configs()



@dataclass
class CronScheduleSettings:
    day_of_week: int = 1   # Среда (отсчёт дней недели с нуля)
    hour: int = 19         #  ->
                                # 19:00
    minute: int = 0        #  ->



def get_db_url():
    return (
        f"postgresql://{configs.DB_USER}:{configs.DB_PASS}@{configs.DB_HOST}:{configs.DB_PORT}/{configs.DB_NAME}"
    )

