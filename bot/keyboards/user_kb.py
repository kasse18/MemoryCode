from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Заполнить основную информацию'
        )
    ],
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


epitaph_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Вернуться в главное меню'
        )
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder="Выберите действие")


def generate_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        # [InlineKeyboardButton(text=questions[0], callback_data=f"q_{questions[0]}")],
        # [InlineKeyboardButton(text=questions[1], callback_data=f"q_{questions[1]}")],
        # [InlineKeyboardButton(text=questions[2], callback_data=f"q_{questions[2]}")],
        [InlineKeyboardButton(text="Заменить вопрос", callback_data="choose_question")],
        [InlineKeyboardButton(text="В главное меню", callback_data="main_menu")]
        # [InlineKeyboardButton(text="Изменить ответ на вопрос", callback_data="change_answer")]
    ])
    return keyboard
