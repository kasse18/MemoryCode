import json
import random

from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery, callback_query

from bot.database import db
from bot.keyboards.user_kb import start_kb, generate_keyboard, epitaph_kb, new_epitaph_kb
from bot.states.userstate import InfoState, QuestionStates, LoginState
from parse_yandex_gpt import Prompt

router = Router()
word_list = ['В главное меню']


async def get_random_question():
    questions = []
    question = random.choice([
    'Расскажите, какие достижения этого человека вызывают у вас особенную гордость?',
    'Чем этот человек запомнился вам и окружающим?',
    'Как бы вы описали этого человека в трёх словах?',
    'Какие люди или события оказали наибольшее влияние на формирование личности этого человека?',
    'Чем этот человек вас впечатлил? Чем удивил?',
    'Какое ваше первое воспоминание об этом человеке?',
    'Какие  ваши любимые воспоминания об этом человеке?',
    'Как этот человек обычно встречал гостей?',
    'Как этот человек любил проводить свободное время? Было ли у него хобби или страсть?',
    'Какие особые черты характера вы выделяете у этого человека и почему?',
    'Как бы вы описали особенности характера этого человека, которые вас больше всего впечатлили?',
    'Как о нем отзывались его друзья и знакомые?',
    'Есть ли книга или фильм, который особенно вдохновляли или изменили видение мира?',
    "Чем этот человек гордился в своей жизни больше всего?",
    "Было ли у этого человека любимое место? Если да, опишите его подробно",
    "Были ли интересные истории, шутки, анекдоты или фразы, которые человек любил повторять?",
    "Каких убеждения, какой жизненной философии придерживался этот человек? Каковы его принципы?",
    "Какие обстоятельства повлияли на выбор его профессии? Что ему нравилось в работе?",
    "Какое самое яркое воспоминание у него было связано с путешествиями? Возможно, этот человек рассказывал про самый необычный маршрут, который он прошел.",
    "Кто или что вдохновляло этого человека в повседневной жизни? Может, у него был нестандартный источник вдохновения?"
    ])
    questions.append(question)
    return question


# TODO // Добавление ответа на вопрос от пользователя в БД
async def add_user_question(user_id, question):
    return 0


@router.callback_query(F.data == 'change_answer')
# state=QuestionStates.waiting_for_question
async def change_answer(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await ask_question(call.message, state)


@router.message((F.text == 'Сгенерировать биографию'), StateFilter(None))
@router.message(F.text, StateFilter(None), Command("epitaph"))
async def cmd_epitaph(message: Message, state: FSMContext):
    await message.answer(
        text="Для успешной генерации текста мне необходимо собрать информацию\n\n"
             "Вам предстоит ответить на 8 вопросов. Если ответ на вопрос вызывает трудности,"
             "его можно заменить с помощью кнопки под сообщением\n\n"
    )
    stats = dict()
    await state.update_data(fullinfo=stats)
    await state.set_state(QuestionStates.waiting_for_question)
    await state.update_data(answers_count=0)
    await state.update_data(rand='')
    await state.update_data(biography='')
    await ask_question(message, state)


@router.message(QuestionStates.waiting_for_question)
async def ask_question(message: Message, state: FSMContext):
    random_question = await get_random_question()
    user_id = message.from_user.id

    if random_question:
        data = await state.get_data()
        data['rand'] = random_question
        await state.set_data(data)
        # await add_user_question(user_id, random_question)
        await message.answer(random_question, reply_markup=generate_keyboard())
        await state.set_state(QuestionStates.asking_question)


@router.message(QuestionStates.asking_question)
async def answer_question(message: Message, state: FSMContext):
    # await message.answer("Ваш ответ сохранён!")
    await state.set_state(QuestionStates.waiting_for_question)
    data = await state.get_data()
    stats = data['fullinfo']
    number = data['answers_count']
    stats[data['rand']] = message.text
    data['answers_count'] += 1
    await state.set_data(data)
    # if data['answers_count'] == 8:
    #     await message.answer("А теперь последний вопрос!\n\n"
    #                          "Добавьте любую дополнительную информацию о данном человеке\n\n"
    #                          "Это может быть факт, случай или воспоминание")
    #
    #     await state.set_state(QuestionStates.asking_question)
    #     # await ask_question(message, state)

    if data['answers_count'] == 8:
        await message.answer("Спасибо за ваши ответы!\n\nСейчас на основе ваших ответов будет сгенерирована биография")
        fullinfo = data['fullinfo']
        with open('info.json') as f:
            info = json.load(f)
        print(fullinfo)
        prompt = Prompt()
        biography = prompt.get_biohraphy(fullinfo, info)
        print(biography)
        await message.answer("Биография сгенерирована!\n\n"
                             f"{biography}")
        await message.answer('Хотите сгенерировать эпитафию на основе биографии?', reply_markup=new_epitaph_kb())
        data = await state.get_data()
        data['biography'] = biography
        await state.set_data(data)
    else:
        await state.set_state(QuestionStates.asking_question)
        await message.answer("Ответ принят, ожидайте следующий вопрос.")
        await ask_question(message, state)


@router.callback_query(F.data == 'epitaph_yes')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    biography = data['biography']
    personal_data = data['fullinfo']
    prompt = Prompt()
    new_epitaph = prompt.change_epitaphy(biography, personal_data)
    await call.message.answer(
        "Отлично! Сейчас сгенерирую!",
        disable_web_page_preview=True
    )
    await call.message.answer("Я готов предложить вам 3 варианта эпитафии, основанные на основной информации\n"
                             "После генерации биографии, вы сможете сгенерировать улучшенную версию эпитафии\n\n"
                             f"1️⃣\n{new_epitaph[0]}\n\n2️⃣\n{new_epitaph[1]}\n\n3️⃣\n{new_epitaph[2]}",
                              reply_markup=start_kb, disable_web_page_preview=True)
    await state.clear()


@router.callback_query(F.data == 'epitaph_no')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer(
        "Хорошо!",
        reply_markup=start_kb, disable_web_page_preview=True
    )


@router.callback_query(F.data == 'choose_question', QuestionStates.asking_question)
async def choose_question(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(QuestionStates.waiting_for_question)
    await call.message.delete()
    await ask_question(call.message, state)


@router.callback_query(F.data == 'main_menu')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer(
        "Вы вернулись в главное меню.",
        reply_markup=start_kb, disable_web_page_preview=True
    )


@router.callback_query(F.data.startswith('q_'))
async def process_question_callback(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    question_text = call.data.replace('q_', '')
    await call.message.delete()
    await call.message.answer(question_text)
    await state.set_state(QuestionStates.asking_question)


async def get_base_question(number):
    questions = ['Укажите ФИО\nНапример: `Петров Валерий Иванович`', 'Введите дату рождения\nНапример: `01.01.1984`',
                 'Введите дату смерти\nНапример: `01.01.2024`', 'Введите место рождения\nНапример: `Москва, Россия`',
                 'Введите место Смерти\nНапример: `Самара, Россия`', 'Укажите детей(если детей нет, отправьте "-")\nНапример: `Петров Иван, Петров Пётр`',
                 'Укажите ФИО Супруга(ги)\nНапример: `Петрова Валерия Ивановна`', 'Укажите гражданство\nНапример: `Российская Федерация`',
                 'Укажите учебное заведение, которое окончил человек\nНапример: `НИТУ МИСИС, прикладная математика`',
                 'Укажите род деятельности\nНапример: `Backend-разработчик`', 'Укажите награды/премии/достижения\nНапример: `Звание "Заслуженный инженер"`'
                 ]

    return questions[number]


@router.message(F.text == 'Заполнить основную информацию', StateFilter(None))
@router.message(F.text, StateFilter(None), Command("baseinfo"))
async def base_info(message: Message, state: FSMContext):
    await message.answer(
        text="Сейчас вам потребуется ответить на 11 коротких вопросов\n\n"
             "Время заполнения информации займёт менее 5 минут\n\n"
             "Отвечать на каждый вопрос следует одним сообщением"
    )
    stat = dict()
    await state.update_data(fullinfo=stat)
    await state.set_state(InfoState.waiting_for_question)
    await state.update_data(answers_count=0)
    await ask_base_question(message, state)


@router.message(InfoState.waiting_for_question)
async def ask_base_question(message: Message, state: FSMContext):
    data = await state.get_data()
    number = data['answers_count']
    question = await get_base_question(number)
    await state.update_data(last_q=number)
    if question:
        await message.answer(question, parse_mode='MARKDOWN')
        await state.set_state(InfoState.asking_question)


@router.message(InfoState.asking_question)
async def answer_base_question(message: Message, state: FSMContext):
    # await message.answer("Ваш ответ сохранён!")
    words = ['ФИО', 'Дата рождения', 'Дата смерти', 'Место рождения', 'Место смерти', 'Дети', 'Супруг(а)',
             'Гражданство', 'Образование', 'Род деятельности', 'Премии, достижения, награды']
    data = await state.get_data()
    stat = data['fullinfo']
    number = data['answers_count']
    stat[words[number]] = message.text
    await state.set_state(InfoState.waiting_for_question)
    data['answers_count'] += 1
    await state.set_data(data)
    if data['answers_count'] >= 11:
        fullinfo = data['fullinfo']
        print(fullinfo)
        with open('info.json', 'w') as f:
            json.dump(fullinfo, f)
        prompt = Prompt()
        epitaph = prompt.get_epitaphy(fullinfo)
        print(epitaph)
        await message.answer("Вы ответили на все вопросы!\n\n"
                             "Я готов предложить вам 3 варианта эпитафии, основанные на основной информации\n"
                             "После генерации биографии, вы сможете сгенерировать улучшенную версию эпитафии\n\n"
                             f"1️⃣\n{epitaph[0]}\n\n2️⃣\n{epitaph[1]}\n\n3️⃣\n{epitaph[2]}\n\n"
                             f"Выберите эпитафию, которую хотите сохранить", reply_markup=epitaph_kb())

        await state.clear()
    else:
        await state.set_state(InfoState.asking_question)
        # await message.answer("Ответ принят, ожидайте следующий вопрос.")
        await ask_base_question(message, state)


@router.callback_query(F.data == 'first_epitaph')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer(
        "Теперь вы можете начать процесс генерации биографии",
        reply_markup=start_kb, disable_web_page_preview=True
    )


@router.callback_query(F.data == 'second_epitaph')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer(
        "Теперь вы можете начать процесс генерации биографии",
        reply_markup=start_kb, disable_web_page_preview=True
    )


@router.callback_query(F.data == 'third_epitaph')
async def main_menu(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer(
        "Теперь вы можете начать процесс генерации биографии",
        reply_markup=start_kb, disable_web_page_preview=True
    )
