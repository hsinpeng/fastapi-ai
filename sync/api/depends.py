from fastapi import HTTPException
from fastapi.params import Header
from sqlalchemy.orm import Session
from sqlalchemy import select 
from typing import Optional
from models.user import User as UserModel
from sync.database.generic import get_db

def check_user_id(user_id:int):
    db_session:Session = get_db()
    stmt = select(UserModel.id).where(UserModel.id == user_id)
    user = db_session.execute(stmt).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.id

def pagination_parms(keyword:Optional[str]=None, last:int=0, limit:int=50):
    return {
        "keyword":keyword,
        "last":last,
        "limit":limit
    }

def test_verify_token(verify_header:str = Header()):
    if verify_header != "1234567890":
        raise HTTPException(status_code=403, detail="Forbidden")
    return verify_header