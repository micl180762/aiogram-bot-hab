from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


# бот проверяет только сообщение которое переслано именно из канала
# как наследник BoundFilter в хендлере возвращает сразу значение check
class IsForvarded(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        if message.forward_from_chat:
            return message.forward_from_chat.type == types.ChatType.CHANNEL
        return False
