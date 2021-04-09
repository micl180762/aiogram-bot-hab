from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from utils.db_api.postgresql import Database
from data import config
from utils.db_api.postgresql2 import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()  # In-memory based states storage can RedisStorage
dp = Dispatcher(bot, storage=storage)
db = Database()
