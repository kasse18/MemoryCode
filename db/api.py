import requests
import json
import asyncio
import time

token = ""
slug = 0
id = 0
data_ = []


async def log_in(data):
    global token, slug, id
    url = 'https://mc.dev.rand.agency/api/v1/get-access-token'

    data = {
        "email": data["login"],
        "password": data["password"],
        "device": "bot-v0.0.1"
    }

    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            data = response.json()
            print(data)
            token = data["access_token"]
            print(token)
            return data
        else:
            print("Error:", response.status_code, response.text)
            return {"status": "error"}
    except:
        print(1)
        return {"status": "error"}


async def search_sp(data):
    global token, slug, id
    url = 'https://mc.dev.rand.agency/api/cabinet/individual-pages'

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.get(url, headers=headers)

        print(response.json())
        slug = response.json()[0]["slug"]
        print(slug)
    except Exception as _ex:
        print(_ex)
        return {"status": "error"}


async def sp_svaz(data):
    global token, slug, id, data_
    url = 'https://mc.dev.rand.agency/api/page/search'

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': f'Bearer {token}'
    }

    data = {
        "name": "",
        "slug": slug,
        "birthday_at": "",
        "died_at": "",
        "slugs": [],
        "published_page": 1,
        "page": {"isTrusted": True}
    }

    try:
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            data_ = data["data"][0]
            id = data_["id"]
            print(data_)
            print(id)
            return data
        else:
            print("Error:", response.status_code, response.text)
            return {"status": "error"}
    except Exception as _ex:
        print(_ex)
        return {"status": "error"}


async def put_data(data):
    global token, slug, id, data_
    url = f'https://mc.dev.rand.agency/api/page/{slug}'

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': f'Bearer {token}'
    }

    null = None
    true = True
    false = False

    data = {

    "id": id,
    "name": "haha Виталий haha",
    "surname": null,
    "patronym": null,
    "birthday_at": "1700-01-02 00:00:00",
    "died_at": "1700-01-03 00:00:00",
    "epitaph": "КРАТКАЯ ЭПИТАФИЯ",
    "author_epitaph": "АВТОР ЭПИТАФИИ",
    "video_links": [
        {
            "url": "https://www.youtube.com/watch?v=figIDuctqMY",
            "enabled": true
        }
    ],
    "external_links": [
        {
            "link": "https://www.youtube.com/watch?v=figIDuctqMY",
            "link_name": "Блондинка за углом - YouTube",
            "enabled": true
        }
    ],
    "published_page": true,
    "accessible_by_password": false,
    "access_password": null,
    "user_id": 6,
    "master_id": null,
    "page_type_id": 1,
    "created_at": "2023-12-28T06:36:02.000000Z",
    "updated_at": "2023-12-28T07:17:13.000000Z",
    "deleted_at": null,
    "slug": slug,
    "burial_id": null,
    "price": null,
    }

    try:
        response = requests.put(url, json=data, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(data)
            return data
        else:
            print("Error:", response.status_code, response.text)
            return {"status": "error"}
    except Exception as _ex:
        print(_ex)
        return {"status": "error"}


if __name__ == '__main__':
    asyncio.run(log_in({"login": "team57@hackathon.ru", "password": "r3q4rLth"}))
    time.sleep(1)
    asyncio.run(search_sp({"login": "team57@hackathon.ru", "password": "r3q4rLth"}))
    time.sleep(1)
    asyncio.run(sp_svaz({"login": "team57@hackathon.ru", "password": "r3q4rLth"}))
    time.sleep(1)
    asyncio.run(put_data({"login": "team57@hackathon.ru", "password": "r3q4rLth"}))

# 4268|PvotwqVbPog4XCOqHF1qLb8fhcIGjkx1gkFHBay5
# 'slug': 23332584  'lead_id': 37360005
# [{'id': 8848, 'name': 'Команда Хакатон 57/2', 'surname': None, 'patronym': None, 'birthday_at': '2024-01-01 00:00:00', 'died_at': '2024-01-01 00:00:00', 'epitaph': None, 'author_epitaph': None, 'video_links': [], 'external_links': None, 'published_page': True, 'accessible_by_password': False, 'access_password': None, 'user_id': 2321, 'master_id': 122, 'page_type_id': 1, 'created_at': '2024-04-11T15:51:30.000000Z', 'updated_at': '2024-04-13T05:57:33.000000Z', 'deleted_at': None, 'slug': 23332584, 'burial_id': None, 'price': 5450, 'commission': '1090', 'video_images': [], 'payment_id': None, 'blank_id': None, 'is_blank': False, 'is_vip': False, 'views': 1, 'visitors': 1, 'lead_id': 37360005, 'index_page': False, 'filled_fields': [], 'position': None, 'is_referral': False, 'banner_enabled': True, 'locale': 'ru', 'was_indexed': False, 'qr_hidden': False, 'historical_status_id': 1, 'count_filled_fields': 0, 'parent_tree_id': None, 'custom_birthday_at': None, 'custom_died_at': None, 'main_image': None, 'start': {'day': '01', 'month': '01', 'year': 2024}, 'end': {'day': '01', 'month': '01', 'year': 2024}, 'lastName': 'Хакатон 57/2', 'firstName': 'Команда', 'link': 'https://mc.dev.rand.agency/page/23332584', 'free_access': True, 'full_name': ' Команда Хакатон 57/2 ', 'burial_place': False, 'page_type_name': 'pageType.full', 'count_fields': 10, 'media': []}, {'id': 8847, 'name': 'Команда Хакатон 57/1', 'surname': None, 'patronym': None, 'birthday_at': '2024-01-01 00:00:00', 'died_at': '2024-01-01 00:00:00', 'epitaph': 'Тест', 'author_epitaph': 'Тест', 'video_links': [], 'external_links': None, 'published_page': True, 'accessible_by_password': False, 'access_password': None, 'user_id': 2321, 'master_id': 122, 'page_type_id': 1, 'created_at': '2024-04-11T15:47:00.000000Z', 'updated_at': '2024-04-13T19:57:38.000000Z', 'deleted_at': None, 'slug': 11831155, 'burial_id': None, 'price': 5450, 'commission': '1090', 'video_images': [], 'payment_id': None, 'blank_id': None, 'is_blank': False, 'is_vip': False, 'views': 2, 'visitors': 2, 'lead_id': 37359353, 'index_page': False, 'filled_fields': ['biography_1', 'epitaph'], 'position': None, 'is_referral': False, 'banner_enabled': True, 'locale': 'ru', 'was_indexed': False, 'qr_hidden': False, 'historical_status_id': 1, 'count_filled_fields': 2, 'parent_tree_id': None, 'custom_birthday_at': None, 'custom_died_at': None, 'main_image': None, 'start': {'day': '01', 'month': '01', 'year': 2024}, 'end': {'day': '01', 'month': '01', 'year': 2024}, 'lastName': 'Хакатон 57/1', 'firstName': 'Команда', 'link': 'https://mc.dev.rand.agency/page/11831155', 'free_access': True, 'full_name': ' Команда Хакатон 57/1 ', 'burial_place': False, 'page_type_name': 'pageType.full', 'count_fields': 10, 'media': []}]
