from datetime import date, datetime
import uuid

from pytz import timezone
from sqlalchemy import UUID, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database import Base, users_shoppings_association_table


class Shopping(Base):
    __tablename__ = "shopping"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), default="Покупки")
    shopping_list: Mapped[list[str]] = mapped_column(String)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"))

    executors: Mapped[list["Users"]] = relationship(
        secondary=users_shoppings_association_table,
        back_populates="shoppings",
    )

    created_date: Mapped[datetime] = mapped_column(Date, default=datetime.now(timezone('Europe/Moscow')))
    finish_date: Mapped[date] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(30))

    def __str__(self) -> str:
        return f"Shopping list {self.id} {self.name}: {self.shopping_list}"

    class Config:
        orm_mode = True
