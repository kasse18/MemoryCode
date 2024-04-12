from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

from bot.keyboards.user_kb import start_kb
from bot.states.userstate import LoginState

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()

    is_authenticated = await check_auth(message.from_user.id)

    if not is_authenticated:
        await message.answer("Вы не авторизованы.\n\nВведите ваш логин.")

        await LoginState.login.set()
    else:
        await message.answer(
            "Добро пожаловать в бота проекта Код Памяти!\nС помощью данного бота вы отредактировать страницу памяти, "
            "а также сгенерировать эпитафию и/или биографию для страницы памяти.\n"
            "Выберите действие!",
            reply_markup=start_kb,
            resize_keyboard=ReplyKeyboardRemove()
        )


@router.message(LoginState.login)
async def process_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Теперь введите ваш пароль.")

    await LoginState.password.set()


@router.message(LoginState.password)
async def process_password(message: types.Message, state: FSMContext):
    # Получаем данные из состояния
    data = await state.get_data()
    login = data.get('login')
    password = message.text

    # Проверка авторизации через API
    is_authenticated = await authenticate_user(login, password)

    if is_authenticated:
        # Обновление базы данных
        # update_user_auth_status(user_id=message.from_user.id, login=login, password=password, is_auth=True)  # Пример

        await message.answer("Вы успешно авторизованы!")
    else:
        await message.answer("Ошибка авторизации. Попробуйте снова.")

    await state.clear()


async def check_auth(user_id):
    # Здесь должна быть логика для проверки авторизации через API

    return False


# Функция для аутентификации пользователя через API
async def authenticate_user(login, password):
    # Здесь должна быть логика для аутентификации пользователя через API

    return True


@router.message(StateFilter(None), Command(commands=["cancel"]))
@router.message(default_state, F.text.lower() == "Главное меню")
async def cmd_cancel_no_state(message: Message, state: FSMContext):
    # Стейт сбрасывать не нужно, удалим только данные
    await state.set_data({})
    await message.answer(
        text="Вы в главном меню",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "Главное меню")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Выберите действие",
        reply_markup=ReplyKeyboardRemove()
    )