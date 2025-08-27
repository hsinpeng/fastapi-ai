from contextlib import asynccontextmanager
from fastapi import FastAPI
from setting.config import get_settings

settings = get_settings()

if settings.run_mode == "ASYNC":
    from database.generic import init_db, close_db
    from api.infor import router as infor_router
    from api.users import router as users_router
    from api.items import router as items_router
    from api.auth import router as auth_router
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # replacement of @app.on_event("startup")
        print("ASYNC startup: Initializing resources...")
        await init_db()
        yield
        # replacement of @app.on_event("shutdown")
        print("ASYNC shutdown: Releasing resources...")
        await close_db()
    app = FastAPI(lifespan=lifespan)
    app.include_router(infor_router)
    app.include_router(users_router)
    app.include_router(items_router)
    app.include_router(auth_router)

elif settings.run_mode == "SYNC":
    from sync.database.generic import init_db, close_db
    from sync.api.infor import router as infor_router
    from sync.api.users import router as users_router
    from sync.api.items import router as items_router
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # replacement of @app.on_event("startup")
        print("SYNC cation startup: Initializing resources...")
        init_db()
        yield
        # replacement of @app.on_event("shutdown")
        print("SYNC shutdown: Releasing resources...")
        close_db()
    app = FastAPI(lifespan=lifespan)
    app.include_router(infor_router)
    app.include_router(users_router)
    app.include_router(items_router)

else:
    print(f"Error: Wrong run_mode:{settings.run_mode}!")