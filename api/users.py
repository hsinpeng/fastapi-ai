from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from schemas import users as UserSchema
from database.generic import get_db
from api.depends import pagination_parms, test_verify_token
from crud import users as UserCrud

db_depends = Depends(get_db)

router = APIRouter(
    tags=["users"], 
    prefix="/api",
    dependencies=[Depends(test_verify_token)]
)

### query user by id ###
@router.get("/users/{user_id}", response_model=UserSchema.UserRead)
async def get_user_by_id(user_id:int, qry:str=None, db_session=db_depends):
    user = await UserCrud.get_user_by_id(db_session, user_id, qry)
    if user:
        return user    
    raise HTTPException(status_code=404, detail="User not found")


### query all users ###
@router.get("/users", 
        response_model=List[UserSchema.UserRead],
        response_description="Get list of user",  
)
async def get_users(page_parms:dict= Depends(pagination_parms), db_session=db_depends):
    users = await UserCrud.get_users(db_session, **page_parms)
    return users


### create user ###
@router.post("/users" ,
        response_model=UserSchema.UserCreateResponse,
        status_code=status.HTTP_201_CREATED,
        response_description="Create new user"
)
async def create_user(newUser: UserSchema.UserCreate, db_session=db_depends):
    # check if user already exists
    user = await UserCrud.get_user_id_by_email(db_session, newUser.email)
    if user:
        raise HTTPException(status_code=409, detail=f"User already exists")
    # create user
    user = await UserCrud.create_user(db_session, newUser)
    return vars(user)


### update user data ###
@router.put("/users/{user_id}", response_model=UserSchema.UserUpdateResponse)
async def update_users(newUser:UserSchema.UserUpdate, user_id:int, db_session=db_depends):
    user = await UserCrud.check_user_by_id(db_session, user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await UserCrud.update_users(db_session, newUser, user_id)
    return newUser


### update password ###
@router.put("/users/{user_id}/password", status_code=200)
async def update_user_password(newUser:UserSchema.UserUpdatePassword, user_id:int, db_session=db_depends):
    user = await UserCrud.check_user_by_id(db_session, user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await UserCrud.update_user_password(db_session, newUser, user_id)
    return newUser


### delete user ###
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(user_id:int, db_session=db_depends):
    user = await UserCrud.check_user_by_id(db_session, user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await UserCrud.delete_users(db_session, user_id)
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