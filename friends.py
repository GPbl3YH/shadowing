import requests
import vk_api
from time import sleep
from datetime import datetime
import  html2text
import os

base = []
time = []

while True:
    try:
        url = requests.get('https://vk.com/id')
        text = html2text.HTML2Text().handle(url.text)
        if len(text[text.find('заходила'):text.find('назад')]) == 0:
            print('В сети')
            session = vk_api.VkApi(token='')
            data = session.method('friends.get', {"user_id":, "order":"random", "fields":("online", "sex")})
            for x in data['items']:
                if x['sex'] == 2 and x['online'] == True:
                    base.append(f"{x['first_name']} {x['last_name']} https://vk.com/id{x['id']}")
                    time.append([datetime.now().hour, datetime.now().minute, datetime.now().second])
            sleep(1)
            continue
        if len(base) > 0:
            base = sorted(list(set(base)))
            file = open('./DataBase/friends.txt', 'a', encoding='utf-8-sig')
            file.write(f'\n{"-"*50}')
            file.write(f'\nC {time[0][0]}:{time[0][1]}:{time[0][2]}-{time[-1][0]}:{time[-1][1]}:{time[-1][2]} были:')
            for x in base: file.write(f'\n\t{x}')
            file.close()
            base.clear()
            time.clear()
            os.system('python stats.py')
            sleep(5)
        print('Сейчас не в сети')
        sleep(5)
    except:
        sleep(5)
        continue





#7c6aae8e5cb13707ab
#{"access_token":"a59b952a357c5e94aa2002b5fd6d84ea45eec19bd3a4b544e2fd8c0e8f3c598139018798b51a832d35221",
#"expires_in":0,
#"user_id":165086485}
