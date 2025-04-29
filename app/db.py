# database.py
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import declarative_base

from config.settings import Settings

settings = Settings()

engine = create_async_engine(
    url=settings.database_url,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncSession:
    print("🔄 Открытие сессии")  # DEBUG
    async with SessionLocal() as session:
        yield session
    print("✅ Закрытие сессии")  # DEBUG


Base = declarative_base()