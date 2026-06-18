from aiogram.fsm.state import StatesGroup, State


class SurveyState(StatesGroup):
    answering = State()
