import hashlib
from uuid import UUID, uuid4
from sqlalchemy import insert, select
from app.dao.base import BaseDAO
from app.database import async_session_maker, users_friends_association_table
from app.users.models import Users, Passwords


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def create(cls, data):
        async with async_session_maker() as session:
            user_info = data.model_dump()
            
            user_id = uuid4()
            user_info["id"] = user_id
            
            salt = 'alsfgornwvuret34634'.encode("utf-8")
            hashed_password = hashlib.sha256(user_info.pop('password').encode("utf-8") + salt).hexdigest()

            query = insert(cls.model).values(**user_info)
            await session.execute(query)

            query_password = insert(Passwords).values({
                "user_id": user_id,
                "hashed_password": hashed_password
            })

            await session.execute(query_password)

            await session.commit()

    @classmethod
    async def find_by_id(cls, model_id: UUID):
        model =  await super().find_by_id(model_id)
        async with async_session_maker() as session:
            query = select(cls.model).select_from(
                users_friends_association_table.join(
                    cls.model,
                    users_friends_association_table.c.friend_id == cls.model.id
                )
            ).where(
                users_friends_association_table.c.user_id == model_id
            )
            model_friends = await session.execute(query)
            model_friends = model_friends.mappings()
        return model, {"friends": [i for i in model_friends]}
