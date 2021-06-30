from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

all_posts = InlineKeyboardButton(text="Получать все посты",
                                 callback_data='all_posts')
profile_posts = InlineKeyboardButton(text="Поучать посты по хабам профиля",
                                     callback_data='profile_posts_add')
cancel = InlineKeyboardButton(text="Отмена", callback_data='cancel')
cancel_allez = InlineKeyboardButton(text="Отписаться",
                                    callback_data='cancel_allez')
profile_posts_other = InlineKeyboardButton(text="Поучать посты по хабам другого профиля",
                                           callback_data='profile_posts_add')

# новый подписчик
choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        profile_posts,
    ],
    [
        cancel
    ]
])

choice_cancel = InlineKeyboardMarkup(inline_keyboard=[
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
    [
        cancel
    ]
])

# статус подписан на профиль
choice_for_profile = InlineKeyboardMarkup(inline_keyboard=[
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
