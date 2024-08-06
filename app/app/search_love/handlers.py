import json
import random
import os

from aiogram import Router, types, F
import redis
from aiogram.types import InputMediaPhoto

from app.auth.services import UserPostgresService


from app.customers.states import UsersList
from app.customers.handlers import next, back
from aiogram.fsm.context import FSMContext

from config import (
    password_redis,
    host_redis,
    port_redis
)
from app.auth.services import UserPostgresService
from app.search_love.services import LikeService
from constants.common import (
    SEARCH,
    BOY, GIRL,
    LIKE_IT,
    MESSAGE_IF_MUTUAL_LIKE,
    MESSAGE_LIKED_CUSTOMER,
    MESSAGE_LIKED_CUSTOMER2, APPLE, MESSAGE_MUTUALLY

)

from keyboards.common import (
    menu_by_search,
    preview_like,
    mutually_like,
    back_preview
)
from utils.permissions import IsAuth

r = redis.StrictRedis(
    host=host_redis,
    port=port_redis,
    password=password_redis,
    db=0,
)

router = Router()


@router.callback_query(lambda c: c.data == 'next')
async def callback_next(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await callback.message.delete()
    await next(message=message, state=state, is_admin=False)


@router.callback_query(lambda c: c.data == 'back')
async def callback_back(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await callback.message.delete()
    await back(message=message, state=state, is_admin=False)


@router.message(lambda message: message.text == SEARCH, IsAuth())
async def search_handler(message: types.Message, state: FSMContext, current_user_id: int = None):

    if current_user_id is None:
        current_user_id = message.from_user.id


    current_user = await UserPostgresService.get_user(current_user_id)

    if current_user.sex == BOY:
        user_ids = await UserPostgresService.get_indexes_users(
            current_user=current_user_id, sex=GIRL
        )
    else:
        user_ids = await UserPostgresService.get_indexes_users(
            current_user=current_user_id, sex=BOY
        )

    await state.set_state(UsersList.index.state)
    await state.update_data(
        index=-1,
        keys=json.dumps(user_ids),
        message_id=message.message_id
    )

    await next(message=message, state=state, is_admin=False)


@router.callback_query(lambda callback: callback.data == "mutually")
async def mutually_callback(callback: types.CallbackQuery, state: FSMContext):
    like = await LikeService.get_like(date=callback.message.date, user_two_id=callback.from_user.id)
    user_one = await UserPostgresService.get_user(user_id=like.user_one)
    user_two = await UserPostgresService.get_user(user_id=like.user_two)


    if like.mutually is False:
        await LikeService.muttualy_true(like_id=like.id)
        await callback.message.bot.send_photo(
            chat_id=user_one.chat_id,
            caption=(
                MESSAGE_MUTUALLY + f"@{user_two.username}"
            ),
            photo=user_two.photo
        )

    await callback.message.answer(
        text=(
                MESSAGE_MUTUALLY + f"@{user_one.username}"
        )
    )


@router.callback_query(lambda callback: callback.data == "like")
async def like_handlers(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lst = json.loads(data["keys"])
    index = data.get("index")
    user_id = lst[index]

    current_user = await UserPostgresService.get_user(user_id=callback.from_user.id)
    user_two = await UserPostgresService.get_user(user_id=user_id)

    is_favorite = await LikeService.is_favorite(
        current_user=callback.from_user.id, user_one=user_two.user_id
    )
    if is_favorite:
        await mutually_callback(callback=callback, state=state)
        return

    await LikeService.add_like(
        user_one=current_user,
        user_two=user_two,
    )
    file_path = os.path.join(os.path.dirname(__file__), '1.png')
    photo = types.FSInputFile(path=file_path)

    await callback.message.answer_photo(
        photo=photo,
        caption=(
            f"{LIKE_IT} *{user_two.name}*\n" +
            MESSAGE_IF_MUTUAL_LIKE
        ),
        reply_markup=preview_like(),
        parse_mode="Markdown",
    )

    await callback.message.bot.send_photo(
        chat_id=int(user_two.chat_id),
        caption=(
            MESSAGE_LIKED_CUSTOMER + "\n" +
            f"*{current_user.name}*" + "\n" +
            f"_{current_user.sex} {current_user.age} гъэм ит_" + "\n" + "\n" +
            current_user.description + "\n" + "\n" +
            MESSAGE_LIKED_CUSTOMER2
        ),
        reply_markup=mutually_like(),
        parse_mode="Markdown",
        photo=current_user.photo
    )

    await callback_next(callback=callback, state=state)





@router.callback_query(lambda callback: callback.data == "not_mutually")
async def not_mutually_callback(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await search_handler(message=message, state=state, current_user_id=callback.from_user.id)


@router.callback_query(lambda callback: callback.data == "preview_profile")
async def preview_profile_callback(callback: types.CallbackQuery, state: FSMContext):
    like = await LikeService.get_like(
        user_one_id=callback.from_user.id,
        date=callback.message.date,
    )

    user_two = await UserPostgresService.get_user(user_id=like.user_two)

    media = InputMediaPhoto(
        media=user_two.photo,
        caption=(
            f"{LIKE_IT} *{user_two.name}*" + "\n" +
            f"_{user_two.sex} - {user_two.age} гъэм ит_" + "\n" + "\n" +
            f"{user_two.description}"
        ),
        parse_mode="Markdown"
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=back_preview()
    )


@router.callback_query(lambda callback: callback.data == "back_preview")
async def back_preview_callback(callback: types.CallbackQuery, state: FSMContext):
    like = await LikeService.get_like(
        user_one_id=callback.from_user.id,
        date=callback.message.date,
    )

    user_two = await UserPostgresService.get_user(user_id=like.user_two)
    file_path = os.path.join(os.path.dirname(__file__), '1.png')
    photo = types.FSInputFile(path=file_path)

    media = InputMediaPhoto(
        media=photo,
        caption=(
            f"{LIKE_IT} *{user_two.name}*\n" +
            MESSAGE_IF_MUTUAL_LIKE
        ),
        parse_mode="Markdown"
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=preview_like()
    )