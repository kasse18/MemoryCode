from aiogram.filters import Filter, StateFilter
from aiogram.fsm.state import State, StatesGroup


class SenderState(StatesGroup):
    name_camp = State()
    get_message = State()
