import asyncio
import utils.habr.HabrParser as hp
from itertools import groupby
from data.config import channels
from loader import dp, db, bot


habr_parser = hp.HabrParser()


async def send_posts_channel(li):
    for post in li:
        await bot.send_message(channels[0], post[0])
        await asyncio.sleep(2)


async def send_posts_users(li):
    for post in li:
        list_suitable_users_id = await db.get_users_for_post(post[1])
        print(f'list_suitable_users_id = {list_suitable_users_id}')
        for user_id in list_suitable_users_id:
            # print(f'user_id={user_id[0]}')
            await bot.send_message(user_id[0], post[0])
            await asyncio.sleep(2)


async def send_all():
    liall = habr_parser.new_posts_in_channel() # [link1,[hub1, hub2,...,hubN],.., linkM,[hub1, hub2,...,hubN]]
    li = [k for k, _ in groupby(sorted(liall, key=lambda x: liall.index(x)))]
#    await send_posts_channel(li)
    await send_posts_users(li)

