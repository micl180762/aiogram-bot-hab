from aiogram.dispatcher.filters.state import StatesGroup, State


# состояния отправки сообщения в канал - написать и подтвердить
class ChangeProfile(StatesGroup):
    Subscribe_State = State()
    EditProfile = State()
    Confirm = State()
    Unsubscribe_Question = State()
    ChangeProfile_State = State()
