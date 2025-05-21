from datetime import date
from uuid import UUID

from pydantic import BaseModel


class GroupInfo(BaseModel):
    name: str
    description: str
    creator_id: UUID
    users: list[UUID]
    created_date: date
