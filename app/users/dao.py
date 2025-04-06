import asyncio
from uuid import uuid4
from sqlalchemy import insert
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users
# from app.tasks.router import TaskInfo


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def create(cls, data):
        async with async_session_maker() as session:
            user_info = data.model_dump()
            
            user_id = uuid4()
            user_info["id"] = user_id
            # hashed_password = 

            query = insert(cls.model).values(**user_info)
            await session.execute(query)

            await session.commit()
