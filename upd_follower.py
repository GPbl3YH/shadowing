import requests
from datetime import datetime, timezone, timedelta
from time import sleep
import vk_api

flag = 0
aim = 'naatik'
temp_stat = 'offline'
offset = timezone(timedelta(hours=3))
session = vk_api.vk_api.VkApi(login='79150470373', password='Prytkov2002', token='c047b419c047b419c047b41999c03a1613cc047c047b419a2afe35905e31ee656da698e', auth_handler=None, captcha_handler=None, config_filename='vk_config.v2.json', api_version='5.81', app_id=8233482, scope=140492255, client_secret='7lLdyc7WoGU7OGu7Dz6p')


def delete_msg(id):
    requests.get(f"https://api.telegram.org/bot5505845559:AAFeuHYprGavV1ELhE-FO8jU6Yag5gFCfsE/deleteMessage?chat_id=394143446&message_id={id}")

def get_status(id):
    return session.method('users.get', values={'user_ids':id, 'fields':'online'})

def pinned_msg(id):
    requests.get(f"https://api.telegram.org/bot5505845559:AAFeuHYprGavV1ELhE-FO8jU6Yag5gFCfsE/pinChatMessage?chat_id=394143446&message_id={id}")

def send_msg(message):
    req = requests.post("https://api.telegram.org/bot5505845559:AAFeuHYprGavV1ELhE-FO8jU6Yag5gFCfsE/sendMessage?chat_id=394143446"+f"&text={message}")
    return req.json()['result']['message_id']

def last_seen(id):
    return session.method('users.get', values={'user_ids':id, 'fields':'last_seen'})[0]['last_seen']['time']

entrance_time = 0
last_time = last_seen(aim)
msg_counter = 0
msg_counter_day = 1
average_time = []
tries = 0
while True:
    while True:
        try:
            status = last_seen(aim)
            if status > last_time and temp_stat == 'offline':
                entrance_time = status
                deleted_id = send_msg('Наташа вошла в сеть')
                temp_stat = 'online'
                print('Entrance')
                last_time = status
                sleep(1)
            if status > last_time and temp_stat == 'online':
                msg_counter += 1
                print(f'Natas message {msg_counter}')
                last_time = status
                tries = 0
                sleep(1)

            elif status == last_time:
                if temp_stat == 'offline':
                    if datetime.now(offset).hour == 3 and flag == 0 and len(average_time)!=0:
                        pinned_id = send_msg(f"Общее время в сети за {datetime.now(timezone(timedelta(hours=-2))).date()} = {sum(average_time)//60}:{sum(average_time)%60} mins\nСреднее время одного сеанса = {(sum(average_time)//len(average_time))//60}:{(sum(average_time)//len(average_time))%60} mins\n~Количество сообщений - {msg_counter_day}")
                        pinned_msg(pinned_id)
                        delete_msg(pinned_id+1)
                        msg_counter_day = 0
                        average_time.clear()
                        flag = 1

                    if datetime.now(offset).hour == 4 and flag == 1:
                        flag = 0
                    sleep(1)

                elif temp_stat == 'online' and tries == 120:
                    temp_stat = 'offline'
                    sess = last_time - entrance_time
                    msg = f'Вход - {datetime.utcfromtimestamp(entrance_time+10800).strftime("%H:%M:%S")}\nВыход - {datetime.utcfromtimestamp(last_time+10800).strftime("%H:%M:%S")}\nПродолжительность - {sess//60} минут(ы) {sess%60} секунд(ы)\n~Количество сообщений - {msg_counter}'
                    delete_msg(deleted_id)
                    send_msg(msg)

                    print(f'{datetime.now().date()} - Запись завершена')

                    tries = 0
                    if sess > 0: average_time.append(sess)
                    msg_counter_day += msg_counter
                    msg_counter = 0
                    sleep(1)
                
                elif temp_stat == 'online' and tries < 120:
                    tries += 1
                    print(f'Nata {tries}')
                    sleep(1)
                
        except Exception as err:
            print(f'Problem: {err}')
# 287286283 dasha
# 472177450 dima
# 52637246 nata


