from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from config import Settings

def create_db_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        url=settings.database_url,
        echo=False,
        pool_pre_ping=True,
    )

def create_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )