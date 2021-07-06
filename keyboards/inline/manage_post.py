from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

post_callback = CallbackData("create_post", "action")

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отправить", callback_data=post_callback.new(action="post")),
            InlineKeyboardButton(text="Отменить", callback_data=post_callback.new(action="cancel"))
        ]
    ]
)