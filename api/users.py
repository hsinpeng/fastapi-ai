from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from schemas import users as UserSchema
#from database.fake_db import get_db
#fake_db = get_db()
from models.user import User as UserModel 
from database.generic import get_db
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session
#from setting.config import get_settings

router = APIRouter(tags=["users"], prefix="/api")

@router.get("/users/{user_id}" , response_model=UserSchema.UserRead )
def get_user_by_id(user_id: int, qry: str = None):
    db_session:Session = get_db()

    stmt = select(UserModel.name,UserModel.id,UserModel.email,UserModel.avatar).where(UserModel.id == user_id)
    user = db_session.execute(stmt).first()
    if user:
        return user
        
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/users", 
        response_model=List[UserSchema.UserRead],
        response_description="Get list of user",  
)
def get_users(qry: str = None):
    db_session:Session = get_db()

    stmt = select(UserModel.name,UserModel.id,UserModel.email,UserModel.avatar)
    users = db_session.execute(stmt).all()
    return users



@router.post("/users" ,
        response_model=UserSchema.UserCreateResponse,
        status_code=status.HTTP_201_CREATED,
        response_description="Create new user"
)
async def create_user(newUser: UserSchema.UserCreate ):
    db_session:Session = get_db()

    # check if user already exists
    # stmt = select(UserModel).where(UserModel.email == newUser.email)
    stmt = select(UserModel.id).where(UserModel.email == newUser.email)
    user = db_session.execute(stmt).first()
    if user:
        raise HTTPException(status_code=409, detail="User already exists")
    
    # create user
    user = UserModel(
        name=newUser.name,
        password=newUser.password,
        age=newUser.age,
        birthday=newUser.birthday,
        email=newUser.email,
        avatar=newUser.avatar
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return vars(user)


@router.put("/users/{user_id}" , response_model=UserSchema.UserUpdateResponse )
def update_users(user_id: int, newUser: UserSchema.UserUpdate ):
    db_session:Session = get_db()

    stmt = select(UserModel.id).where(UserModel.id == user_id)
    user = db_session.execute(stmt).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # ...
    stmt = update(UserModel).where(UserModel.id == user_id).values(
        name=newUser.name,
        password=newUser.password,
        age=newUser.age,
        birthday=newUser.birthday,
        avatar=newUser.avatar
    )

    db_session.execute(stmt)

    return newUser


@router.put("/users/{user_id}/password", status_code=200)
def update_user_password(user_id : int, newUser:UserSchema.UserUpdatePassword):
    db_session:Session = get_db()

    stmt = select(UserModel.id).where(UserModel.id == user_id)
    user = db_session.execute(stmt).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # ...
    stmt = update(UserModel).where(UserModel.id == user_id).values(
        password=newUser.password,
    )
    db_session.execute(stmt)
    db_session.commit()

    return newUser


@router.delete("/users/{user_id}",status_code=status.HTTP_204_NO_CONTENT )
def delete_users(user_id: int):
    db_session:Session = get_db()

    stmt = select(UserModel.id).where(UserModel.id == user_id)
    user = db_session.execute(stmt).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    stmt = delete(UserModel).where(UserModel.id == user_id)
    db_session.execute(stmt)
    db_session.commit()

    return


#@router.get("/users", response_model=List[UserSchema.UserRead])
#def get_users(qry: str = None):
#    return fake_db['users']

#@router.get("/users/{user_id}" , response_model=UserSchema.UserRead)
#def get_user_by_id(user_id: int, qry: str = None):
#    for user in fake_db["users"]:
#        if user["id"] == user_id:
#            return user
#    raise HTTPException(status_code=404, detail="User not found")

#@router.post("/users" , response_model=UserSchema.UserCreateResponse)
#def create_users(user: UserSchema.UserCreate):
#    json_compatible_user_data = jsonable_encoder(user)
#    fake_db["users"].append(json_compatible_user_data)
#    return json_compatible_user_data #JSONResponse(content=json_compatible_user_data)

#@router.delete("/users/{user_id}")
#def delete_users(user_id: int):
#    for user in fake_db["users"]:
#        if user["id"] == user_id:
#            fake_db["users"].remove(user)
#            return user
#    return {"error": "User not found"}