import json

from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
import requests
from bot.keyboards.user_kb import start_kb
from bot.states.userstate import LoginState
from db import api

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    is_authenticated = await check_auth(message.from_user.id)
    if message.text == '/start':
        await message.answer(
            "Добро пожаловать в бота проекта Код Памяти!\nС помощью данного бота вы отредактировать страницу памяти, "
            "а также сгенерировать эпитафию и/или биографию для страницы памяти.\n\n")
    if not is_authenticated:
        await message.answer("Вы не авторизованы.\n\nДля входа в аккаунт Введите вашу электронную почту\n\n"
                             "Для теста: `team57@hackathon.ru`", parse_mode='MARKDOWN')

        await state.set_state(LoginState.login)
    else:
        await message.answer(
            "Выберите действие!",
            reply_markup=start_kb,
            resize_keyboard=ReplyKeyboardRemove()
        )


@router.message(LoginState.login)
async def process_login(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Теперь введите ваш пароль.\n\n"
                         "Для теста: `r3q4rLth`", parse_mode='MARKDOWN')

    await state.set_state(LoginState.password)


@router.message(LoginState.password)
async def process_password(message: Message, state: FSMContext):
    data = await state.get_data()
    login = data.get('login')
    password = message.text
    is_authenticated = await authenticate_user(message.from_user.id, login, password)

    if is_authenticated:
        # Обновление базы данных
        # update_user_auth_status(user_id=message.from_user.id, login=login, password=password, is_auth=True)  # Пример

        await message.answer("Вы успешно авторизованы!",
                             reply_markup=start_kb)
        await state.clear()
    else:
        await message.answer("Ошибка авторизации. Попробуйте снова.\n\nВведите вашу электронную почту\n\n"
                             "Для теста: `team57@hackathon.ru`", parse_mode='MARKDOWN')
        await state.set_state(LoginState.login)
        # await process_login(message, state)


async def check_auth(user_id):
    # url = 'http://127.0.0.1:8000/check'
    #
    # data = {
    #     'id': user_id,
    # }
    #
    # response = requests.post(url, json=data)
    #
    # if response.json()['data'] == 'error':
    #     return False
    # return True
    return False


# Функция для аутентификации пользователя через API
async def authenticate_user(user_id, login, password):
    url = 'https://mc.dev.rand.agency/api/v1/get-access-token'

    data = {
        "email": login,
        "password": password,
        "device": "bot-v0.0.1"
    }

    response = requests.post(url, json=data)
    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            data = response.json()
            with open('token.json', 'w') as f:
                json.dump(data['access_token'], f)
            print(data)
            return data
        else:
            print("Error:", response.status_code, response.text)
            return False
    except:
        return False


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "главное меню")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Вы в главном меню",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "главное меню")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выберите действие",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["info"]))
@router.message(F.text.lower() == "информация")
async def cmd_info(message: Message, state: FSMContext):
    await message.answer(
        text="Данный бот создан для бла-бла-бла",
        reply_markup=start_kb,
        resize_keyboard=ReplyKeyboardRemove()
    )
