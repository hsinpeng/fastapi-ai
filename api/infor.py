from fastapi import APIRouter
from setting.config import get_settings

router = APIRouter(tags=["infor"], prefix="/api")

@router.get("/")
async def hello_world():
    return "Hello FastAPI!"

@router.get("/infor")
async def get_infor():
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "author": settings.author,
        "app_mode": settings.app_mode,
        "port": settings.port,
        "reload": settings.reload,
        "database_url": settings.database_url
    }