# чтобы работало в  middleware in __init__ обязятельно д б setup !
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from utils.db_api.sqllite import Database
from utils.db_api.User import User


# All methods on the middle always must be coroutines and name starts with "on_" like "on_process_message
class GetDbUser(BaseMiddleware):
    db = Database()
    all_users_list = db.select_all_users()

    async def on_process_message(self, message: types.Message, data: dict):  # data - данные, кот летят в хендлер
        one_us = self.db.select_user(name=message.from_user.full_name)
        if one_us is None:
            self.db.add_user(message.from_user.id, message.from_user.full_name)
            data['user'] = User(id_user=message.from_user.id, name=message.from_user.full_name, status='new_user')
        else:
            data['user'] = {'id_user': message.from_user.id, 'name': message.from_user.full_name, 'status': 'from_base'}

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):

        # data['user'] = {'id': 345, 'name': cq.from_user.full_name}
        one_us = self.db.select_user(name=cq.from_user.full_name)
