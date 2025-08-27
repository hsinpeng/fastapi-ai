from fastapi import APIRouter, HTTPException, Depends
from schemas.auth import login_form_schema, Token, RefreshRequest
from crud.users import  UserCrud, get_user_crud_manager
from schemas.users import UserInDB
from auth.jwt import create_token_pair, verify_refresh_token
from auth.passwd import verify_password

router = APIRouter(
    tags=["auth"],
    prefix="/api/auth",
)


exception_invalid_token = HTTPException(
    status_code=401,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"}
)

exception_invalid_login = HTTPException(
    status_code=401,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"}
)

#UserCrud = get_user_crud_manager()
db_depends = Depends(get_user_crud_manager)

#@router.post("/login", response_model=Token)
#async def login(form_data: login_form_schema):
#    """
#    Login with the following information:
#    - **username**
#    - **password**
#    """
#    return {
#        "access_token": "login_access_token",
#        "refresh_token": "login_refresh_token",
#        "token_type": "bearer",
#    }

@router.post("/login",response_model=Token)
async def login(form_data:login_form_schema, userCrud:UserCrud=db_depends):
    """
    Login with the following information:

    - **username**
    - **password**

    """
    user_in_db:UserInDB = await userCrud.get_user_in_db(email=form_data.username)
    if user_in_db is None:
        raise exception_invalid_login
    if not verify_password(form_data.password, user_in_db.password):
        raise exception_invalid_login
    
    return await create_token_pair(
        {"username": user_in_db.name, "id": user_in_db.id},
        {"username": user_in_db.name, "id": user_in_db.id},
    )
    

# @router.post("/refresh", response_model=RefreshRequest)
# async def refresh(token: oauth2_token_scheme):
#     """
#     Refresh token with the following information:
#     - **token** in `Authorization` header
#     """
#     return {
#         "access_token": "new_access_token",
#         "refresh_token": "new_refresh_token",
#         "token_type": "bearer",
#     }
@router.post("/refresh",response_model=Token)
async def refresh(refersh_data: RefreshRequest):
    """
    Refresh token with the following information:

    - **token** in `Authorization` header

    """
    payload : dict = await verify_refresh_token(refersh_data.refresh_token)
    username: str = payload.get("username")
    u_id:int = payload.get("id")
    if username is None or u_id is None:
        raise  exception_invalid_token

    return await create_token_pair(
        {"username": username , "id": u_id},
        {"username": username , "id": u_id}
    )