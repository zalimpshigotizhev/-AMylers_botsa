import json

from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

import redis

from keyboards.common import (delete_keyboard,
                              menu_for_admin,
                              menu_by_search)
from app.customers.states import UsersList, SendMessageAdmin, RegisterAdmin
from app.auth.states import Customer
from app.auth.handlers import auth_trigger
from app.auth.services import UserPostgresService
from constants.common import (
    MESSAGE_ALL_USERS_CHEKED,
    GIRL, BOY,
    JUNIOR,
    MIDDLE,
    SENIOR,
)
from config import (
    password_redis,
    host_redis,
    port_redis, password_for_admin
)
from utils.permissions import IsAdmin

r = redis.StrictRedis(
    host=host_redis,
    port=port_redis,
    password=password_redis,
    db=0,
)

router = Router()


@router.message(Command('stats'), IsAdmin())
async def len_users(message: types.Message):
    user_count = await UserPostgresService.user_count()
    girl_count = await UserPostgresService.user_count(sex=GIRL)
    boy_count = await UserPostgresService.user_count(sex=BOY)
    junior_count = await UserPostgresService.user_count(age=JUNIOR)
    middle_count = await UserPostgresService.user_count(age=MIDDLE)
    senior_count = await UserPostgresService.user_count(age=SENIOR)

    await message.answer(
        text=(
            "*Кол-ство всех пользователей: *" + str(user_count) + "\n" +
            "*Кол-ство женщин: *" + str(girl_count) + "\n" +
            "*Кол-ство мужчин: *" + str(boy_count) + "\n" +
            f"*{JUNIOR}: *" + str(junior_count) + "\n" +
            f"*{MIDDLE}: *" + str(middle_count) + "\n" +
            f"*{SENIOR}: *" + str(senior_count)
        ),
        parse_mode="Markdown",
    )


@router.message(Command('new_user'), IsAdmin())
async def new_user(message: types.Message, state: FSMContext):
    await state.set_state(Customer.user_id.state)
    await message.answer(text=str("Напишите id:"))


@router.message(Customer.user_id)
async def process_user_id(message: types.Message, state: FSMContext):
    await state.set_state(Customer.name.state)
    await state.update_data(user_id=int(message.text))
    await message.answer('Как вас зовут?', reply_markup=delete_keyboard())


@router.message(Command('next'), UsersList.index)
async def next(message: types.Message, state: FSMContext, is_admin: bool = False):
    data = await state.get_data()
    keys = json.loads(data.get("keys"))
    index = data.get("index") + 1

    if keys and index >= len(keys) or len(keys) == 0:
        await message.answer(MESSAGE_ALL_USERS_CHEKED)
        await state.clear()
        return

    user_id = keys[index]
    user_data = await UserPostgresService.get_user(user_id=user_id)

    if is_admin:
        representation = (
            f"Username: @{user_data.username} \n"
            f"ID: {user_data.user_id}\n"
            f"*{user_data.name}*\n"
            f"_{user_data.sex} {user_data.age} гъэм ит_\n\n"
            f"{user_data.description}"
        )
        keyboard = menu_for_admin
    else:
        representation = (
            f"*{user_data.name}*\n"
            f"_{user_data.sex} {user_data.age} гъэм ит_\n\n"
            f"{user_data.description}"
        )
        keyboard = menu_by_search

    await message.answer_photo(
        caption=representation,
        photo=user_data.photo,
        reply_markup=keyboard(),
        parse_mode="Markdown",
    )

    await state.update_data(index=index)


@router.message(Command('back'), UsersList.index)
async def back(message: types.Message, state: FSMContext, is_admin: bool = False):
    data = await state.get_data()
    keys = json.loads(data.get("keys"))
    index = data.get("index") - 1

    if index < 0:
        await message.answer(MESSAGE_ALL_USERS_CHEKED)
        await state.clear()
        return

    user_id = keys[index]

    user_data = await UserPostgresService.get_user(user_id=user_id)

    if is_admin:
        representation = (
            f"Username: @{user_data.username} \n"
            f"ID: {user_data.user_id}\n"
            f"*{user_data.name}*\n"
            f"_{user_data.sex} {user_data.age} гъэм ит_\n\n"
            f"{user_data.description}"
        )
        keyboard = menu_for_admin
    else:
        representation = (
            f"*{user_data.name}*\n"
            f"_{user_data.sex} {user_data.age} гъэм ит_\n\n"
            f"{user_data.description}"
        )
        keyboard = menu_by_search
        
    await message.answer_photo(
        caption=representation,
        photo=user_data.photo,
        reply_markup=keyboard(),
        parse_mode="Markdown",
    )
    
    await state.update_data(index=index)


@router.callback_query(lambda c: c.data == 'next_admin', IsAdmin())
async def callback_next(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await callback.message.delete()
    await next(message=message, state=state, is_admin=True)


@router.callback_query(lambda c: c.data == 'back_admin', IsAdmin())
async def callback_back(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await callback.message.delete()
    await back(message=message, state=state, is_admin=True)

@router.message(Command('id_photo'), IsAdmin())
async def id_photo(message: types.Message, state: FSMContext):
    photo_data = message.photo[-1]

    if photo_data is None:
        await message.answer(text="Нет фото")
        return
    photo_id = photo_data.file_id
    await message.answer_photo(
        photo=photo_id,
        caption=str(photo_id)
    )

@router.message(Command('all_users'), IsAdmin())
async def all_users(message: types.Message, state: FSMContext):
    user_keys = await UserPostgresService.get_indexes_users()

    if not user_keys:
        await message.answer(MESSAGE_ALL_USERS_CHEKED)
        return

    await state.set_state(UsersList.index.state)

    await state.update_data(
        index=-1,
        keys=json.dumps(user_keys),
        message_id=message.message_id
    )

    await next(message=message, state=state, is_admin=True)

@router.callback_query(lambda c: c.data == 'admin_delete_user', IsAdmin())
async def admin_deleted_user_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    keys = json.loads(data.get("keys"))
    index = data.get("index")
    user_id = keys[index]
    await UserPostgresService.delete_user(user_id=user_id)
    await callback.message.answer(
        "Deleted user."
    )


@router.callback_query(lambda c: c.data == 'admin_block_user', IsAdmin())
async def admin_block_user_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    keys = json.loads(data.get("keys"))
    index = data.get("index")
    user_id = keys[index]

    r.sadd("black_list", user_id)
    r.close()
    await UserPostgresService.delete_user(user_id=user_id)
    await callback.message.answer(
        text="Blocked user."
    )

@router.callback_query(lambda c: c.data == 'admin_message_to_user', IsAdmin())
async def admin_message_to_user_callback(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(SendMessageAdmin.state_send_message_user.state)
    await callback.message.answer(
        text="Text message:"
    )

@router.message(SendMessageAdmin.state_send_message_user)
async def send_message_user(message: types.Message, state: FSMContext):
    data = await state.get_data()
    keys = json.loads(data.get("keys"))
    index = data.get("index")
    user_id = keys[index]

    user = await UserPostgresService.get_user(user_id)

    await message.bot.send_message(
        chat_id=user.chat_id,
        text=message.text,
    )

    await message.reply(text=f"Message shipped. user_id: {user_id}")

@router.message(Command('admin'))
async def admin(message: types.Message, state: FSMContext):
    await state.set_state(RegisterAdmin.state_register_with_password.state)
    await message.answer(
        text="Please enter password for admin:"
    )

@router.message(RegisterAdmin.state_register_with_password)
async def admin_register(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if message.text == password_for_admin:
        r.sadd("admin_list", user_id)
        await message.answer(
            text="Successful registration by the administrator."
        )