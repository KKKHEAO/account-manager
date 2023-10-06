from sqlalchemy import insert, select

from database.db import Session


class BaseRepo:
    model = None
    async_session: Session

    def __init__(self, async_session: Session) -> None:
        self.async_session = async_session

    async def add(self, data: dict):
        async with self.async_session.begin() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_by_value(self, **kwargs):
        async with self.async_session() as session:
            stmt = select(self.model).filter_by(**kwargs)
            res = await session.execute(stmt)
            return res.scalar()
