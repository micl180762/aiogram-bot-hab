from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_datas import choise_callback

all_posts = InlineKeyboardButton(text="Получать все посты",
                                 callback_data=choise_callback.new(post_type_choise='all_posts'))
profile_posts = InlineKeyboardButton(text="Поучать посты по хабам профиля",
                                     callback_data=choise_callback.new(post_type_choise='profile_posts_add'))
cancel = InlineKeyboardButton(text="Отмена", callback_data=choise_callback.new(post_type_choise='cancel'))
cancel_allez = InlineKeyboardButton(text="Отписаться",
                                    callback_data=choise_callback.new(post_type_choise='cancel_allez'))
profile_posts_other = InlineKeyboardButton(text="Поучать посты по хабам другого профиля",
                                           callback_data=choise_callback.new(post_type_choise='profile_posts_edit'))

# новый подписчик
choice = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    # [
    #     all_posts,
    # ],
    [
        profile_posts,
    ],
    [
        cancel
    ]
])

choice_cancel = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        cancel
    ]
])

# точно отписаться?
cancel_quest = InlineKeyboardMarkup(row_width=1).row(
        InlineKeyboardButton(text="Да, отписаться", callback_data='yes_unsuscribe'),
        InlineKeyboardButton(text="Отмена", callback_data='no_cancel'))


# статус нет подписок, новый/старый
choice_for_all = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        profile_posts,
    ],
    # [
    #     cancel_allez,
    # ],
    [
        cancel
    ]
])

# статус подписан на профиль
choice_for_profile = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    # [
    #     all_posts,
    # ],
    [
        profile_posts_other,
    ],
    [
        cancel_allez,
    ],
    [
        cancel
    ]
])


def user_keyboard(keyborda: str):
    if keyborda == 'new_user':
        return choice
    elif keyborda == 'in_profile':
        return choice_for_all
    else:
        return choice_for_profile
