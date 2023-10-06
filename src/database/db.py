import logging
from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends

from config import get_settings


logger = logging.getLogger(__name__)

s = get_settings()
db_url = f"postgresql+{s.postgres_driver}://{s.postgres_user}:{s.postgres_password}@{s.postgres_host}:{s.postgres_port}/{s.postgres_db}"

engine = create_async_engine(
    url=db_url,
    echo=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    future=True,
)


async def get_session():
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as err:
        logger.exception(err)

Session = Annotated[AsyncSession, Depends(get_session)]
