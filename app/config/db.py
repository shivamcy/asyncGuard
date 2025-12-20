from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from app.config.settings import settings

Base = declarative_base()
#for alembic only 
sync_engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
)
_async_engine = None
_async_session_factory = None


def get_async_engine():
    global _async_engine
    if _async_engine is None:
        async_url = settings.DATABASE_URL.replace(
            "postgresql+psycopg2", "postgresql+asyncpg"  #converting it so that we can have async engine
        )
        _async_engine = create_async_engine(
            async_url,
            echo=False,
        )
    return _async_engine


def get_async_session():
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = sessionmaker(
            bind=get_async_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


async def get_db():
    async_session = get_async_session()
    async with async_session() as session:
        yield session
