
from aiogram.fsm.state import State, StatesGroup


class Customer(StatesGroup):
    user_id = State()
    name = State()
    age = State()
    sex = State()
    description = State()
    photo = State()


