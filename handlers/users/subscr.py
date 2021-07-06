from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
import re
from loader import dp, db, bot
from keyboards.inline.choice_subs import choice_for_all, choice_for_profile, choice_cancel, \
    cancel_quest
from utils.misc import rate_limit
from utils.habr.HabrUser import get_user_tags
from data.config import channels
from states.profile_state import ChangeProfile  # все состояния для команды


@rate_limit(limit=4)
@dp.message_handler(Command('subscribe'), state=None)
async def show_items(message: Message, user: dict):
    await ChangeProfile.Subscribe_State.set()
    chat = await bot.get_chat(channels[0])
    invite_link = await chat.export_invite_link()
    channels_format = f" <a href='{invite_link}'>Ссылка</a>"

    await message.answer(f"Привет, <b>{user['name']}</b>", parse_mode="HTML")
    if user['new_user']:
        str_for_new = f"Вы новый посетитель, здесь можно оформить рассылки на Хабр-новости\n"
    else:
        str_for_new = ''
    answer = \
        str_for_new + f"Вот {channels_format} на канал с новостной лентой <a href='https://habr.com/ru/all'>Хабра</a>"

    if user['channel']:
        answer += '\n( вы на него подписаны )'
    await message.answer(answer)
    if user['habr_account']:
        await message.answer(f"Вы подписаны на рассылки как <b>{user['status']}</b>", reply_markup=choice_for_profile)
    else:
        await message.answer(f"Можно подписаться на рассылки по любому профилю Хабра", reply_markup=choice_for_all)


# логика выбора действия (нажатие соотв кнопок)
@dp.callback_query_handler(state=ChangeProfile.Subscribe_State)  # text - это не text из назв кнопки а из callback_data
async def change_profile(call: CallbackQuery, state: FSMContext):
    await state.finish()
    if call.data == 'profile_posts_add':
        await add_profile(call)
    elif call.data == 'cancel_allez':
        await cancel_profile(call)
    elif call.data == 'cancel':
        await cancel(call)
    else:
        print('???????')

# нет, чтобы просто нажать кнопку - теестер, точняк!
@dp.message_handler(state=ChangeProfile.Subscribe_State)
async def no_message(message: Message):
    await message.answer("Не надо ничего писать, выберите действие и нажмите соотв. кнопку ")


# @dp.callback_query_handler(choise_callback.filter(post_type_choise='profile_posts_add'))
async def add_profile(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await ChangeProfile.EditProfile.set()
    await call.message.answer("Введите имя действующего аккаунта Хабра", reply_markup=choice_cancel)


# @dp.callback_query_handler(choise_callback.filter(post_type_choise='cancel_allez'))
async def cancel_profile(call: CallbackQuery):
    await ChangeProfile.Unsubscribe_Question.set()
    await call.message.edit_reply_markup()
    await call.message.answer("Желаете отписаться от аккаунта Хабра для этото бота?", reply_markup=cancel_quest)


# вместо подтв пытается что-то писать, козел
@dp.message_handler(state=ChangeProfile.Unsubscribe_Question)
async def post_unknown(message: Message):
    await message.answer("Не надо ничего писать, прдтвердите или отмените действия по подписке ")


# отказ от подписки да/нет
@dp.callback_query_handler(state=ChangeProfile.Unsubscribe_Question)
async def unsubscribe_profile(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    if call.data == 'no_cancel':
        await call.message.answer(f"{call.from_user['first_name']}, ваш статус подписки на Хабре остался прежним")
        return
    await db.update_user_status('new_user', call.message.chat.id)
    await db.delete_user_hubs(call.message.chat.id)

    chat = await bot.get_chat(channels[0])
    invite_link = await chat.export_invite_link()
    channels_format = f" <a href='{invite_link}'>Канала</a>"

    await call.message.answer(f"{call.from_user['first_name']}, рассылка по профилю вам больше приходить не будет")
    await call.message.answer(f"От {channels_format} отпишитесь прямо в нем")

# реакция на ввод имени профиля хабра
@dp.message_handler(state=ChangeProfile.EditProfile)
async def enter_message(message: Message, state: FSMContext, user: dict):
    template = r'[a-zA-Z0-9_-]+'
    if re.fullmatch(template, message.text) is None:
        await message.answer(f"<b>{user['name']}</b>, вы пытаетесь ввести недопустимые в имени профиля символы;\n"
                             f"попробуйте еще; кнопка отмена (выше) - отказ от изменений")
        return
    ut = get_user_tags(message.text)
    if ut[0] != '-1':
        await state.finish()
        await db.update_user_status(message.text, message.chat.id, False, True)
        await db.delete_user_hubs(message.chat.id)
        await db.add_user_hubs_by_name(message.chat.id, ut)
        await message.answer(f"<b>{user['name']}</b>Теперь вы будете получать посты по хабам профиля "
                             f"<b>{message.text}</b>")
    else:  # такого профиля нет
        await message.answer(f"<b>{user['name']}</b>, {ut[1]}!\n"
                             f"попробуйте еще; кнопка отмена (выше) - отказ от изменений")


@dp.callback_query_handler(state=ChangeProfile.EditProfile)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Вы ничего не поменяли, ваш статус подписки на Хабре остался прежним")


# отмена изменений профиля
# @dp.callback_query_handler(
#     choise_callback.filter(post_type_choise='cancel'))  # text - это не text из назв кнопки а из callback_data
async def cancel(call: CallbackQuery):
    await call.answer('Отмена! Параметры подписки остались прежними', show_alert=True)
    await call.message.edit_reply_markup()
