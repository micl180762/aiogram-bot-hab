from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=4)
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Здесь можно оформить подписку на получение постов с сайта 'habr.com'",
            "Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку"
            "/subscribe - Оформить/изменить подписку")
    
    await message.answer("\n".join(text))
