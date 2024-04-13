import requests
import os
from dotenv import load_dotenv

load_dotenv()

FOLDER_ID = os.environ.get("FOLDER_ID")
API_KEY = os.environ.get("API_KEY")


class Prompt:
    
    def get_biohraphy(self, s:str, personal_data:str):

        temperature = 0.2

        prompt_for_generate_biography = { 
            "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-pro/latest",
            "completionOptions": {
                "stream": False, 
                "temperature": temperature,
                "maxTokens": "50000"
            },
            "messages": [
                {
                "role": "system",
                'text': f'данный текст - несколько блоков, которые являются ответами на вопросы о жизни некоторого человека. \
                    твоя задача - составить на основе этих блоков очень трогательнуюбиографию, используя литературный стиль и\
                          большое количество эпитетов. Часто повторяющиеся слова замени синонимами. Личные данные человека - {personal_data.items()}'   
                },
                {
                "role": "user",
                'text': s
                }
            ]
        }
        
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {API_KEY}"
        }

        response = requests.post(url, headers=headers, json=prompt_for_generate_biography)
        
        return response.json()['result']['alternatives'][0]['message']['text']
    

    def get_epitaphy(self, personal_data:dict):
    # def get_epitaphy(self, biography:str):
        epitaphies = []

        # for temperature in [0.4, 0.6, 0.8]:
        
        for temperature in [0.3, 0.6, 0.9]:

            prompt_for_generate_epitaphy = {
                "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-pro/latest",
                "completionOptions": {
                    "stream": False,
                    "temperature": temperature,
                    "maxTokens": "2000"
                    }, 
                "messages": [
                    {
                        "role": "system",
                        'text': 'данный текст - личные данные некоторого человека. твоя задача - суммаризировать этот текст и составить на его основе очень трогательную эпитафию, \
                            используя большее количество эпитетов.\
                            В ответе не форматируй текст. Ответ должен содержать ТОЛЬКО эпитафию. Так, чтобы твой ответ можно было сразу высечь на могильном камне.'
                    }, 
                    {
                        "role": "user",
                        'text': ''.join([f"{i[0]} {i[1]}." for i in personal_data.items()])
                    }, 
                ]
            }
        
            url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Api-Key {API_KEY}"
            }

            response = requests.post(url, headers=headers, json=prompt_for_generate_epitaphy)
            epitaphies.append(response.json()['result']['alternatives'][0]['message']['text'])

        return epitaphies

    def change_epitaphy(self, biography:str, personal_data:dict):

        epitaphies = []

        for temperature in [0.3, 0.6, 0.9]:

            prompt_for_generate_epitaphy = {
                "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-pro/latest",
                "completionOptions": {
                    "stream": False,
                    "temperature": temperature,
                    "maxTokens": "2000"
                    }, 
                "messages": [
                    {
                        "role": "system",
                        'text': 'данный текст - личные данные некоторого человека. твоя задача - суммаризировать этот текст и составить на его основе очень трогательную эпитафию, \
                            используя большее количество эпитетов.\
                            В ответе не форматируй текст. Ответ должен содержать ТОЛЬКО эпитафию. Так, чтобы твой ответ можно было сразу высечь на могильном камне.'
                    }, 
                    {
                        "role": "user",
                        'text':'Персональная данные' + ''.join([f"{i[0]} {i[1]}." for i in personal_data.items()]) + f'Биография - {biography}'
                    }, 
                ]
            }
        
            url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Api-Key {API_KEY}"
            }

            response = requests.post(url, headers=headers, json=prompt_for_generate_epitaphy)
            epitaphies.append(response.json()['result']['alternatives'][0]['message']['text'])

        return epitaphies


 
prptpr = Prompt()
 
bio = 'Мой дедушка родился в городе Волжском Волгоградской области. Он был единственным ребёнком у своей мамы, но в семье также воспитывался его старший брат. Великая Отечественная война и её последствия пришлись на годы его детства. Единственным воспоминанием из детства у него остались три дня в окопе, проведенные без еды и воды. В основном его воспитывала мама и старший брат, так как родители были заняты работой. Дедушка всегда поддерживал тёплые отношения со своей мамой, а также со своим братом.\
В школе он был пионером и старостой, учился хорошо и всегда старался быть первым. Благодаря своей инициативе он встретил свою будущую жену, с которой прожил всю жизнь.\
После школы он поступил в техникум и получил образование инженера. Студенческие годы были для него веселыми и насыщенными. Всю жизнь дедушка усердно трудился, работая на заводе, и вышел на пенсию с 40-летним стажем работы\
Дедушка имел одну жену, единственную и неповторимую, с которой они прожили в любви и согласии всю жизнь. У них родились две дочери, старшая из которых, Виктория, всю жизнь искала своё призвание и в итоге стала известной успешной женщиной с множеством знакомых, умеющей найти подход к любому человеку. Младшая дочь, Евгения, пошла по стопам дедушки и стала выдающимся хирургом.\
На старости лет дедушка активно занимался воспитанием своих детей и внуков, а также работал на своей даче с большим огородом. Несмотря на свой возраст, он не останавливался на достигнутом и продолжал трудиться, даже когда вышел на пенсию, устроившись работать сторожем.\
Мой дедушка всегда поступал честно и справедливо, держал слово и был заботливым отцом, мужем и дедушкой. Он научил меня стремиться к лучшему и никогда не опускать руки в трудные моменты.'

ne_bio = 'Родился в 1945г под Курском. В детстве любил оставаться на ночь у дедушки и ухаживать за пчелами.\
Его мама была учительницей, а отец фотографом. У него было две сестры, с которыми он любил играть.\
    Школу закончил с хорошими отметками.\
После школы отправился покорять большой город и поступил в балтийский флот, ему очень шла его морская форма.\
 Проработал моряком 36 лет, после чего вышел на пенсию\
Его жена преподавала в институте и отличалась строгим характером. У них была большая семья: две дочки, четыре внука и правнук. Он любил играть с детьми и внуками, воспитывали их.\
В старости он вёл активный образ жизни. Путешествовал по России и играл на баяне.\
Он всегда подбадривал и мог поддержать. Все его называли по-разному: "Товарищ полковник", "Человек-энциклопедия", и, конечно, "любимый дедушка"'

# print(prptpr.get_biohraphy(ne_bio, {'fio': 'fio'}))

print(prptpr.get_epitaphy({'fio': 'fio'}))