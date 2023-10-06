import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Type


class DBTable(DeclarativeBase):
    metadata: sa.MetaData = sa.MetaData()

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")


Base: Type[DeclarativeBase] = DBTable
