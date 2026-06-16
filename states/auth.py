from aiogram.fsm.state import (
    State,
    StatesGroup
)


class AuthStates(StatesGroup):

    waiting_secret_code = State()