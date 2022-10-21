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
    requests.get(f"https://api.telegram.org/bot1226847744:AAHLU7TXkxe13r0LEwjeQ1dFUVk0kMB56Os/deleteMessage?chat_id=394143446&message_id={id}")

def get_status(id):
    return session.method('users.get', values={'user_ids':id, 'fields':'online'})

def pinned_msg(id):
    requests.get(f"https://api.telegram.org/bot1226847744:AAHLU7TXkxe13r0LEwjeQ1dFUVk0kMB56Os/pinChatMessage?chat_id=394143446&message_id={id}")

def send_msg(message):
    req = requests.post("https://api.telegram.org/bot1226847744:AAHLU7TXkxe13r0LEwjeQ1dFUVk0kMB56Os/sendMessage?chat_id=394143446"+f"&text={message}")
    return req.json()['result']['message_id']

average_time = [2, 4]
mass = []
while True:
    while True:
        try:
            status = get_status(aim)
            if status[0]['online'] == 1:
                if temp_stat == 'offline':
                    deleted_id = send_msg('Вошла в сеть')
                    temp_stat = 'online'

                print('Online')
                hours = datetime.now(offset).hour
                minutes = datetime.now(offset).minute
                mass.append([hours, minutes])
                sleep(30)
            else:
                if len(mass) == 0:
                    print('Offline')
                    if datetime.now(offset).hour == 4 and flag == 0 and len(average_time)!=0:
                        pinned_id = send_msg(f"Общее время в сети за {datetime.now(timezone(timedelta(hours=-2))).date()} = {sum(average_time)} mins\nСреднее время одного сеанса = {sum(average_time)//len(average_time)} mins")
                        pinned_msg(pinned_id)
                        delete_msg(pinned_id+1)
                        average_time.clear()
                        flag = 1

                    if datetime.now(offset).hour == 5 and flag == 1:
                        flag = 0

                    sleep(30)
                else:
                    temp_stat = 'offline'
                    if mass[-1][0] == 0 and mass[0][0] == 23:
                        mass[-1][0] = 24
                    if mass[-1][0] == 0 and mass[0][0] == 22:
                        mass[-1][0] = 24
                    if mass[-1][0] == 1 and mass[0][0] == 23:
                        mass[-1][0] = 25
                    if mass[-1][0] == 1 and mass[0][0] == 22:
                        mass[-1][0] = 25
                    if mass[-1][0] == 2 and mass[0][0] == 23:
                        mass[-1][0] = 26
                    if mass[-1][0] == 2 and mass[0][0] == 22:
                        mass[-1][0] = 26

                    sess = ((mass[-1][0] * 60 + mass[-1][1]) -
                            (mass[0][0] * 60 + mass[0][1])) - 5

                    if sess < 0:
                        sess = 0

                    if sess != 0: average_time.append(sess)

                    msg = f'Вход - {mass[0][0]}:{mass[0][1]}\nВыход - {mass[-1][0]}:{mass[-1][1]}\nПродолжительность - {sess} минут(ы)'
                    delete_msg(deleted_id)
                    send_msg(msg)

                    print(f'{datetime.now().date()} - Запись завершена')

                    mass.clear()
                    sleep(30)

        except Exception as err:
            print(f'Problem: {err}')
# 287286283 dasha
# 472177450 dima
# 52637246 nata