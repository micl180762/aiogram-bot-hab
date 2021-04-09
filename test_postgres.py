import asyncpg
import asyncio
from data import config


async def conne():
    usera = config.PGUSER
    return await asyncpg.connect(user=config.PGUSER, password=config.PGPASSWORD, host=config.IP,
                                 database=config.DATABASE)


async def run():
    con = \
        await asyncpg.connect(user=config.PGUSER, password=config.PGPASSWORD, host=config.IP, database=config.DATABASE)
    types = await con.fetch('SELECT * FROM usersn')
    await con.execute('INSERT INTO usersn (id, name, email) VALUES ($1, $2, $3)', 4, "sveta", "s@s")
    print(types)


async def run_one(idu):
    con = await conne()
    # await asyncpg.connect(user=config.PGUSER, password=config.PGPASSWORD, host=config.IP, database=config.DATABASE)
    types = await con.fetchrow('SELECT * FROM Users WHERE id = ' + str(idu))

    print(types)


async def run_all():
    con = await conne()
    # await asyncpg.connect(user=config.PGUSER, password=config.PGPASSWORD, host=config.IP, database=config.DATABASE)
    # types = await con.fetch("SELECT * FROM information_schema.tables WHERE table_schema = 'public'")
    types = await con.fetch("SELECT * FROM Usersn")

    print(types)

async def create():
    con = await conne()
    sql = """
    create table Usersn
    (
        id     integer      not null
               primary key,
        name   varchar(100) not null,
        email  varchar(100),
        status varchar(40) default 'new_user'::character varying
    );
    """
    await con.execute(sql)




loop = asyncio.get_event_loop()
loop.run_until_complete(run())


# pool = await asyncpg.create_pool(
#     user=config.PGUSER,
#     password=config.PGPASSWORD,
#     host=config.IP,
#     database=config.DATABASE
# )
