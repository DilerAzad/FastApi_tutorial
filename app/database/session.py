from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import db_settings

engine = create_async_engine(
    url=db_settings.POSTGRES_URL,
    echo=False
)


async def create_db_tables():
    async with engine.begin() as conn:
        from .models import Shipment, Seller
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit = False,
)

async def get_session():
    async with async_session() as session:
        yield session

