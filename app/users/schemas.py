from uuid import UUID
from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    email: str
    telegram: str
    role: str


class GetUserInfo(UserInfo):
    id: UUID


class GetUserInfoFriends(GetUserInfo):
    friends: list[GetUserInfo]


class CreateUserInfo(UserInfo):
    password: str
