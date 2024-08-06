from app.auth.models import UserORM, LikesORM
from databases.db import get_db
from sqlalchemy import select, func, and_, or_


class UserPostgresService:
    @staticmethod
    async def add_user(data: dict):
        async with get_db() as session:
            user = UserORM(
                user_id=data.get('user_id'),
                chat_id=data.get('chat_id'),
                name=data.get('name'),
                username=data.get('username'),
                age=data.get('age'),
                sex=data.get('sex'),
                description=data.get('description'),
                photo=data.get('photo'),
            )
            session.add(user)
            await session.commit()

    @staticmethod
    async def get_user(user_id: int = None, date = None) -> UserORM:
        async with get_db() as session:
            if user_id is not None:
                query = select(UserORM).where(UserORM.user_id == user_id)

            result = await session.execute(query)
            user = result.scalar_one_or_none()

        return user

    @staticmethod
    async def is_auth(user_id: int) -> bool:
        async with get_db() as session:
            query = select(UserORM).where(UserORM.user_id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()
            return user is not None

    async def update_user(data: dict):
        async with get_db() as session:
            query = select(UserORM).where(UserORM.user_id == data["user_id"])
            result = await session.execute(query)
            user = result.scalars().all()[0]
            user.name = data["name"]
            user.age = data["age"]
            user.sex = data["sex"]
            user.description = data["description"]
            user.photo = data["photo"]
            await session.commit()
    @staticmethod
    async def delete_user(user_id: int):
        async with get_db() as session:
            query = select(UserORM).where(UserORM.user_id == user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user:
                await session.delete(user)
                await session.commit()


    @staticmethod
    async def get_indexes_users(
            current_user: int = None,
            sex: str = None
    ) -> list:
        async with get_db() as session:
            query = select(UserORM.user_id)

            if sex is not None:
                subquery_1 = select(LikesORM.user_two).where(
                    and_(
                        LikesORM.user_one == current_user,
                    )
                )
                subquery_2 = select(LikesORM.user_one).where(
                    and_(
                        LikesORM.user_two == current_user,
                        LikesORM.mutually == True # noqa
                    )
                )
                query = select(UserORM.user_id).where(
                    and_(
                        UserORM.user_id.not_in(subquery_1),
                        UserORM.user_id.not_in(subquery_2),
                        UserORM.sex == sex
                    )
                )

            result = await session.execute(query)
            ids = result.scalars().all()

        return ids


    @staticmethod
    async def user_count(sex: str = None, age: str = None):
        async with get_db() as session:
            stmt = select(func.count(UserORM.user_id))

            if sex is not None:
                stmt = select(func.count(UserORM.user_id)).where(UserORM.sex == sex)
            if age is not None:
                stmt = select(func.count(UserORM.user_id)).where(UserORM.age == age)

            result = await session.execute(stmt)
            count = result.scalar_one()
            return count
class UserRedisService:
    pass




