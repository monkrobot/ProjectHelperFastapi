from uuid import UUID
from fastapi import APIRouter

from app.tasks.dao import TasksDAO
from app.tasks.schemas import TaskInfo


router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)


@router.get("")
async def get_tasks(id: UUID):
    return await TasksDAO.get_task_by_id(id)


@router.post("/create_task")
async def create_task(task_info: TaskInfo):
    return await TasksDAO.create(task_info)
