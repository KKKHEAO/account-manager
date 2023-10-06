import datetime as dt

from sqlalchemy import DateTime, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import functions as sa_functions

from .base import Base


class User(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(
        String(length=64), nullable=False, unique=True)

    hashed_password: Mapped[bytes] = mapped_column(
        LargeBinary(length=1024), nullable=False)

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=sa_functions.now())
