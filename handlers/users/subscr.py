from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery
import re
from loader import dp, db, bot
from aiogram import types
from keyboards.inline.choice_buttons import user_keyboard
from keyboards.inline.callback_datas import choise_callback
from utils.misc import rate_limit
from utils.habr.HabrUser import get_user_tags

from data.config import channels
from utils.misc.subscription import check
from keyboards.inline.subscription import check_button


@rate_limit(limit=4)
@dp.message_handler(Command('sb'), state=None)
async def show_items(message: types.Message, user: dict):
    chat = await bot.get_chat(channels[0])
    invite_link = await chat.export_invite_link()
    channels_format = f" <a href='{invite_link}'>Ссылка</a>"

    await message.answer(f"Привет, <b>{user['name']}</b>", parse_mode="HTML")
    if user['new_user']:
        str_for_new = f"Вы новый посетитель, здесь можно оформить рассылки на Хабр-новости\n"
    else:
        str_for_new = ''
        # await message.answer(f"Вы новый посетитель, здесь можно оформить рассылки на Хабр-новости", reply_markup=user_keyboard('new_user'))
    answer = str_for_new + f"Вот {channels_format} на канал с новостной лентой <a href='https://habr.com/ru/all'>Хабра</a>"

    if user['channel']:
        answer +='\n( вы на него подписаны )'
    await message.answer(answer)
    if user['habr_account']:
        await message.answer(f"Вы подписаны на рассылки как <b>{user['status']}</b>", reply_markup=user_keyboard('change_profile'))
    else:
        await message.answer(f"Можно подписаться на рассылки по любому профилю Хабра", reply_markup=user_keyboard('in_profile'))

