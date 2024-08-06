from aiogram.fsm.state import State, StatesGroup


class UsersList(StatesGroup):
    message_id = State()
    index = State()
    keys = State()

class SendMessageAdmin(StatesGroup):
    state_send_message_user = State()


class RegisterAdmin(StatesGroup):
    state_register_with_password = State()