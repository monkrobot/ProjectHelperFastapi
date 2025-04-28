from datetime import date, datetime
import uuid

from pytz import timezone
from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database import (
    Base,
    users_friends_association_table,
    users_tasks_association_table,
    users_shoppings_association_table,
)


class Passwords(Base):
    __tablename__ = "passwords"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    hashed_password: Mapped[str] = mapped_column()
    user: Mapped["Users"] = relationship(back_populates="password")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    telegram: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30), default="user")

    friends: Mapped[list["Users"]] = relationship(
        secondary=users_friends_association_table,
        primaryjoin=(users_friends_association_table.c.user_id == id),
        secondaryjoin=(users_friends_association_table.c.friend_id == id),
        lazy='dynamic',
    )

    password: Mapped["Passwords"] = relationship(back_populates="user")

    tasks: Mapped[list["Tasks"]] = relationship(
        secondary=users_tasks_association_table,
        back_populates="executors",
    )

    shoppings: Mapped[list["Shopping"]] = relationship(
        secondary=users_shoppings_association_table,
        back_populates="executors",
    )

    def __str__(self) -> str:
        return f"User {self.name} {self.email}"

    class Config:
        orm_mode = True
