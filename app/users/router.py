from uuid import UUID
from fastapi import APIRouter
from pydantic import BaseModel

from app.users.dao import UsersDAO


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


class UserInfo(BaseModel):
    id: UUID
    name: str
    email: str
    telegram: str
    password: str
    role: str


@router.get("/{id}")
async def get_user(id: UUID):
    return await UsersDAO.find_by_id(id)


@router.post("/create_user")
async def create_user(user_info: UserInfo):
    return await UsersDAO.create(user_info)
