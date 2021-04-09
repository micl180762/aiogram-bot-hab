from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
# from .database import GetDbUser
from .db_postgres import GetDbUserPg

if __name__ == "middlewares":
     dp.middleware.setup(ThrottlingMiddleware())
     dp.middleware.setup(GetDbUserPg())

