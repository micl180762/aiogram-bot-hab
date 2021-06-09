from aiogram import executor
import aioschedule
import asyncio
from data.config import channels
# import utils.habr.HabrParser as hp
from utils.habr.send_new_posts import send_all

from loader import dp, db, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from itertools import groupby

# habr_parser = hp.HabrParser()


async def noon_print():
    # await bot.send_message(channels[0], 'mim-dialog!')
    # liall = habr_parser.new_posts_in_channel()
    # li = [k for k, _ in groupby(sorted(liall, key=lambda x: liall.index(x)))]
    # for post in li:
    #     await bot.send_message(channels[0], post)
    #     await asyncio.sleep(2)
    await send_all()
    # print(channels[0])


async def scheduler():
    # await bot.send_message(channels[0], '!!start sending posts!!')
    aioschedule.every(15).minutes.do(noon_print)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    await db.create()
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
