from uuid import UUID
from fastapi import APIRouter

from app.groups.dao import GroupsDAO
from app.groups.schemas import GroupInfo


router = APIRouter(
    prefix="/groups",
    tags=["Группы"],
)


@router.get("")
async def get_groups(id: UUID) -> GroupInfo:
    return await GroupsDAO.get_group_by_id(id)


@router.post("/create_group")
async def create_group(group_info: GroupInfo) -> UUID:
    return await GroupsDAO.create(group_info)
