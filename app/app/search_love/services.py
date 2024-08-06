import datetime

from databases.db import get_db
from app.auth.models import LikesORM
from sqlalchemy import select, func, literal, and_


class LikeService:
    @staticmethod
    async def add_like(user_one, user_two):
        async with get_db() as session:
            like = LikesORM(
                user_one=user_one.user_id,
                user_two=user_two.user_id,
                mutually=False
            )

            session.add(like)
            await session.commit()


    async def get_like(
            like_id: int | None = None,
            date = None,
            user_one_id: int = None,
            user_two_id: int = None,
    ):
        async with get_db() as session:
            if like_id is not None:
                query = select(LikesORM).where(LikesORM.id == like_id)

            if date is not None and user_two_id is not None:
                query = (
                    select(
                        LikesORM
                    ).where(
                        LikesORM.user_two == user_two_id
                    ).order_by(
                        func.abs(
                            func.extract('epoch', LikesORM.created_at) - func.extract('epoch', date)).asc()
                    ).limit(1)
                )

            if date is not None and user_one_id is not None:
                query = (
                    select(
                        LikesORM
                    ).where(
                        LikesORM.user_one == user_one_id
                    ).order_by(
                        func.abs(
                            func.extract('epoch', LikesORM.created_at) - func.extract('epoch', date)).asc()
                    ).limit(1)
                )
            result = await session.execute(query)
            like = result.scalar_one_or_none()
        return like

    @staticmethod
    async def muttualy_true(like_id: int):
        async with get_db() as session:
            query = select(LikesORM).where(LikesORM.id == like_id)
            result = await session.execute(query)
            like = result.scalar_one_or_none()
            like.mutually = True
            await session.commit()


    @staticmethod
    async def is_favorite(current_user: int, user_one: int = None):
        async with get_db() as session:
            if user_one is not None:
                query = select(LikesORM).where(
                    and_(
                        LikesORM.user_one == user_one,
                        LikesORM.user_two == current_user
                    )
                )
                result = await session.execute(query)
                like = result.scalar_one_or_none()


            if like is not None:
                return True
            return False