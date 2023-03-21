import os
from typing import Union

from pydantic import BaseSettings


class Settings(BaseSettings):
    SENDER_EMAIL :      str 
    SENDER_PASSWORD:    str
    RECIPIENT_EMAIL:    str
    POSTGRES_USER:      str
    POSTGRES_PASSWORD:  str
    POSTGRES_HOST:      str
    POSTGRES_DB:        str
    SECRET_KEY:         str
    ALGORITHM :         str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    
    class Config:   
        env_file = 'environments\development.env' 

settings = Settings()