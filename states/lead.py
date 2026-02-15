from aiogram.fsm.state import StatesGroup, State

class LeadState(StatesGroup):
    name = State()
    phone = State()
    comment = State()