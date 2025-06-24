from datetime import datetime
import traceback
from uuid import UUID, uuid4
from sqlalchemy import insert, select, update
from sqlalchemy.dialects.postgresql import insert as psql_insert
from app.dao.base import BaseDAO
from app.database import async_session_maker, users_groups_association_table
from app.enums import Status
from app.groups.models import Groups
from app.groups.schemas import CreateGroupInfo, GroupInfo, UpdateGroupInfo


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

            if group_info["creator_id"] not in users:
                users.add(group_info["creator_id"])

            insert_stmt = insert(users_groups_association_table).values([
                {"group_id": group_id, "user_id": user_id} for user_id in users
            ])
            await session.execute(insert_stmt)

            await session.commit()

            return group_id


    @classmethod
    async def get_group_by_id(cls, group_id: UUID) -> CreateGroupInfo:
        group_data = await cls.find_by_id(group_id)

        async with async_session_maker() as session:
            query = select(users_groups_association_table).filter_by(group_id=group_id)
            result = await session.execute(query)
            users = result.scalars().all()

            group_data = CreateGroupInfo(
                name=group_data.name,
                description=group_data.description,
                creator_id=group_data.creator_id,
                users=users,
                created_date=group_data.created_date,
            )

            return group_data


    @classmethod
    async def update_group_by_id(cls, group_id: UUID, data: UpdateGroupInfo) -> Status:
        group_info = data.model_dump()
        group_info = {param: value for param, value in group_info.items() if value is not None}
        group_info['updated_date'] = datetime.now()
        users_groups = group_info.pop('users')

        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == group_id).values(**group_info)

            if users_groups:
                query_users_groups = psql_insert(users_groups_association_table).values([
                    {"group_id": group_id, "user_id": user_id} for user_id in users_groups
                ]).on_conflict_do_nothing(index_elements=["group_id", "user_id"])
            try:
                await session.execute(query)
                await session.execute(query_users_groups)
            except Exception:
                await session.rollback()
                traceback.print_exc()
                return Status.failed

            await session.commit()
            return Status.success
