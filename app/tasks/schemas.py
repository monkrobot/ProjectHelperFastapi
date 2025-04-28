from datetime import date
from uuid import UUID

from pydantic import BaseModel


class TaskInfo(BaseModel):
    name: str
    description: str
    creator_id: UUID
    executors: list[UUID]
    finish_date: date
    status: str