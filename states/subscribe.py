from aiogram.dispatcher.filters.state import StatesGroup, State


class Subscribe(StatesGroup):
    Set_subscrible = State()
    Unsubscribe = State()
