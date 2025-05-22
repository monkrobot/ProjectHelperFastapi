from datetime import date, datetime
import uuid

from pytz import timezone
from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database import Base, users_groups_association_table


class Groups(Base):
    __tablename__ = "groups"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), default="Группа")
    description: Mapped[str | None] = mapped_column(String(60))
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))

    users: Mapped[list["Users"]] = relationship(
        secondary=users_groups_association_table,
        back_populates="groups",
    )

    created_date: Mapped[datetime] = mapped_column(Date, default=datetime.now(timezone('Europe/Moscow')))

    def __str__(self) -> str:
        return f"Group {self.id} {self.name}: {self.description}"

    class Config:
        orm_mode = True
