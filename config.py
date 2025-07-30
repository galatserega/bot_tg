import os
from dotenv import load_dotenv
from aiogram.fsm.state import State, StatesGroup


load_dotenv()
IBAN = os.getenv('IBAN')
TOKEN = os.getenv("BOT_TOKEN")  # Убедись, что переменная BOT_TOKEN указана в .env
ADMIN_ID = int(os.getenv('ADMIN_ID'))

class OrderState(StatesGroup):
    """Состояния заказа."""
    waiting_for_coffee = State()
    waiting_for_address = State()
    waiting_for_payment = State()


PRICES = {
    "☕ Еспресо": 45,
    "☕ Американо": 50,
    "☕ Капучино": 60,
    "☕ Латте": 65,
    "☕ Допіо": 65,
    "☕ Біг Бос": 90,
    "☕ Флет Уайт": 80,
    "☕ Джміль": 100,
    "☕ Айс лате": 95,
    "☕ Капуоранж": 80,
    'Паніні Максі': 85,
    'Хот-Дог': 75
}
