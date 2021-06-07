from typing import Union, Any
import asyncio
import asyncpg
from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self) -> None:
        self.pool: Union[Pool, None] = None
        # self.pool = None
        pass

    async def create(self):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.IP,
            database=config.DATABASE
        )
        self.pool = pool
        return pool

    async def select_all_users(self):
        # self.pool = await self.create()
        # Замки обычно используются для синхронизации доступа к общим ресурсам.Для каждого источника создается объект
        # Когда вам нужно получить доступ к ресурсу, вызовите acquire для того, чтобы поставить блок
        async with self.pool.acquire() as con:
            async with con.transaction():
                rez = await con.fetch('SELECT * FROM Usersn')
        print(rez)

    async def add_user(self, id: int, name: str, email: str = None):
        sql = "INSERT INTO Usersn(id, name, email, new_user, channel, habr_account) VALUES ($1, $2, $3, TRUE , FALSE , FALSE )"
        try:
            await self.pool.execute(sql, id, name, email)
        except asyncpg.exceptions.UniqueViolationError:
            pass

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([f'{item} = ${num}' for num, item in enumerate(parameters, start=1)])
        return sql, tuple(parameters.values())

    async def select_user(self, **kwargs):
        sql = "SELECT id, name, email, status, new_user, channel, habr_account FROM Usersn WHERE "
        sql, params = self.format_args(sql, kwargs)
        print(sql)
        print(*params)
        return await self.pool.fetchrow(sql, *params)

    @staticmethod
    def format_args_status(sql, parameters: dict):
        sql += ', '.join([f'{item} = ${num}' for num, item in enumerate(parameters, start=1)])
        return sql, tuple(parameters.values())

    async def update_user_status2(self, id, **kwargs):
        sql = 'UPDATE Usersn SET '
        sql, params = self.format_args_status(sql, kwargs)
        sql += f" WHERE id = {id}"
        # print(sql)
        # print(params)
        return  # await self.pool.execute(sql, *params)

    async def update_user_status(self, status, id):
        sql = 'UPDATE Usersn SET status = $1 WHERE id = $2'
        return await self.pool.execute(sql, status, id)

    async def delete_user_hubs(self, id):
        sql = 'DELETE FROM Users_hubs WHERE id_user = $1'
        return await self.pool.execute(sql, id)

    # у user изменились хабыб пишем в базу id_user - id_hub->(из hubs_list)
    async def add_user_hubs(self, id: int, hubs_list: list):
        sql = "INSERT INTO Users_hubs(id_user, id_hub) VALUES "
        sql += ', '.join([f'({id}, {num})' for num in hubs_list])
        await self.pool.execute(sql)

    async def add_user_hubs_by_name(self, id: int, hubs_list: list):
        sql = "INSERT INTO Users_hubs(id_user, id_hub) "
        sql += f"(SELECT {id}, id FROM hubs WHERE hub_name IN ("
        sql += ' , '.join([f'\'{num}\'' for num in hubs_list])
        sql += ")"
        sql += ")"
        # print(sql)
        await self.pool.execute(sql)

    # получить list(id - hub_name) из списка
    async def get_post_hubs(self, hubs_names: list):
        sql = "SELECT * FROM hubs WHERE hub_name IN ("
        sql += ' , '.join([f'\'{num}\'' for num in hubs_names])
        sql += ")"
        return await self.pool.fetch(sql)

    # получить спис подходящих юзеров для рассылки нового поста - внутри селект список id тегов поста
    async def get_users_for_post(self, hubs_names: list):
        sql = "SELECT DISTINCT id_user FROM users_hubs WHERE id_hub IN ("
        sql += "SELECT id FROM hubs WHERE hub_name IN ("
        sql += ' , '.join([f"'{num}'" for num in hubs_names])
        sql += ")"
        sql += ")"
        print(sql)
        return await self.pool.fetch(sql)

    async def subscr_all_posts(self, id):
        async with self.pool.acquire() as con:
            # async with con.transaction():
            await self.update_user_status('all_posts', id)
            await self.delete_user_hubs(id)
            await self.add_user_hubs(id, [999])


    # async def subscr_all_posts(self, id):
    #     tr = self.pool.acquire().transaction()
    #     await tr.start()
    #     try:
    #         await self.update_user_status('all_posts', id)
    #         await self.delete_user_hubs(id)
    #         await self.add_user_hubs(id, [999])
    #     except:
    #         await tr.rollback()
    #         raise
    #     else:
    #         await tr.commit()
    #

# await tr.start()
# try:
#     ...
# except:
#     await tr.rollback()
#     raise
# else:
#     await tr.commit()



# db = Database()
# # db.create()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(db.select_all_users())
# pass
