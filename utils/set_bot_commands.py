from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('channels', 'Список каналов на подписку'),
        types.BotCommand('create_post', 'Предложить пост в канале')
    ])
