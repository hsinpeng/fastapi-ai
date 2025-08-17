from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
from schemas import users as UserSchema
from database.fake_db import get_db

fake_db = get_db()

router = APIRouter(tags=["users"], prefix="/api")

@router.get("/users", response_model=List[UserSchema.UserRead])
#@app.get("/users")
async def get_users(qry: str = None):
    #print(fake_db['users'])
    return fake_db['users']

@router.get("/users/{user_id}" , response_model=UserSchema.UserRead)
async def get_user_by_id(user_id: int, qry: str = None):
    for user in fake_db["users"]:
        #print(f"-----{user}-----")
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/users" , response_model=UserSchema.UserCreateResponse)
#@app.post("/users" , response_model=UserSchema.UserCreate)
async def create_users(user: UserSchema.UserCreate):
    json_compatible_user_data = jsonable_encoder(user)
    fake_db["users"].append(json_compatible_user_data)
    return json_compatible_user_data #JSONResponse(content=json_compatible_user_data)

@router.delete("/users/{user_id}")
async def delete_users(user_id: int):
    for user in fake_db["users"]:
        if user["id"] == user_id:
            fake_db["users"].remove(user)
            return user
    return {"error": "User not found"}