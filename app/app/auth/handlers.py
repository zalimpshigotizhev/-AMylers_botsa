import json
import re

from aiogram import F, Router
from aiogram import types
from keyboards.common import (
    make_row_keyboard,
    delete_keyboard,
    edit_or_delete_profile,
    security_answer_for_delete_profile,
    edit_profile_keyboard
)
from utils.permissions import IsAuth, IsActivated
from aiogram.fsm.context import FSMContext
from app.auth.states import Customer
import redis

from config import (
    password_redis,
    host_redis,
    port_redis
)
from app.auth.services import UserPostgresService

from app.auth.utils import (
    is_valid_name,
    is_valid_age,
    is_valid_sex,
    is_valid_description,
)

from constants.common import (
    WELCOME_MESSAGE_IS_AUTH,
    ENTER_NAME,
    ENTER_AGE,
    ENTER_SEX,
    ENTER_DESCRIPTION,
    ENTER_PHOTO,
    MY_PROFILE,
    CANCEL,
    VALIDATION_PHOTO,
    SECURITY_QUESTION_FOR_DELETED_PROFILE,
    MESSAGE_ABOUT_CONFIRM_DELETED_PROFILE,
    SEARCH,
    AUTHORIZE,
    HELP,
    EDIT_PROFILE_TEXT,
    GIRL, BOY,
    SEX, AGE,
    ERROR_VALIDATE_NAME,
    ERROR_VALIDATE_BUTTONS,
    ERROR_VALIDATE_DESCRIPTION,
)


router = Router()

r = redis.StrictRedis(
    host=host_redis,
    port=port_redis,
    password=password_redis,
    db=0,
)


@router.message(lambda message: message.text == AUTHORIZE, IsActivated())
async def auth_trigger(message: types.Message, state: FSMContext):
    await state.set_state(Customer.name.state)
    await message.answer(text=ENTER_NAME, reply_markup=delete_keyboard())


@router.message(Customer.name)
async def process_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    
    if user_id is None:
        await state.update_data(username=message.from_user.username)
        await state.update_data(user_id=message.from_user.id)

    if is_valid_name(message.text):
        await state.update_data(name=message.text)
    else:
        await message.reply(ERROR_VALIDATE_NAME)
        return

    await state.set_state(Customer.age.state)
    await message.answer(ENTER_AGE, reply_markup=make_row_keyboard([*AGE, CANCEL]))


@router.message(Customer.age)
async def process_age(message: types.Message, state: FSMContext):
    if message.text == CANCEL:
        await state.set_state(Customer.name.state)
        await message.answer(text=ENTER_NAME, reply_markup=delete_keyboard())
        return

    if is_valid_age(message.text):
        await state.update_data(age=message.text)
    else:
        await message.reply(ERROR_VALIDATE_BUTTONS)
        return

    await state.set_state(Customer.sex.state)
    await message.answer(ENTER_SEX, reply_markup=make_row_keyboard([*SEX, CANCEL]))


@router.message(Customer.sex)
async def process_sex(message: types.Message, state: FSMContext):
    if message.text == CANCEL:
        await state.set_state(Customer.age.state)
        await message.answer(ENTER_AGE, reply_markup=make_row_keyboard([*AGE, CANCEL]))
        return

    if is_valid_sex(message.text):
        await state.update_data(sex=message.text)
    else:
        await message.reply(ERROR_VALIDATE_BUTTONS)
        return

    await state.set_state(Customer.description.state)
    await message.reply(ENTER_DESCRIPTION, reply_markup=make_row_keyboard([CANCEL]))
    

@router.message(Customer.description)
async def process_description(message: types.Message, state: FSMContext):
    if message.text == CANCEL:
        await state.set_state(Customer.sex.state)
        await message.answer(ENTER_SEX, reply_markup=make_row_keyboard([*SEX, CANCEL]))
        return
    
    if is_valid_description(message.text):
        await state.update_data(description=message.text)
    else:
        await message.reply(ERROR_VALIDATE_DESCRIPTION)
        return

    await state.set_state(Customer.photo.state)
    await message.reply(ENTER_PHOTO, reply_markup=make_row_keyboard([CANCEL]))


@router.message(Customer.photo, F.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_data = message.photo[-1]
    photo_id = photo_data.file_id
    await state.update_data(photo=photo_id, chat_id=message.chat.id)

    data = await state.get_data()
    is_auth = await UserPostgresService.is_auth(message.from_user.id)
    if is_auth and message.from_user.id == data["user_id"]:
        await UserPostgresService.update_user(data=data)
    else:
        await UserPostgresService.add_user(data=data)
    
    await state.clear()
    await message.reply(
        text=WELCOME_MESSAGE_IS_AUTH,
        reply_markup=make_row_keyboard([SEARCH, MY_PROFILE, HELP])
    )


@router.message(Customer.photo)
async def auth_state_if_not_photo(message: types.Message, state: FSMContext):
    if message.text == CANCEL:
        await state.set_state(Customer.description.state)
        await message.reply(ENTER_DESCRIPTION, reply_markup=make_row_keyboard([CANCEL]))
        return
    await message.answer(VALIDATION_PHOTO)


@router.message(lambda message: message.text == MY_PROFILE, IsAuth())
async def process_callback_button(message: types.Message, state: FSMContext):
    user = await UserPostgresService.get_user(user_id=message.from_user.id)

    await message.answer_photo(
        caption=(
            f'*{user.name}*\n' +
            f'_{user.sex} {user.age} гъэм ит_\n' + '\n' +
            f'{user.description}'
        ),
        photo=user.photo,
        reply_markup=edit_or_delete_profile(),
        parse_mode="Markdown",
    )


@router.callback_query(lambda c: c.data == "edit_profile")
async def edit_profile(callback: types.CallbackQuery):
    await callback.message.answer(
        text=EDIT_PROFILE_TEXT,
        reply_markup=edit_profile_keyboard()
    )


@router.callback_query(lambda c: c.data == "edit")
async def edit(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(Customer.name.state)
    await callback.message.answer(
        text=ENTER_NAME,
        reply_markup=delete_keyboard()
    )


@router.callback_query(lambda c: c.data == "delete_profile", IsAuth())
async def delete_profile(callback: types.CallbackQuery):
    await callback.message.answer(
        text=SECURITY_QUESTION_FOR_DELETED_PROFILE,
        reply_markup=security_answer_for_delete_profile()
    )


@router.callback_query(lambda c: c.data == "confirm_delete", IsAuth())
async def confirm_delete(callback: types.CallbackQuery):
    await UserPostgresService.delete_user(user_id=callback.from_user.id)

    await callback.message.answer(
        text=MESSAGE_ABOUT_CONFIRM_DELETED_PROFILE,
        reply_markup=make_row_keyboard([AUTHORIZE, HELP])
    )

# @router.message()
# async def echo(message: types.Message):
#     await message.answer(message.text)
