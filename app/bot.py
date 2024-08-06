import asyncio
import logging
import redis
from config import token_api_telegram, redis_url
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

from app.common.handlers import router as common_router
from app.auth.handlers import router as auth_router
from app.customers.handlers import router as customers_router
from app.search_love.handlers import router as search_love_router


logging.basicConfig(level=logging.INFO)

bot = Bot(token=str(token_api_telegram))

# r = redis.Redis(host='redis', port=6379, decode_responses=True, password='mypassword')

storage = RedisStorage.from_url(redis_url)

# storage = MemoryStorage()


dp = Dispatcher(storage=storage)


async def main():
    dp.include_router(common_router)
    dp.include_router(auth_router)
    dp.include_router(customers_router)
    dp.include_router(search_love_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
