import asyncio
import platform

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from config import postgres_url

# DATABASE_URL = "postgresql+asyncpg://postgres:552216742@localhost/postgres"

# Создание асинхронного движка базы данных
engine = create_async_engine(postgres_url, echo=True)

# Создание фабрики сессий
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

@asynccontextmanager
async def get_db():
    session = async_session()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()

# async def some_db_operation():
#     async with get_db() as session:
#         user = UserORM(
#             user_id=11,
#             chat_id=3,
#             name="Alsina",
#             username="aaa",
#             age="12",
#             sex="Male",
#             description="asdasd",
#             photo="axadsadasd"
#         )
#         session.add(user)
#         await session.commit()
#
# if __name__ == "__main__":
#     asyncio.run(some_db_operation())
