from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Сгенерировать эпитафию'
        ),
        KeyboardButton(
            text='Сгенерировать биографию'
        )
    ],
    [
        KeyboardButton(
            text='Мой профиль'
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
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Выбрать другой вопрос", callback_data="choose_question"))
    keyboard.add(InlineKeyboardButton("Изменить ответ на вопрос", callback_data="change_answer"))
    return keyboard