from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer(f"Назначение сообщения:\n"
                         f"{message.text} \nне распознано логикой бота"
                         )

# Эхо хендлер, куда летят ВСЕ сообщения с состоянием для кто нет спец хендлера
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    state = await state.get_state()
    print(state)  # будем логировать
    await message.answer(f"Логика бота не распознала назначение "
                         f"вашего сообщения:\n"
                         f"<code>{message}</code>")
