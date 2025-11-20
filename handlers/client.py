from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from keyboards import main_menu, bedroom_menu, kitchen_menu, sofa_menu, product_buttons
from states import OrderState
from data.products import PRODUCTS

router = Router()
user_history = {}

# ========== /start ==========


@router.message(F.text == "/start")
async def start(message: Message):
    user_history[message.from_user.id] = ["main"]
    await message.answer("Добро пожаловать в каталог мебели.", reply_markup=main_menu())

# ========== обработка категорий ==========


@router.callback_query(F.data.startswith("category_"))
async def category_handler(callback: CallbackQuery):
    await callback.answer()  # кнопка гаснет

    user_id = callback.from_user.id
    data = callback.data.replace("category_", "")
    if user_id not in user_history:
        user_history[user_id] = ["main"]
    user_history[user_id].append(data)

    # если это главная категория
    if data in ["bedroom", "kitchen", "sofa"]:
        if data == "bedroom":
            await callback.message.edit_text("Выберите подкатегорию:", reply_markup=bedroom_menu())
        elif data == "kitchen":
            await callback.message.edit_text("Выберите подкатегорию:", reply_markup=kitchen_menu())
        elif data == "sofa":
            await callback.message.edit_text("Выберите подкатегорию:", reply_markup=sofa_menu())
    else:
        # иначе показываем товары
        await show_products(callback.message, data)

# ========== кнопка назад ==========


@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    history = user_history.get(user_id, ["main"])
    if len(history) > 1:
        history.pop()
    prev = history[-1]

    if prev == "main":
        await callback.message.edit_text("Главное меню:", reply_markup=main_menu())
    elif prev == "bedroom":
        await callback.message.edit_text("Выберите подкатегорию:", reply_markup=bedroom_menu())
    elif prev == "kitchen":
        await callback.message.edit_text("Выберите подкатегорию:", reply_markup=kitchen_menu())
    elif prev == "sofa":
        await callback.message.edit_text("Выберите подкатегорию:", reply_markup=sofa_menu())
    else:
        await show_products(callback.message, prev)

# ========== показать товары ==========


async def show_products(message: Message, category: str):
    items = PRODUCTS.get(category)
    if not items:
        await message.answer("Товары не найдены.", reply_markup=main_menu())
        return

    for item in items:
        if len(item["images"]) > 1:
            media = [InputMediaPhoto(media=url) for url in item["images"]]
            await message.answer_media_group(media)
            await message.answer(f"{item['name']}\n{item['description']}\nСтрана: {item['country']}\nЦена: {item.get('price','-')}", reply_markup=product_buttons(item["name"]))
        else:
            await message.answer_photo(photo=item["images"][0],
                                       caption=f"{item['name']}\n{item['description']}\nСтрана: {item['country']}\nЦена: {item.get('price','-')}",
                                       reply_markup=product_buttons(item["name"]))

# ========== оформление заказа ==========


@router.callback_query(F.data.startswith("order_"))
async def order_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    product_name = callback.data.replace("order_", "")
    await state.update_data(product=product_name)
    await state.set_state(OrderState.waiting_name)
    await callback.message.answer(f"Оформление заказа на {product_name}. Введите имя:")


@router.message(OrderState.waiting_name)
async def order_get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(OrderState.waiting_phone)
    await message.answer("Введите номер телефона:")


@router.message(OrderState.waiting_phone)
async def order_get_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    if not phone.replace("+", "").isdigit():
        await message.answer("Телефон должен содержать только цифры. Введите ещё раз:")
        return
    await state.update_data(phone=phone)
    await state.set_state(OrderState.waiting_comment)
    await message.answer("Комментарий (или /skip):")


@router.message(OrderState.waiting_comment)
async def order_get_comment(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    await finish_order(message, state)


@router.message(F.text == "/skip", OrderState.waiting_comment)
async def skip_comment(message: Message, state: FSMContext):
    await state.update_data(comment="-")
    await finish_order(message, state)


async def finish_order(message: Message, state: FSMContext):
    data = await state.get_data()
    text = f"Новый заказ:\nИмя: {data['name']}\nТелефон: {data['phone']}\nТовар: {data['product']}\nКомментарий: {data['comment']}"
    await message.answer("Спасибо. Ваш заказ отправлен.")
    await message.bot.send_message(-1001234567890, text)
    await state.clear()


# ========== задать вопрос ==========
@router.callback_query(F.data.startswith("ask_"))
async def ask_question(callback: CallbackQuery):
    await callback.answer()
    product_name = callback.data.replace("ask_", "")
    await callback.message.answer(f"Вы выбрали 'Задать вопрос' по товару {product_name}. Введите ваш вопрос:")

# ========== заказать консультацию ==========


@router.callback_query(F.data.startswith("consult_"))
async def order_consult(callback: CallbackQuery):
    await callback.answer()
    product_name = callback.data.replace("consult_", "")
    await callback.message.answer(f"Вы выбрали 'Заказать консультацию' по товару {product_name}. Мы свяжемся с вами в ближайшее время.")