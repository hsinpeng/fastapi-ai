from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.infor import router as infor_router
from api.users import router as users_router
from api.items import router as items_router
from database.generic import init_db

#@app.on_event("startup")
def startup():
    init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # replacement of @app.on_event("startup")
    startup()
    yield
    # replacement of @app.on_event("shutdown")
    
app = FastAPI(lifespan=lifespan)

app.include_router(infor_router)
app.include_router(users_router)
app.include_router(items_router)

