from aiogram.filters.state import StatesGroup, State

class AddAccountStates(StatesGroup):
    waiting_account_number = State()
    waiting_owners = State()
    waiting_owner_percent = State()
    confirm_account = State()

    
class DeleteAccountStates(StatesGroup):
    waiting_account_number = State()