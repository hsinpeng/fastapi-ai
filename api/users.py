from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List

from api.depends import pagination_parms, verify_apikey
from auth.jwt import verify_access_token
from crud.users import UserCrud, get_user_crud_manager
from schemas import users as UserSchema

db_depends = Depends(get_user_crud_manager)
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
oauth2_depends = Depends(OAuth2PasswordBearer(tokenUrl="api/auth/login"))

router = APIRouter(
    tags=["users"], 
    prefix="/api",
    dependencies=[Depends(verify_apikey)]
)

### query user by id ###
@router.get("/users/{user_id}", response_model=UserSchema.UserRead)
async def get_user_by_id(user_id:int, qry:str=None, userCrud:UserCrud=db_depends):
    user = await userCrud.get_user_by_id(user_id, qry)
    if user:
        return user    
    raise HTTPException(status_code=404, detail="User not found")

### query all users ###
@router.get("/users", 
        response_model=List[UserSchema.UserRead],
        response_description="Get list of user",  
)
async def get_users(page_parms:dict=Depends(pagination_parms), userCrud:UserCrud=db_depends):
    users = await userCrud.get_users(**page_parms)
    return users

### create user ###
@router.post("/users" ,
        response_model=UserSchema.UserCreateResponse,
        status_code=status.HTTP_201_CREATED,
        response_description="Create new user"
)
async def create_user(newUser: UserSchema.UserCreate, 
                      userCrud:UserCrud=db_depends):
    # check if user already exists
    user = await userCrud.get_user_id_by_email(newUser.email)
    if user:
        raise HTTPException(status_code=409, detail=f"User already exists")
    # create user
    #newUser.password = get_password_hash(newUser.password) # hash password
    user = await userCrud.create_user(newUser)
    return vars(user)


### update user data ###
@router.put("/users/{user_id}", response_model=UserSchema.UserUpdateResponse)
async def update_users(newUser:UserSchema.UserUpdate,
                       user_id:int,
                       userCrud:UserCrud=db_depends,
                       token:str = oauth2_depends):
    # cannot update others
    payload = await verify_access_token(token)
    if payload.get("id") != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")  
    
    user = await userCrud.check_user_by_id(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    #newUser.password = get_password_hash(newUser.password) # hash password
    await userCrud.update_users(newUser, user_id)
    return newUser


### update password ###
@router.put("/users/{user_id}/password", status_code=200)
async def update_user_password(newUser:UserSchema.UserUpdatePassword,
                               user_id:int, 
                               userCrud:UserCrud=db_depends,
                               token:str = oauth2_depends):
    # cannot update others
    payload = await verify_access_token(token)
    if payload.get("id") != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")    
    
    user = await userCrud.check_user_by_id(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    #newUser.password = get_password_hash(newUser.password) # hash password
    await userCrud.update_user_password(newUser, user_id)
    return newUser


### delete user ###
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(user_id:int,
                       userCrud:UserCrud=db_depends,
                       token:str = oauth2_depends):
    # cannot delete others
    payload = await verify_access_token(token)
    if payload.get("id") != user_id:
        raise HTTPException(status_code=403, detail="Permission denied")  
    
    user = await userCrud.check_user_by_id(user_id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    
    await userCrud.delete_users(user_id)
    return