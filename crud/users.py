import hashlib
from sqlalchemy import select, update, delete
from models.user import User as UserModel 
from schemas import users as UserSchema
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_id_by_email(db_session:AsyncSession, email: str):
    stmt = select(UserModel.id).where(UserModel.email == email)
    user = db_session.execute(stmt).first()
    if user:
        return user
    return None


async def create_user(db_session:AsyncSession, newUser: UserSchema.UserCreate ):
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
    return user


async def get_users(db_session:AsyncSession, keyword:str=None,last:int=0,limit:int=50):
    stmt = select(UserModel.name,UserModel.id,UserModel.email,UserModel.avatar)
    if keyword:
        stmt = stmt.where(UserModel.name.like(f"%{keyword}%"))
    stmt = stmt.offset(last).limit(limit)
    result = db_session.execute(stmt)
    users = result.all()

    return users

async def get_user_by_id(db_session:AsyncSession, user_id:int, qry:str=None):
    stmt = select(UserModel.name,UserModel.id,UserModel.email,UserModel.avatar).where(UserModel.id == user_id)
    user = db_session.execute(stmt).first()
    return user


async def update_users(db_session:AsyncSession, newUser:UserSchema.UserUpdate, user_id:int):
    stmt = update(UserModel).where(UserModel.id == user_id).values(
        name=newUser.name,
        password=newUser.password,
        age=newUser.age,
        birthday=newUser.birthday,
        avatar=newUser.avatar
    )
    db_session.execute(stmt)
    db_session.commit()
    return


async def update_user_password(db_session:AsyncSession, newUser:UserSchema.UserUpdatePassword, user_id:int):
    stmt = update(UserModel).where(UserModel.id == user_id).values(
        password=newUser.password,
    )
    db_session.execute(stmt)
    db_session.commit()
    return newUser


async def delete_users(db_session:AsyncSession, user_id:int):
    stmt = delete(UserModel).where(UserModel.id == user_id)
    db_session.execute(stmt)
    db_session.commit()
    return