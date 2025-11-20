from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import OrderState
from database import add_product, list_products
from data.config import ADMIN_IDS

router = Router()

# Простой админ: команда /admin (только для ADMIN_IDS)


@router.message(F.text == "/admin")
async def admin_index(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Доступ запрещён.")
        return
    await message.answer("Админ панель:\nКоманды:\n/add - добавить тестовый продукт\n/list - список продуктов")


@router.message(F.text == "/add")
async def admin_add(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("Доступ запрещён.")
        return
    # Добавим тестовый продукт (в реале — FSM для добавления)
    add_product(name='Тестовая кровать', category='bedroom_russian', subcategory='-', country='Россия', ptype='прямая', price=12345, description='Тестовый', images_csv='https://example.com/1.jpg')
    await message.answer('Продукт добавлен.')


@router.message(F.text == "/list")
async def admin_list(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer('Доступ запрещён.')
        return
    rows = list_products()
    if not rows:
        await message.answer('Нет продуктов.')
        return
    text = '\n'.join([f"{r[0]}: {r[1]} ({r[2]})" for r in rows])
    await message.answer(f"Продукты:\n{text}")
