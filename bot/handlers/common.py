from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
import requests
from bot.keyboards.user_kb import start_kb
from bot.states.userstate import LoginState

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    is_authenticated = await check_auth(message.from_user.id)
    await message.answer(
        "Добро пожаловать в бота проекта Код Памяти!\nС помощью данного бота вы отредактировать страницу памяти, "
        "а также сгенерировать эпитафию и/или биографию для страницы памяти.\n\n")
    if not is_authenticated:
        await message.answer("Вы не авторизованы.\n\nВведите ваш логин.")

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
    await message.answer("Теперь введите ваш пароль.")

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
    else:
        await message.answer("Ошибка авторизации. Попробуйте снова.")

    await state.clear()


async def check_auth(user_id):
    url = 'http://127.0.0.1:8000/check'

    data = {
        'id': user_id,
    }

    response = requests.post(url, json=data)

    if response.json()['data'] == 'error':
        return False
    return True


# Функция для аутентификации пользователя через API
async def authenticate_user(user_id, login, password):
    url = 'http://127.0.0.1:8000/log_in'

    data = {
        'id': user_id,
        "login": login,
        "password": password
    }

    response = requests.post(url, json=data)

    return response.json()['status'] == 'error'


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
