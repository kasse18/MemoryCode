from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram import Bot, F, Router
from aiogram.filters import CommandObject, Command, StateFilter
from bot.states.sender_state import SenderState


router = Router()


@router.message(StateFilter(None), Command('bc'))
async def bc_name(message: Message, command: CommandObject, state: FSMContext):
    if not command.args:
        await message.answer(f'Для создания рассылки введите команду /sender и название рассылки')
        return

    await message.answer(f'Создание рассылки. Название - {command.args}\r\n\r\n'
                         f'Отправьте текст сообщения')
    await state.set_state(SenderState.name_camp)
    await state.update_data(name_camp=command.args)
    await state.set_state(SenderState.get_message)


@router.message(StateFilter(None), Command('bc'))
async def bc_message(message: Message, command: CommandObject, state: FSMContext):
    await message.answer(
        text=f"Название рассылки: {F.text(message.from_user.first_name, message.from_user.last_name)}"
    )
