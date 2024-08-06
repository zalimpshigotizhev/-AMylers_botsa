import datetime

from sqlalchemy import text, ForeignKey, BigInteger
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from config import Base



class UserORM(Base):
    __tablename__ = 'users'
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str]
    username: Mapped[str | None]
    age: Mapped[str]
    sex: Mapped[str]
    description: Mapped[str]
    photo: Mapped[str]


class LikesORM(Base):
    __tablename__ = 'likes'
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_one: Mapped[UserORM] = mapped_column(ForeignKey(column="users.user_id", ondelete="CASCADE"))
    user_two: Mapped[UserORM] = mapped_column(ForeignKey(column="users.user_id", ondelete="CASCADE"))
    mutually: Mapped[bool]

