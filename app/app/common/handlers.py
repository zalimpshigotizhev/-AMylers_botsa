from pathlib import Path
import os 
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram import Router, types, F
from aiogram.enums import ChatAction
import redis
from app.auth.services import UserPostgresService
from utils.permissions import (
    IsAuth
)

from constants.common import (
    AUTHORIZE,
    SEARCH,
    MY_PROFILE,
    HELP,
    WELCOME_MESSAGE_IS_AUTH,
    WELCOME_MESSAGE_NOT_AUTH,
    INFO_BOT
)
from keyboards.common import make_row_keyboard, help

from config import (
    password_redis,
    host_redis,
    port_redis
)


router = Router()

r = redis.StrictRedis(
    host=host_redis,
    port=port_redis,
    password=password_redis,
    db=0,
)


@router.message(Command('start'))
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    is_auth = await UserPostgresService.is_auth(message.from_user.id)

    if is_auth:
        await message.answer(
            WELCOME_MESSAGE_IS_AUTH,
            reply_markup=make_row_keyboard([SEARCH, MY_PROFILE, HELP])
        )
        return

    welcome_text = (
        WELCOME_MESSAGE_NOT_AUTH
    )
    await message.answer(
        welcome_text,
        reply_markup=make_row_keyboard([AUTHORIZE, HELP])
    )


@router.message((F.text == '/help') | (F.text == HELP))
async def help_command(message: types.Message):
    file_path = os.path.join(os.path.dirname(__file__), 'help.jpg')

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )

    await message.answer_photo(
        photo="AgACAgIAAxkBAAO6ZqwGBYwPKvSxJYzx6bxVbBLRmiEAAuXlMRvlXGBJpfRd5oXDoSUBAAMCAAN5AAM1BA",
        caption=INFO_BOT,
        reply_markup=help()
    )


@router.callback_query(lambda c: c.data == "cancel", IsAuth())
async def cancel_delete(callback: types.CallbackQuery):
    await callback.message.delete()

# @router.message(F.photo)
# async def get_photo_id(message: types.Message):
#     await message.answer(message.photo[-1].file_id)

# @router.message()
# async def echo(message: types.Message):
#     await message.answer(message.text)
