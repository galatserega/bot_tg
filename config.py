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
    "☕ Еспресо": 35,
    "☕ Американо": 40,
    "☕ Капучино": 50,
    "☕ Латте": 55,
    "☕ Допіо": 50,
    "☕ Біг Бос": 70,
    "☕ Флет Уайт": 65,
    "☕ Банановий лате": 85,
    "☕ Кокосовий лате": 85,
    "☕ Капуоранж": 70,
    'Паніні Максі': 70,
    'Хот-Дог': 65
}
