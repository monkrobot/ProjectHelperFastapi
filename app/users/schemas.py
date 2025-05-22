from uuid import UUID

from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    email: str
    telegram: str
    password: str
    role: str
