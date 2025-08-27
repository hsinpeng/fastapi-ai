from datetime import datetime, timedelta, UTC
from jose import jwt
from jose.exceptions import ExpiredSignatureError , JWTError
from fastapi import HTTPException

from setting.config import get_settings
from schemas.auth import Token

settings = get_settings()

async def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.access_token_secret)
    return encoded_jwt

async def create_refresh_token(data:dict):   
    to_encode = data.copy()
    expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=settings.refresh_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.refresh_token_secret)
    return encoded_jwt


async def create_token_pair(access_data:dict,refresh_data:dict) -> Token:
    access_token = await create_access_token(access_data)
    refresh_token = await create_refresh_token(refresh_data)
    return Token(access_token=access_token,refresh_token=refresh_token,token_type="bearer")


async def verify_refresh_token(token:str):
    try:
        payload = jwt.decode(token, settings.refresh_token_secret)
        return payload
    except ExpiredSignatureError:
        raise  HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise  HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    

async def verify_access_token(token:str):
    print("verify_access_token")
    try:
        payload = jwt.decode(token, settings.access_token_secret)
        print("payload",payload)
        return payload
    except ExpiredSignatureError:
        raise  HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise  HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )