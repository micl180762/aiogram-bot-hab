from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.misc.throttling import rate_limit
from utils.misc.states import states


@rate_limit(limit=5)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, user: dict):  # user: dict данные из middleware
    if user['status'] == 'new_user':
        await message.answer(f"Привет, {message.from_user.full_name}!\nздесь вы можете оформить рассылку на посты с "
                             f" <a>habr.com</a> введите команду /subscribe и следуйте иннструкциям")
    else:
        # если все посты - берем из словаря, иначе профиль из базы (user)
        stat = states.get(user['status'], f'Профиль - <b>{user["status"]}</b>')
        await message.answer(f"И снова здравствуйте, "
                             f"<b>{message.from_user.full_name}</b>!\nваш статус подписки: {stat}\n"
                             f"вы можете изменить параметры рассылки "
                             f"\n на посты с <a>habr.com</a> (команда /subscribe)")
