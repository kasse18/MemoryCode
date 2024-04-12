from aiogram import types, Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery

from bot.keyboards.user_kb import start_kb


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в бота проекта Код Памяти!",
        reply_markup=start_kb,
        resize_keyboard=ReplyKeyboardRemove()
    )
