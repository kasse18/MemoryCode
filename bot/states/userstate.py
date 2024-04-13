from aiogram.fsm.state import State, StatesGroup


class LoginState(StatesGroup):
    login = State()
    password = State()
    # authorized = State()
    # unauthorized = State()


class QuestionStates(StatesGroup):
    waiting_for_question = State()
    asking_question = State()


class InfoState(StatesGroup):
    waiting_for_question = State()
    asking_question = State()


class AuthState(StatesGroup):
    AUTHORIZED = State()
    UNAUTHORIZED = State()
