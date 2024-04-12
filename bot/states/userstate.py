from aiogram.fsm.state import State, StatesGroup


class LoginState(StatesGroup):
    login = State()
    password = State()
    authorized = State()


class QuestionStates(StatesGroup):
    waiting_for_question = State()
    asking_question = State()


class InfoState(StatesGroup):
    fullname = State()
    date_of_birth = State()
    date_of_death = State()
    birth_city = State()
    death_city = State()
    lover = State()
    kids = State()
    nationality = State()
    graduation = State()
    workplace = State()
    achievement = State()

