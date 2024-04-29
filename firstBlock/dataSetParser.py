import random
import re
import time

import requests
from bs4 import BeautifulSoup
import json
rooms_variants = [[1,4,9],[2,3]]
def create_request(underground, page,rooms_v):
    cookies = {
        '_CIAN_GK': '61ecfcce-0826-48de-a9ba-9673353f920d',
        '__cf_bm': '5__lKNMqiSznjEB__6zMungkYdldyhlj_t3aqSXVhaE-1714375492-1.0.1.1-uGf0IUHXzZMM6I0It1v1eQ4UnsjYUUyUyRszR7P6.pGI6u5E5H9TVeXlsk3nDxITq1XEKdRpwB2KLXcmoGIIDw',
        '_gcl_au': '1.1.905873749.1714375493',
        'tmr_lvid': '33574daf6ecaa9685ff8ce14949b1744',
        'tmr_lvidTS': '1714375493292',
        'login_mro_popup': '1',
        'sopr_utm': '%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D',
        'sopr_session': 'e49e4ce3e6de4012',
        'uxfb_usertype': 'searcher',
        'uxs_uid': '9308d580-05f9-11ef-a5e5-4b7946a5175e',
        '_gid': 'GA1.2.860519583.1714375494',
        '_ym_uid': '1714375495103905793',
        '_ym_d': '1714375495',
        '_ym_visorc': 'b',
        '_ym_isad': '2',
        'afUserId': 'ea563913-67bc-4166-82d5-5b8de5802cc5-p',
        'AF_SYNC': '1714375495992',
        'session_region_id': '1',
        'session_main_town_region_id': '1',
        '_ga_3369S417EL': 'GS1.1.1714375494.1.1.1714375508.46.0.0',
        '_ga': 'GA1.2.444595236.1714375494',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        # 'cookie': '_CIAN_GK=61ecfcce-0826-48de-a9ba-9673353f920d; __cf_bm=5__lKNMqiSznjEB__6zMungkYdldyhlj_t3aqSXVhaE-1714375492-1.0.1.1-uGf0IUHXzZMM6I0It1v1eQ4UnsjYUUyUyRszR7P6.pGI6u5E5H9TVeXlsk3nDxITq1XEKdRpwB2KLXcmoGIIDw; _gcl_au=1.1.905873749.1714375493; tmr_lvid=33574daf6ecaa9685ff8ce14949b1744; tmr_lvidTS=1714375493292; login_mro_popup=1; sopr_utm=%7B%22utm_source%22%3A+%22google%22%2C+%22utm_medium%22%3A+%22organic%22%7D; sopr_session=e49e4ce3e6de4012; uxfb_usertype=searcher; uxs_uid=9308d580-05f9-11ef-a5e5-4b7946a5175e; _gid=GA1.2.860519583.1714375494; _ym_uid=1714375495103905793; _ym_d=1714375495; _ym_visorc=b; _ym_isad=2; afUserId=ea563913-67bc-4166-82d5-5b8de5802cc5-p; AF_SYNC=1714375495992; session_region_id=1; session_main_town_region_id=1; _ga_3369S417EL=GS1.1.1714375494.1.1.1714375508.46.0.0; _ga=GA1.2.444595236.1714375494',
        'origin': 'https://www.cian.ru',
        'priority': 'u=1, i',
        'referer': 'https://www.cian.ru/',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }
    json_data = {
        'jsonQuery': {
            '_type': 'flatsale',
            'engine_version': {
                'type': 'term',
                'value': 2,
            },
            'geo': {
                'type': 'geo',
                'value': [
                    {
                        'type': 'underground',
                        'id': underground,
                    },
                ],
            },
            'region': {
                'type': 'terms',
                'value': [
                    1,
                ],
            },
            'page': {
                'type': 'term',
                'value': page,
            },
            'room': {
                'type': 'terms',
                'value': rooms_variants[rooms_v],
            },
        },
    }

    response = requests.post(
        'https://api.cian.ru/search-offers/v2/search-offers-desktop/',
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response

def parsing(min_underground, max_undergroud):
    i = min_underground
    while(i<max_undergroud):
        for k in range(0,2):
            j = 1;
            while (j<4):
                print(f"страница {j}, метро {i}, конфиг комнат {k}")
                response = create_request(i,j,k)
                print(response.status_code)
                if (response.status_code == 429):
                    print('Ошибка! Ждем')
                    time.sleep(random.randint(7,10))
                    continue
                js = json.loads(response.text)
                js = js['data']["offersSerialized"]
                if (len(js)==0):
                    if (k == 1):
                        i+=1
                        print("все объявления этого метро запаршены")
                    print("переключаем К")
                    break
                for n in js:
                    try:
                        params = []
                        params.append(n['geo']['address'][3]['name'])  # метро
                        params.append(n['geo']['coordinates']['lng'])  # корды
                        params.append(n['geo']['coordinates']['lat'])
                        params.append(n['building']['floorsCount'])  # этажность
                        params.append(n['building']['materialType'])  # тип дома
                        params.append(n['building']['buildYear'])  # год постройки
                        params.append(n['kitchenArea'])  # площадь кухни
                        params.append(n['roomsCount'])  # количество комнат
                        params.append(n['id'])  # id объявления
                        params.append(n['totalArea'])  # полная площадь
                        params.append(n['offerType'])  # флат - квартира
                        params.append(n['floorNumber'])  # этаж
                        params.append(n['livingArea'])  # жилая площадь

                        priceStr = str(n['formattedShortPrice'])
                        price = re.sub(r'\D', '', priceStr)
                        params.append(price)

                        with open('dataset2.csv','a',encoding='utf-8') as f:
                            string = ''
                            for ij in params:
                                string += str(ij) + ';'
                            string = string[:-1] +'\n'
                            f.writelines(string)
                    except Exception as ex:
                        print(ex.with_traceback())
                j+=1
                time.sleep(random.randint(5,9))

def start_parsing(yourId):
    split_parsing = [[1,51],[51,101],[101,151],[151,201],[201,251],[251,301],[301,351],[351,401],[401,451],[451,501],[501,551],[551],[578]]
    parsing(split_parsing[yourId][0],split_parsing[yourId][1])
start_parsing(0)