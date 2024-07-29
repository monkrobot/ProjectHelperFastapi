from fastapi import APIRouter


router = APIRouter(
    prefix="/tasks",
    tags=["Задачи"],
)


@router.get("/")
def get_tasks():
    return {"user_tasks": "user_tasks"}
