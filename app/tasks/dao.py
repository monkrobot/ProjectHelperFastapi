from uuid import uuid4
from sqlalchemy import insert, select
from app.dao.base import BaseDAO
from app.database import async_session_maker, users_tasks_association_table
from app.tasks.models import Tasks
from app.tasks.schemas import TaskInfo


class TasksDAO(BaseDAO):
    model = Tasks

    @classmethod
    async def create(cls, data):
        async with async_session_maker() as session:
            task_info = data.model_dump()
            # executors = task_info.pop("executors")
            task_id = uuid4()
            task_info["id"] = task_id

            executors = task_info.pop("executors")

            query = insert(cls.model).values(**task_info)
            await session.execute(query)

            insert_stmt = insert(users_tasks_association_table).values([
                {"task_id": task_id, "user_id": user_id} for user_id in executors
            ])
            await session.execute(insert_stmt)

            await session.commit()

            return task_id


    @classmethod
    async def get_task_by_id(cls, task_id):
        task_data = await cls.find_by_id(task_id)

        async with async_session_maker() as session:
            query = select(users_tasks_association_table).filter_by(task_id=task_id)
            result = await session.execute(query)
            executors = result.scalars().all()

            task_data = TaskInfo(
                name=task_data.name,
                description=task_data.description,
                creator_id=task_data.creator_id,
                executors=executors,
                finish_date=task_data.finish_date,
                status=task_data.status,
            )

            return task_data
