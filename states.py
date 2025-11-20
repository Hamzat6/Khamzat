from aiogram.fsm.state import StatesGroup, State


class OrderState(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_comment = State()
