from uuid import UUID, uuid4
from sqlalchemy import insert, select
from app.dao.base import BaseDAO
from app.database import async_session_maker, users_groups_association_table
from app.groups.models import Groups
from app.groups.schemas import GroupInfo


class GroupsDAO(BaseDAO):
    model = Groups

    @classmethod
    async def create(cls, data: GroupInfo) -> UUID:
        async with async_session_maker() as session:
            group_info = data.model_dump()
            group_id = uuid4()
            group_info["id"] = group_id

            users = group_info.pop("users")

            query = insert(cls.model).values(**group_info)
            await session.execute(query)

            insert_stmt = insert(users_groups_association_table).values([
                {"group_id": group_id, "user_id": user_id} for user_id in users
            ])
            await session.execute(insert_stmt)

            await session.commit()

            return group_id


    @classmethod
    async def get_group_by_id(cls, group_id: UUID) -> GroupInfo:
        group_data = await cls.find_by_id(group_id)

        async with async_session_maker() as session:
            query = select(users_groups_association_table).filter_by(group_id=group_id)
            result = await session.execute(query)
            users = result.scalars().all()

            group_data = GroupInfo(
                name=group_data.name,
                description=group_data.description,
                creator_id=group_data.creator_id,
                users=users,
                created_date=group_data.created_date,
            )

            return group_data
