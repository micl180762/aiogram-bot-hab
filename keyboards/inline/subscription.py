from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import choise_callback

# all_posts = InlineKeyboardButton(text="Получать все посты", callback_data= choise_callback.new(post_type_choise='all_posts'))
check_subs = InlineKeyboardButton(text='Check Subs',
                     callback_data=choise_callback.new(post_type_choise='check_subs'))

check_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            check_subs
        ]
    ]
)
