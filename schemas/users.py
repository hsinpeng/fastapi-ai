from typing import Union, Optional
from datetime import date
from pydantic import BaseModel

#class User(BaseModel):
#    id: int
#    name: str
#    email: str
#    birthday: date

class UserBase(BaseModel):
    name: str

class UserCreate(UserBase):
    password: str # 新增 password 欄位
    name: str
    avatar: Optional[str] = None # 新增 avatar 欄位
    age: int
    email: str
    birthday: date

class UserCreateResponse(UserBase):
    name: str
    email: str

class UserRead(UserBase):
    name: str
    email: str
    avatar: Union[str,None] = None