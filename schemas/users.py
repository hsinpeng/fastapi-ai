from typing import Union, Optional
from datetime import date
from pydantic import BaseModel, Field

#class User(BaseModel):
#    id: int
#    name: str
#    email: str
#    birthday: date

class UserBase(BaseModel):
    name: str

class UserInDB(BaseModel):
    id: int
    name: str
    password: str
    
class UserRead(UserBase):
    id: int
    name: str
    email: str
    avatar: Union[str,None] = None

class UserCreate(UserBase):
    id: int
    password: str # 新增 password 欄位
    name: str
    avatar: Optional[str] = None # 新增 avatar 欄位
    age: int
    email: str
    birthday: date

class UserCreateResponse(UserBase):
    name: str
    email: str

class UserUpdate(UserBase):
    #password: Optional[str] = Field(min_length=6)
    avatar: Optional[str] = None
    age: Optional[int] = Field(gt=0,lt=100)
    birthday: Optional[date] = Field()

class UserUpdatePassword(BaseModel):
    password:str
    
class UserUpdateResponse(UserBase):
    avatar: Optional[str] = None
    age: Optional[int] = Field(gt=0,lt=100)
    birthday: Optional[date] = Field()