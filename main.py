from fastapi import FastAPI

from setting.config import get_settings
from schemas import users as UserSchema
from schemas import items as ItemSchema
#from database.fake_db import fake_db
from database.fake_db import get_db

fake_db = get_db()

app = FastAPI()

@app.get("/")
def hello_world():
    return "Hello World"

@app.get("/infor")
def get_infor():
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "author": settings.author,
        "app_mode": settings.app_mode,
        "port": settings.port,
        "reload": settings.reload,
        "database_url": settings.database_url
    }

@app.get("/users/{user_id}", response_model=UserSchema.UserRead)
def get_users(user_id: int, qry: str = None):
    if user_id not in fake_db["users"]:
        return {"error": "User not found"}
    #return {"user": fake_db['users'][user_id], "query": qry }
    user = fake_db["users"][user_id]
    return user

@app.post("/users", response_model=UserSchema.UserCreate)
def create_users(user: UserSchema.UserCreate):
    fake_db["users"][user.id] = user
    return user

@app.delete("/users/{user_id}")
def delete_users(user_id: int):
    user = fake_db["users"].pop(user_id)
    return user

@app.get("/items/{item_id}" , response_model=ItemSchema.ItemRead)
def get_item_by_id(item_id : int , qry : str = None ):
    if item_id not in fake_db["items"]:
        return {"error": "Item not found"}
    return fake_db['items'][item_id]

@app.post("/items" , response_model=ItemSchema.ItemCreate)
def create_items(item: ItemSchema.ItemCreate ):
    fake_db["items"][item.id] = item
    return item

@app.delete("/items/{item_id}")
def delete_items(item_id: int):
    item = fake_db["items"].pop(item_id)
    return item