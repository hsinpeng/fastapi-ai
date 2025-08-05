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
    id: int
    age: int
    email: str
    birthday: date

class UserRead(UserBase):
    email: str