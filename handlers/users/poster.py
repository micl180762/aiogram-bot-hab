from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from data.config import admins, channels
from keyboards.inline.manage_post import confirmation_keyboard, post_callback
from loader import dp, bot

# подтвердить/отказаться от сообщения админу
from states.poster_state import NewPost


@dp.message_handler(Command("personal_question"))
async def create_message(message: Message):
    await message.answer('Введите текст сообщения')
    await NewPost.EnterMessage.set()


@dp.message_handler(state=NewPost.EnterMessage)
async def enter_message(message: Message, state: FSMContext):
    # сохраняем текст с разметкой и ссылкой на автора
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer('Отправить сообщение?', reply_markup=confirmation_keyboard)
    await NewPost.next()  # Confirm


@dp.callback_query_handler(post_callback.filter(action="post"), state=NewPost.Confirm)
async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")

    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Отправлено!")
    # Это уходит админу для подтв/отказа
    await state.update_data(autor=mention)
    await bot.send_message(chat_id=admins[0], text=f"User {mention} sent message:")
    # await bot.send_message(chat_id=admins[0], text=text, parse_mode="HTML",
    #                        reply_markup=confirmation_keyboard, disable_web_page_preview=True)
    await bot.send_message(chat_id=admins[0], text=text, parse_mode="HTML",
                           disable_web_page_preview=True)


@dp.callback_query_handler(post_callback.filter(action="cancel"), state=NewPost.Confirm)
async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Вы отменили отправку сообщения")


# вместо подтв пытается что-то писать, козел
@dp.message_handler(state=NewPost.Confirm)
async def post_unknown(message: Message):
    await message.answer("Finish play the fool, push button! :P ")


# admin выбрал!
@dp.callback_query_handler(post_callback.filter(action="post"), user_id=admins)
async def approve_post(call: CallbackQuery):
    await call.answer("You approve this post", show_alert=True)
    target_channel = channels[0]
    # in message попадет измененное сообщение
    message = await call.message.edit_reply_markup()
    # пересылаем/копируем  сообщение, пометки forwarded не будет
    await message.send_copy(chat_id=target_channel)

# admin отклонил
@dp.callback_query_handler(post_callback.filter(action="cancel"), user_id=admins)
async def decline_post(call: CallbackQuery, user: dict, state: FSMContext):
    await call.answer("You decline this post", show_alert=True)
    print(user['id'])
    await call.message.edit_reply_markup()
    async with state.proxy() as data:
        mention = data.get("autor")
    print(mention)
