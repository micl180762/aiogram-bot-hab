from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from loader import db
from utils.db_api.User import User
from utils.misc.states import states


class GetDbUserPg(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):  # data - данные, кот летят в хендлер
        one_us = await db.select_user(id=int(message.chat.id))
        if one_us is None:
            await db.add_user(int(message.chat.id), message.chat.full_name)
            data['user'] = \
                {'id_user': message.chat.id,
                 'name': message.chat.full_name,
                 'status': 'new_user',
                 'status_ru': 'Новый подписчик'}
        else:
            data['user'] = \
                {'id_user': one_us['id'], 'name': one_us['name'],
                 'status': one_us['status'],
                 'status_ru': states.get(one_us['status'], f'Профиль - {one_us["status"]}')}

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):

        # data['user'] = {'id': 345, 'name': cq.from_user.full_name}
        # one_us = await db.select_user(name=cq.from_user.full_name)
        # print(F'one_us={one_us}')
        pass

# select usersn.id, usersn.status, user_states.state FROM usersn LEFT JOIN user_states ON usersn.id = user_states.id WHERE usersn.id = 949072754