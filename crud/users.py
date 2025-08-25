import hashlib
from sqlalchemy import select, update, delete
from models.user import User as UserModel
from schemas import users as UserSchema
from database.generic import get_db
from sqlalchemy.ext.asyncio import AsyncSession

class UserCrud:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    
    async def check_user_by_id(self, user_id:int):
        stmt = select(UserModel.id).where(UserModel.id == user_id)
        result = await self.db_session.execute(stmt)
        user = result.first()
        if not user:
            return None
        return user.id
    

    # CRUD functions
    async def get_users(self, keyword:str=None, last:int=0, limit:int=50):
        stmt = select(UserModel.name, UserModel.id, UserModel.email, UserModel.avatar)
        if keyword:
            stmt = stmt.where(UserModel.name.like(f"%{keyword}%"))
        stmt = stmt.offset(last).limit(limit)
        result = await self.db_session.execute(stmt)
        users = result.all()
        return users
    

    async def get_user_by_id(self, user_id:int, qry:str=None):
        stmt = select(UserModel.name, UserModel.id, UserModel.email, UserModel.avatar).where(UserModel.id == user_id)
        result = await self.db_session.execute(stmt)
        user = result.first() 
        return user


    async def get_user_id_by_email(self, email: str):
        stmt = select(UserModel.id).where(UserModel.email == email)
        result = await self.db_session.execute(stmt)
        user = result.first() 
        if user:
            return user
        return None


    async def create_user(self, newUser:UserSchema.UserCreate):
        user = UserModel(
            name=newUser.name,
            password=newUser.password,
            age=newUser.age,
            birthday=newUser.birthday,
            email=newUser.email,
            avatar=newUser.avatar
        )
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)
        return user


    async def update_users(self, newUser:UserSchema.UserUpdate, user_id:int):
        stmt = update(UserModel).where(UserModel.id == user_id).values(
            name=newUser.name,
            password=newUser.password,
            age=newUser.age,
            birthday=newUser.birthday,
            avatar=newUser.avatar
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return


    async def update_user_password(self, newUser:UserSchema.UserUpdatePassword, user_id:int):
        stmt = update(UserModel).where(UserModel.id == user_id).values(
            password=newUser.password,
        )
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return newUser


    async def delete_users(self, user_id:int):
        stmt = delete(UserModel).where(UserModel.id == user_id)
        await self.db_session.execute(stmt)
        await self.db_session.commit()
        return
    

async def get_user_crud_manager():
    async with get_db() as db_session:
        yield UserCrud(db_session)