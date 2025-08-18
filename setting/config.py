import os
from functools import lru_cache
from .util import parse_boolean
#from dotenv import load_dotenv

@lru_cache()
def get_settings():
    #load_dotenv(f".env.{os.getenv('APP_MODE')}") # 多此一舉？
    return Settings()

class Settings():
    app_name:str = "FastAPI for AI Tutorial"
    author:str = "Sheldon Lin"

    app_mode: str = os.getenv("APP_MODE")
    port:int = int(os.getenv("PORT"))
    #reload:bool = bool(os.getenv("RELOAD"))
    reload:bool = parse_boolean(os.getenv("RELOAD"))
    # 多新增 db_type
    #database_url:str = os.getenv("DATABASE_URL")
    db_type:str = os.getenv("DB_TYPE").upper()
    database_url: str = os.getenv(f"{db_type}_DATABASE_URL")