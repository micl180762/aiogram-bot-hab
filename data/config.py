from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
admins = env.list("ADMINS")  # Тут у нас будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
PGUSER=env.str("PGUSER")
PGPASSWORD=env.str("PGPASSWORD")
DATABASE = env.str('DATABASE')
channels = env.list("CHANNELS")

# with open('./data/users.txt', 'r') as f:  # список юзеров
#     users_list = f.read().splitlines()
#
# users_dict = dict()
# for user in users_list:
#     user_list = user.split(',')
#     users_dict[user_list[0]] = user_list[1]
