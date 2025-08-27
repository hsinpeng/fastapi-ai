import os
from functools import lru_cache
from .util import parse_boolean
#from dotenv import load_dotenv

@lru_cache()
def get_settings():
    #load_dotenv(f".env.{os.getenv('APP_MODE')}") # 多此一舉？
    return Settings()

class Settings():
    app_name:str = "FastAPI for AI Services"
    author:str = "Sheldon Lin"

    app_mode: str = os.getenv("APP_MODE")
    run_mode: str = os.getenv("RUN_MODE")
    port:int = int(os.getenv("PORT"))
    #reload:bool = bool(os.getenv("RELOAD"))
    reload:bool = parse_boolean(os.getenv("RELOAD"))
    # 新增 db_type
    #database_url:str = os.getenv("DATABASE_URL")
    db_type:str = os.getenv("DB_TYPE").upper()
    #database_url: str = os.getenv(f"{db_type}_DATABASE_URL")
    database_url: str = os.getenv(f"{run_mode}_{db_type}_DATABASE_URL") 

    # 新增 JWT
    access_token_secret:str = os.getenv("ACCESS_TOKEN_SECRET")
    access_token_expire_minutes:int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    refresh_token_secret:str = os.getenv("REFRESH_TOKEN_SECRET")
    refresh_token_expire_minutes:int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))