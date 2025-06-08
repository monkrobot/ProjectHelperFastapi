from datetime import date
from uuid import UUID

from pydantic import BaseModel


class GroupInfo(BaseModel):
    name: str
    description: str
    creator_id: UUID
    users: list[UUID]
    created_date: date


class UpdateGroupInfo(BaseModel):
    name: str | None
    description: str | None
    creator_id: UUID | None
    users: list[UUID] | None
    updated_date: date
