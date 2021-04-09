from aiogram import types
from loader import dp, db
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command('subscr'))
async def email_create(message: types.Message, state: FSMContext):
    await message.answer("Выберите действие:")
    await state.set_state('subscr')


@dp.message_handler(state='subscr')
async def enter_email(message: types.Message, state: FSMContext):
    all = await db.select_all_users()
    print(all)
    await state.finish()
    await message.answer(message.text)
