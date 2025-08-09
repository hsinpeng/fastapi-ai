import json
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
#from fastapi.responses import JSONResponse
from typing import List
from setting.config import get_settings
from schemas import users as UserSchema
from schemas import items as ItemSchema
from database.fake_db import get_db

fake_db = get_db()

app = FastAPI()

@app.get("/")
def hello_world():
    return "Hello FastAPI!"

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

##### Users #####
@app.get("/users", response_model=List[UserSchema.UserRead])
#@app.get("/users")
def get_users(qry: str = None):
    #print(fake_db['users'])
    return fake_db['users']

@app.get("/users/{user_id}" , response_model=UserSchema.UserRead)
def get_user_by_id(user_id: int, qry: str = None):
    for user in fake_db["users"]:
        #print(f"-----{user}-----")
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/users" , response_model=UserSchema.UserCreateResponse)
#@app.post("/users" , response_model=UserSchema.UserCreate)
def create_users(user: UserSchema.UserCreate):
    json_compatible_user_data = jsonable_encoder(user)
    fake_db["users"].append(json_compatible_user_data)
    return json_compatible_user_data #JSONResponse(content=json_compatible_user_data)

@app.delete("/users/{user_id}")
def delete_users(user_id: int):
    for user in fake_db["users"]:
        if user["id"] == user_id:
            fake_db["users"].remove(user)
            return user
    return {"error": "User not found"}

##### Items #####
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