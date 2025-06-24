from datetime import date
from uuid import UUID

from pydantic import BaseModel


class GroupInfo(BaseModel):
    name: str
    description: str
    creator_id: UUID
    users: set[UUID]


class CreateGroupInfo(GroupInfo):
    created_date: date


class UpdateGroupInfo(GroupInfo):
    name: str | None
    description: str | None
    creator_id: UUID | None
    users: set[UUID] | None
