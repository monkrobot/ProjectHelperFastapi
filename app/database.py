from sqlalchemy import Column, ForeignKey, Table, event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Mapper

from app.config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
)


@event.listens_for(Mapper, "before_configured", once=True)
def go():
    from app.users.models import Users
    from app.tasks.models import Tasks
    from app.shopping.models import Shopping
