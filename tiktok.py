import time
import logging
import requests
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

def download_tiktok(link, filename):
    try:
        #куки файлы
        cookies = {
            'cf_clearance': 'ecB.1i0xqpG0WZvIWeewAB8LugZwyh_Bf.ImrjIPicY-1733458177-1.2.1.1-ZALAc2hsAJzlsp7wBQvUpf_KFWmQeK6pI6klZyZItXrlOA8VAdpZ8sSb2gb1vNwblzIGPrJeICjS0ELUf36mpQojtZVFSxptLzC7bqN.jlNVcNEYEI5Z_M2F4ZuUh6wu5soNUv0mbNhZBljxKXD.SvObEtQXkmXP9KY8BoLrjNsAe1.AnVXc7mjtflVQvrTPQHjWQ0Y.VBgKbIjYMjfwYV8raoaVMqMQwUnl9npEcyyqQ1kAihsE5hXG2aJLdZEklK_RR4Whw6xtncQHuPjLtVVJLVoS6Q.lKyzS9GndClpUA5r3v781It15mpboTJvEcswQz6G3vHSIqK2.Tiwd6jdgMuFugUqZQ_2EO18qRw1jaUU8NFCDv9uLGY2Polix8UbeCwMkQISqza0b3KH9fl2Q8fiS4tEea0A0.4Dw8yn1Ey8hkKub0tkPGzZvp3.M',
            '_ga': 'GA1.1.594216057.1733458182',
            '_ga_ZSF3D6YSLC': 'GS1.1.1733458182.1.1.1733458305.51.0.0',
        }
        #настройки заголовков
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,az;q=0.6,xh;q=0.5',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'hx-current-url': 'https://ssstik.io/',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'priority': 'u=1, i',
            'referer': 'https://ssstik.io/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-arch': '"x86"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"131.0.6778.86"',
            'sec-ch-ua-full-version-list': '"Google Chrome";v="131.0.6778.86", "Chromium";v="131.0.6778.86", "Not_A Brand";v="24.0.0.0"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"10.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        }

        params = {
            'url': 'dl',
        }
        #передаваемая информация
        data = {
            'id': link,
            'locale': 'en',
            'tt': 'NHNIb0E3',
        }


        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')

        file = urlopen(soup.a['href'])
        with open(f'cache/tiktok/{filename}.mp4', 'wb') as output:
            data = file.read()
            output.write(data)

    except AttributeError as e:
        # logging.error('таймаут')
        # raise e
        ...

# тесты
if __name__ == '__main__':
    url = 'https://www.tiktok.com/t/ZTYKD3pQ1/'
    download_tiktok(url, 'r')
