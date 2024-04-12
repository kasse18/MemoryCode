from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

from bot.database import db
from bot.keyboards.user_kb import start_kb, generate_keyboard
from bot.states.userstate import InfoState, QuestionStates, LoginState

router = Router()


# TODO // ADD DATABASE
async def get_random_question():
    async with db.acquire() as conn:
        question = await conn.fetchrow("SELECT question FROM questions ORDER BY random() LIMIT 1")
        return question['question'] if question else None


# TODO // ADD DATABASE
async def add_user_question(user_id, question):
    async with db.acquire() as conn:
        await conn.execute("INSERT INTO user_questions (user_id, question) VALUES ($1, $2)", user_id, question)


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
        reply_markup=start_kb
    )
    await QuestionStates.waiting_for_question.set()


@router.message(Command('ask_question'))
# state=QuestionStates.waiting_for_question
async def ask_question(message: types.Message, state: FSMContext):
    random_question = await get_random_question()
    user_id = message.from_user.id

    if random_question:
        await add_user_question(user_id, random_question)
        await message.answer(random_question, reply_markup=generate_keyboard())
        await QuestionStates.asking_question.set()


@router.message(QuestionStates.asking_question)
async def answer_question(message: types.Message, state: FSMContext):
    await message.answer("Ваш ответ сохранён!")
    await QuestionStates.waiting_for_question.set()


@router.callback_query(F.data == 'choose_question', QuestionStates.asking_question)
async def choose_question(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await QuestionStates.waiting_for_question.set()
    await ask_question(callback_query.message, state)