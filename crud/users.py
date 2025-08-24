import hashlib
from sqlalchemy import select, update, delete
from models.user import User as UserModel 
from schemas import users as UserSchema
from sqlalchemy.ext.asyncio import AsyncSession

async def check_user_by_id(db_session:AsyncSession, user_id:int):
    stmt = select(UserModel.id).where(UserModel.id == user_id)
    #user = await db_session.execute(stmt).first()
    result = await db_session.execute(stmt)
    user = result.first()
    if not user:
        return None
    return user.id


async def get_user_by_id(db_session:AsyncSession, user_id:int, qry:str=None):
    stmt = select(UserModel.name,UserModel.id,UserModel.email,UserModel.avatar).where(UserModel.id == user_id)
    #user = await db_session.execute(stmt).first()
    result = await db_session.execute(stmt)
    user = result.first() 
    return user


async def get_user_id_by_email(db_session:AsyncSession, email: str):
    stmt = select(UserModel.id).where(UserModel.email == email)
    #user = await db_session.execute(stmt).first()
    result = await db_session.execute(stmt)
    user = result.first() 
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
    await db_session.commit()
    await db_session.refresh(user)
    return user


async def get_users(db_session:AsyncSession, keyword:str=None,last:int=0,limit:int=50):
    stmt = select(UserModel.name,UserModel.id,UserModel.email,UserModel.avatar)
    if keyword:
        stmt = stmt.where(UserModel.name.like(f"%{keyword}%"))
    stmt = stmt.offset(last).limit(limit)
    result = await db_session.execute(stmt)
    users = result.all()

    return users



async def update_users(db_session:AsyncSession, newUser:UserSchema.UserUpdate, user_id:int):
    stmt = update(UserModel).where(UserModel.id == user_id).values(
        name=newUser.name,
        password=newUser.password,
        age=newUser.age,
        birthday=newUser.birthday,
        avatar=newUser.avatar
    )
    await db_session.execute(stmt)
    await db_session.commit()
    return


async def update_user_password(db_session:AsyncSession, newUser:UserSchema.UserUpdatePassword, user_id:int):
    stmt = update(UserModel).where(UserModel.id == user_id).values(
        password=newUser.password,
    )
    await db_session.execute(stmt)
    await db_session.commit()
    return newUser


async def delete_users(db_session:AsyncSession, user_id:int):
    stmt = delete(UserModel).where(UserModel.id == user_id)
    await db_session.execute(stmt)
    await db_session.commit()
    return