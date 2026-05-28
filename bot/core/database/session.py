from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from bot.core import configuration

engine = create_async_engine(
    configuration.database_url,
    echo=configuration.sql_echo,
    pool_pre_ping=True,
)

session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
