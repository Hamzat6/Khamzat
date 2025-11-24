from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    kb = [
        [InlineKeyboardButton(text="Спальная мебель", callback_data="category_bedroom")],
        [InlineKeyboardButton(text="Кухонная мебель", callback_data="category_kitchen")],
        [InlineKeyboardButton(text="Мягкая мебель", callback_data="category_sofa")],
        [InlineKeyboardButton(text="Столы и стулья", callback_data="category_tables")],
        [InlineKeyboardButton(text="Тумбы и комоды", callback_data="category_chests")],
        [InlineKeyboardButton(text="Матрасы", callback_data="category_mattresses")],
        [InlineKeyboardButton(text="Шкафы", callback_data="category_wardrobes")],
        [InlineKeyboardButton(text="О компании / Контакты", callback_data="about")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def bedroom_menu():
    kb = [
        [InlineKeyboardButton(text="Российская", callback_data="category_bedroom_russian")],
        [InlineKeyboardButton(text="Турецкая", callback_data="category_bedroom_turkish")],
        [InlineKeyboardButton(text="Кровати", callback_data="category_bedroom_beds")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def kitchen_menu():
    kb = [
        [InlineKeyboardButton(text="Прямая", callback_data="category_kitchen_straight")],
        [InlineKeyboardButton(text="Угловая", callback_data="category_kitchen_corner")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def sofa_menu():
    kb = [
        [InlineKeyboardButton(text="Российская", callback_data="category_sofa_russian")],
        [InlineKeyboardButton(text="Турецкая", callback_data="category_sofa_turkish")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def product_buttons(product_name: str):
    kb = [
        [InlineKeyboardButton(text="Задать вопрос", callback_data=f"ask_{product_name}")],
        [InlineKeyboardButton(text="Заказать консультацию", callback_data=f"consult_{product_name}")],
        [InlineKeyboardButton(text="Оформить заказ", callback_data=f"order_{product_name}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
