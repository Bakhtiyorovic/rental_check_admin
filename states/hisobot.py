from aiogram.filters.state import StatesGroup, State

class ReportStates(StatesGroup):
    waiting_account = State()
    waiting_hours = State()
    waiting_price = State()
