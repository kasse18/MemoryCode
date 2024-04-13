import requests
import json
import asyncio



async def log_in(data):
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
            return data
        else:
            print("Error:", response.status_code, response.text)
            return {"status": "error"}
    except:
        return {"status": "error"}




if __name__ == '__main__':
    asyncio.run(log_in({"login": "team57@hackathon.ru", "password": "r3q4rLth"}))
