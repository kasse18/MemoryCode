from aiogram.fsm.state import State, StatesGroup


class QuestionStates(StatesGroup):
    waiting_for_question = State()
    asking_question = State()


class EpitaphState(StatesGroup):
    fullname = State()
    date_of_birth = State()
    date_of_death = State()
    birth_city = State()
    death_city = State()
    achievement = State()
    workplace = State()

