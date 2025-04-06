from datetime import date, datetime
import uuid

from pytz import timezone
from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database import Base, association_table


class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), default="Покупки")
    description: Mapped[str] = mapped_column(String)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))

    executors: Mapped[list["Users"]] = relationship(secondary=association_table, back_populates="tasks")

    created_date: Mapped[datetime] = mapped_column(Date, default=datetime.now(timezone('Europe/Moscow')))
    finish_date: Mapped[date] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30))

    def __str__(self) -> str:
        return f"Tasks list {self.id} {self.name}: {self.description}"

    class Config:
        orm_mode = True
