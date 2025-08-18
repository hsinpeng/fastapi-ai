from fastapi import APIRouter
from setting.config import get_settings
from sqlalchemy import text
from database.generic import get_db # 新增 get_db

router = APIRouter(tags=["infor"], prefix="/api")

@router.get("/")
async def hello_world():
    return "Hello FastAPI!"


@router.get("/infor")
def get_infor():
    settings = get_settings()
    databases = None
    db_session = get_db()
    
    try :
        databases = db_session.execute(text("SELECT datname FROM pg_database;")).fetchall()
    except Exception as e:
        print(e)

    if databases is None:
        try :
            databases = db_session.execute(text("SHOW DATABASES;")).fetchall()
        except Exception as e:
            print(e)

    return {
        # ....
        "db_type": settings.db_type,
        "database_url": settings.database_url,
        "database": str(databases)
    }

# @router.get("/infor")
# async def get_infor():
#     settings = get_settings()
#     return {
#         "app_name": settings.app_name,
#         "author": settings.author,
#         "app_mode": settings.app_mode,
#         "port": settings.port,
#         "reload": settings.reload,
#         "database_url": settings.database_url
#     }