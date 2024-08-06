from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.types import Message
import redis
from app.auth.services import UserPostgresService

from keyboards.common import make_row_keyboard
from constants.common import (
    MESSAGE_PROFILE_404,
    AUTHORIZE,
    HELP
)

from config import (
    password_redis,
    host_redis,
    port_redis
)


r = redis.StrictRedis(
    host=host_redis,
    port=port_redis,
    password=password_redis,
    db=0,
)


class IsAuth(BaseFilter):
    async def __call__(self, message: types.Message):
        user_id = message.from_user.id
        is_auth = await UserPostgresService.is_auth(user_id=user_id)
        if is_auth:
            return is_auth
        await message.answer(
            text=MESSAGE_PROFILE_404,
            reply_markup=make_row_keyboard([AUTHORIZE, HELP])
         )
        return


class IsActivated(BaseFilter):
    async def __call__(self, message: types.Message):
        user_id = message.from_user.id
        if not r.sismember("black_list", str(user_id)):
            return True
        return False


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message):
        user_id = message.from_user.id
        if r.sismember("admin_list", str(user_id)):
            return True
        return False



