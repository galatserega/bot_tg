from config import PRICES
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    """Головне меню з відображенням ціни."""
    # Формуємо кнопки для кожного напою
    buttons = [KeyboardButton(text=f"{item} - {price}₴") for item, price in PRICES.items()]

    # Розділяємо кнопки на рядки по 2 елементи
    keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    # Додаємо статичні кнопки
    # Додаємо кнопку "🛒 Кошик" на окремий рядок, займаючи всю ширину клавіатури
    keyboard.append([KeyboardButton(text="🛒 Кошик")])

    # Додаємо кнопку "ℹ️ Допомога" на окремий рядок
    keyboard.append([KeyboardButton(text="ℹ️ Допомога")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


# Створюємо клавіатуру з варіантами оплати
def payment_options_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Оплата готівкою")],
            [KeyboardButton(text="Оплата через IBAN")]
        ],
        resize_keyboard=True  # Зменшує кнопки для зручності
    )
    return keyboard


