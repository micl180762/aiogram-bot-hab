import asyncio

from utils.db_api.postgresql import Database

async def setup_psql():
    await db.create()


loop = asyncio.get_event_loop()
db = Database()


loop.run_until_complete(db.select_all_users())