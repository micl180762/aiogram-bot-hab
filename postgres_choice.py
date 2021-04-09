import asyncio

import asyncpg
import time
from data import config


async def bench_asyncpg_pool():
    # pool = await asyncpg.create_pool(user='postgres', host='127.0.0.1')
    pool = await asyncpg.create_pool(
        user=config.PGUSER,
        password=config.PGPASSWORD,
        host=config.IP,
        database=config.DATABASE
    )
    power = 2
    start = time.monotonic()
    for i in range(1, 3):
        async with pool.acquire() as con:
            rez = await con.fetch('SELECT * FROM Users')
            print(rez)

    await pool.close()
    end = time.monotonic()
    print(end - start)


loop = asyncio.get_event_loop()
loop.run_until_complete(bench_asyncpg_pool())