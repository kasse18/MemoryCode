import random

from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery, callback_query

from bot.database import db
from bot.keyboards.user_kb import start_kb, generate_keyboard, epitaph_kb
from bot.states.userstate import InfoState, QuestionStates, LoginState

router = Router()


# TODO // Выбор случайного вопроса из БД
async def get_random_question():
    question = random.choice(['ВОПРОС', 'ОТВЕТ', 'ВЕНЯ'])
    print(question)
    return question


# TODO // Добавление ответа на вопрос от пользователя в БД
async def add_user_question(user_id, question):
    return 0


@router.callback_query(F.data == 'change_answer')
# state=QuestionStates.waiting_for_question
async def change_answer(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await ask_question(callback_query.message, state)


@router.message(StateFilter(None), Command("epitaph"))
async def cmd_food(message: Message, state: FSMContext):
    await message.answer(
        text="Вы начали процесс генерации эпитафии\n\n"
             "После успешной генерации текста вы сможете сгенерировать новый\n\n",
        reply_markup=epitaph_kb
    )
    await state.set_state(QuestionStates.waiting_for_question)
    await ask_question(message, state)


@router.message(QuestionStates.waiting_for_question)
async def ask_question(message: types.Message, state: FSMContext):
    random_question = await get_random_question()
    user_id = message.from_user.id

    if random_question:
        await add_user_question(user_id, random_question)
        await message.answer(random_question, reply_markup=generate_keyboard())
        await state.set_state(QuestionStates.asking_question)


@router.message(QuestionStates.asking_question)
async def answer_question(message: types.Message, state: FSMContext):
    await message.answer("Ваш ответ сохранён!")
    await state.set_state(QuestionStates.waiting_for_question)
    await ask_question(message, state)


@router.callback_query(F.data == 'choose_question', QuestionStates.asking_question)
async def choose_question(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(QuestionStates.waiting_for_question)
    await call.message.delete()
    await ask_question(call.message, state)
