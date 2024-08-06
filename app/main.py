import asyncio
from aiogram.filters.command import Command
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from config import token_api_telegram


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=token_api_telegram)
# Диспетчер
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

users = []


class User(StatesGroup):
    name = State()
    age = State()
    user_id = State()
    description = State()
    # photo = State()




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
