import requests
import re
import configparser


def get_updates_json(request):
    try:
        response = requests.get(request)
    except requests.exceptions.RequestException as e:
        return None
    return response.json()


def last_update(data):
    results = data['result']
    total_updates = len(results) - 1
    if total_updates == -1:
        return None
    return results[total_updates]


def get_chat_id(update):
    chat_id = update['message']['chat']['id']
    return chat_id


def send_new_post_name(url, chat, text):
    params = {'chat_id': chat, 'text': text}
    response = requests.post(url, data=params)
    return response


def new_posts_note(new_posts_list=[]):
    tlg_set = get_ini_tlg()
    url_bot = 'https://api.telegram.org/bot' + tlg_set['token']
    # data_update_json = get_updates_json(url_bot + '/getUpdates')
    # if data_update_json is None:
    #     print("Telegram Connection aborted.TimeoutError " + datetime.now().strftime('%d-%b %H:%M'))
    #     return
    # results = data_update_json['result']
    # # бот подвисает каждые 24 часа, если ему ничего не писать, однако, id чата остается тем же
    # if len(results) == 0:
    #     AlarmNotification.alarm_notification("Telegram bot is Off " + datetime.now().strftime('%d-%b %H:%M'))
    chat_id = tlg_set['chat_id']
    # else:
    #     chat_id = get_chat_id(last_update(data_update_json))
    #     if str(chat_id) != tlg_set['chat_id']:
    #         AlarmNotification.alarm_notification("chat ID was changed" + datetime.now().strftime('%d-%b %H:%M'))
    #         write_ini_chat_id(chat_id)
    # for post in new_posts_list:
    send_new_post_name(url_bot + '/sendMessage', chat_id, 'post-post')


def tlg_notification(all_posts):
    post_names_list = []
    for post in all_posts:
        post_names_list.append(post['post_link'])
    new_posts_note(post_names_list)


# нехорошо здесь работать с ини, но не хочется плодить сущности
# проверка токена - если несоответствие шаблону - None
def get_ini_tlg():
    config = configparser.ConfigParser()
    config.read("private_set.ini")
    token = config['Tlg']['token']
    template = r'[0-9]{8,12}[:-][a-zA-Z0-9_-]{35,36}'
    if re.fullmatch(template, token) is not None:
        return config._sections['Tlg']
    else:
        return None


def write_ini_chat_id(chat_id):
    config = configparser.ConfigParser()
    config.read("private_set.ini")
    config['Tlg']['chat_id'] = str(chat_id)
    with open('private_set.ini', 'w') as conf:
        config.write(conf)
