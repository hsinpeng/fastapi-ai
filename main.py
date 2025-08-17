from fastapi import FastAPI
from api.infor import router as infor_router
from api.users import router as users_router
from api.items import router as items_router

app = FastAPI()

app.include_router(infor_router)
app.include_router(users_router)
app.include_router(items_router)
