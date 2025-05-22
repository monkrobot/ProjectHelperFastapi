from uuid import UUID

from fastapi import APIRouter

from app.users.dao import UsersDAO
from app.users.schemas import UserInfo


router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router.get("/{id}")
async def get_user(id: UUID):
    return await UsersDAO.find_by_id(id)


@router.post("/create_user")
async def create_user(user_info: UserInfo) -> UUID:
    return await UsersDAO.create(user_info)
