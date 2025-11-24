from aiogram.fsm.state import StatesGroup, State


class OrderState(StatesGroup):
    waiting_name = State()
    waiting_phone = State()
    waiting_comment = State()


class AddProductState(StatesGroup):
    category = State()
    name = State()
    description = State()
    price = State()
    country = State()
    photos = State()