from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from constants.common import (
    DONATE_DEV,
    DELETE_PROFILE,
    CONNECT_DEV,
    EDIT_PROFILE,
    DELETE_PROFILE,
    YES_DELETED_PROFILE,
    NO_DELETED_PROFILE,
    CANCEL,
    PREVIEW_PROFILE,

)


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    """
    Создаёт реплай-клавиатуру с кнопками в один ряд
    :param items: список текстов для кнопок
    :return: объект реплай-клавиатуры
    """
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def delete_keyboard():
    return ReplyKeyboardRemove()


def help():
    buttons = [
        [InlineKeyboardButton(text=DONATE_DEV, url="https://www.sberbank.com/sms/pbpn?requisiteNumber=79889251000")],
        [InlineKeyboardButton(text=CONNECT_DEV, url="tg://resolve?domain=AdygaGods")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def menu_by_search():
    buttons = [
        [InlineKeyboardButton(text="🍎", callback_data="like")],
        [InlineKeyboardButton(text="<<", callback_data="back"), InlineKeyboardButton(text=">>", callback_data="next")],
        
        
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def menu_for_admin():
    buttons = [
        [InlineKeyboardButton(text="<<", callback_data="back_admin"), InlineKeyboardButton(text=">>", callback_data="next_admin")],
        [InlineKeyboardButton(text="Удалить аккаунт", callback_data="admin_delete_user")],
        [InlineKeyboardButton(text="Add black list", callback_data="admin_block_user")],
        [InlineKeyboardButton(text="Отправить сообщение пользователю", callback_data="admin_message_to_user")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_or_delete_profile():
    buttons = [
        [InlineKeyboardButton(text=EDIT_PROFILE, callback_data="edit_profile")],
        [InlineKeyboardButton(text=DELETE_PROFILE, callback_data="delete_profile")],
        [InlineKeyboardButton(text=CANCEL, callback_data="cancel")],
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def security_answer_for_delete_profile():
    buttons = [
        [InlineKeyboardButton(text=YES_DELETED_PROFILE, callback_data="confirm_delete")],
        [InlineKeyboardButton(text=NO_DELETED_PROFILE, callback_data="cancel")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def edit_profile_keyboard():
    buttons = [
        [InlineKeyboardButton(text=EDIT_PROFILE, callback_data="edit")],
        [InlineKeyboardButton(text=CANCEL, callback_data="cancel")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def preview_like():
    buttons = [
        [InlineKeyboardButton(text=PREVIEW_PROFILE, callback_data="preview_profile")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def mutually_like():
    buttons = [
        [InlineKeyboardButton(text="🍎", callback_data="mutually")],
        [InlineKeyboardButton(text=">>", callback_data="not_mutually")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def back_preview():
    buttons = [
        [InlineKeyboardButton(text=CANCEL, callback_data="back_preview")],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard