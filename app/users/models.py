from datetime import date, datetime
import uuid

from pytz import timezone
from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database import Base, association_table


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    telegram: Mapped[str] = mapped_column(String(30))
    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(String(30), default="user")

    tasks: Mapped[list["Tasks"]] = relationship(secondary=association_table, back_populates="executors")

    def __str__(self) -> str:
        return f"User {self.name} {self.email}"

    class Config:
        orm_mode = True
