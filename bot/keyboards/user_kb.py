from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

start_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Шаг 1 - Заполнить основную информацию'
        )
    ],
    [
        KeyboardButton(
            text='Шаг 2 - Сгенерировать биографию'
        )
    ],
    [
        KeyboardButton(
            text='В разработке'
        ),
        KeyboardButton(
            text='Информация'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите действие")


help_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Главное Меню'
        )
    ]
])


my_profile_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text=''
        )
    ]
])


def generate_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text=questions[0], callback_data=f"q_{questions[0]}")],
        # [InlineKeyboardButton(text=questions[1], callback_data=f"q_{questions[1]}")],
        # [InlineKeyboardButton(text=questions[2], callback_data=f"q_{questions[2]}")],
        [InlineKeyboardButton(text="Заменить вопрос", callback_data="choose_question")],
        [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")]
    ])
    return keyboard


def new_epitaph_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="epitaph_yes")],
        [InlineKeyboardButton(text="Нет", callback_data="epitaph_no")],
        [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")]
    ])
    return keyboard


def epitaph_kb(user_id):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1️", callback_data="first_epitaph")],
        [InlineKeyboardButton(text="2️", callback_data="second_epitaph")],
        [InlineKeyboardButton(text="3️", callback_data="third_epitaph")],
        [InlineKeyboardButton(text="Open Webview", web_app=WebAppInfo(url=f"https://vvvvtrt2.pythonanywhere.com/epc/{user_id}"))]
    ])
    return keyboard


def update_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Обновить СП', callback_data="update_page")]
    ])
    return keyboard
