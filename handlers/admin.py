from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import AddProductState
from data.products import PRODUCTS
from data.config import ADMIN_IDS

router = Router()
LEADS = []


def is_admin(message: Message):
    return message.from_user.id in ADMIN_IDS


# ---------------------------
# /admin
# ---------------------------
@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if not is_admin(message):
        return await message.answer("Доступ запрещен.")

    await message.answer(
        "Админ панель:\n"
        "/add — добавить товар\n"
        "/list — список товаров"
    )


# ---------------------------
# /add Товар
# ---------------------------
@router.message(F.text == "/add")
async def start_add(message: Message, state: FSMContext):
    if not is_admin(message):
        return await message.answer("Доступ запрещен.")

    await state.set_state(AddProductState.category)
    await message.answer(
        "Введите категорию из списка:\n" +
        "\n".join(PRODUCTS.keys())
    )


@router.message(AddProductState.category)
async def add_category(message: Message, state: FSMContext):
    category = message.text.strip()

    if category not in PRODUCTS:
        return await message.answer("Такой категории нет. Введите снова.")

    await state.update_data(category=category)
    await state.set_state(AddProductState.name)
    await message.answer("Введите название товара:")


@router.message(AddProductState.name)
async def add_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProductState.description)
    await message.answer("Введите описание товара:")


@router.message(AddProductState.description)
async def add_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddProductState.price)
    await message.answer("Введите цену товара (число):")


@router.message(AddProductState.price)
async def add_price(message: Message, state: FSMContext):
    price = message.text.strip()

    if not price.isdigit():
        return await message.answer("Цена должна быть числом. Введите снова.")

    await state.update_data(price=price)
    await state.set_state(AddProductState.country)
    await message.answer("Страна производства:")


@router.message(AddProductState.country)
async def add_country(message: Message, state: FSMContext):
    await state.update_data(country=message.text)
    await state.set_state(AddProductState.photos)
    await message.answer("Отправьте ссылки на фото через запятую:")


@router.message(AddProductState.photos)
async def add_photos(message: Message, state: FSMContext):
    urls = [u.strip() for u in message.text.split(",") if u.strip()]

    if not urls:
        return await message.answer("Введите хотя бы одну ссылку.")

    data = await state.get_data()

    new_product = {
        "name": data["name"],
        "description": data["description"],
        "price": data["price"],
        "country": data["country"],
        "images": urls
    }

    PRODUCTS[data["category"]].append(new_product)

    await state.clear()
    await message.answer("Товар успешно добавлен.")


# ---------------------------
# /list — список товаров
# ---------------------------
@router.message(F.text == "/list")
async def list_all(message: Message):
    if not is_admin(message):
        return await message.answer("Доступ запрещен.")

    text = "Список товаров:\n\n"

    for category, items in PRODUCTS.items():
        text += f"{category} — {len(items)} шт.\n"

    await message.answer(text)


# ---------------------------
# /delete — удалить товар по категории и индексу
# ---------------------------
@router.message(F.text.startswith('/delete'))
async def delete_product(message: Message):
    if not is_admin(message):
        return await message.answer("Доступ запрещен.")


    parts = message.text.split()
    if len(parts) != 3:
        return await message.answer("Нужно ввести: /delete <category> <index>")


    category, index_str = parts[1], parts[2]


    if category not in PRODUCTS:
        return await message.answer("Такой категории нет.")


    if not index_str.isdigit():
        return await message.answer("Индекс должен быть числом.")


    index = int(index_str)


    if index < 0 or index >= len(PRODUCTS[category]):
        return await message.answer("Нет товара с таким индексом.")


    deleted = PRODUCTS[category].pop(index)


    await message.answer(f"Товар '{deleted['name']}' удалён." )



