import requests
import bs4
import telegramBot
import time
starttime = time.time()


# def get_all():
#     telegramBot.new_posts_note()
#     # print(all_us)
#     pass
#
# while True:
#     get_all()
#     time.sleep(10.0 - ((time.time() - starttime) % 10.0))

hubs_list = ['c','java','python']
id = 15
sql = "INSERT INTO Users_hubs(id_user, id_hub) "
sql += f"(SELECT {id}, id FROM hubs WHERE hub_name IN ("
sql += ' , '.join([f'\'{num}\'' for num in hubs_list])
sql += ")"
sql += ")"

print(sql)

