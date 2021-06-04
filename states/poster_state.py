from aiogram.dispatcher.filters.state import StatesGroup, State


# состояния отправки сообщения в канал - написать и подтвердить
class NewPost(StatesGroup):
    EnterMessage = State()
    Confirm = State()