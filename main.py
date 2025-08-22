from contextlib import asynccontextmanager
from fastapi import FastAPI
from setting.config import get_settings

settings = get_settings()

if settings.run_mode == "ASYNC":
    from database.generic import init_db, close_db
elif settings.run_mode == "SYNC":
    from sync.database.generic import init_db, close_db
else:
    print(f"Error: Wrong run_mode:{settings.run_mode}!")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # replacement of @app.on_event("startup")
    init_db()
    yield
    # replacement of @app.on_event("shutdown")
    close_db()

app = FastAPI(lifespan=lifespan)

if settings.run_mode == "ASYNC":
    from api.infor import router as infor_router
    from api.users import router as user_router
    from api.items import router as item_router
elif settings.run_mode == "SYNC":
    from sync.api.infor import router as infor_router
    from sync.api.users import router as users_router
    from sync.api.items import router as items_router
else:
    print(f"Error: Wrong run_mode:{settings.run_mode}!")

app.include_router(infor_router)
app.include_router(users_router)
app.include_router(items_router)
