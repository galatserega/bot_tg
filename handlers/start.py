from aiogram import Router, F, types
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from config import PRICES, OrderState, ADMIN_ID, IBAN
from keyboards.keyboards import main_menu, payment_options_keyboard
import re
from datetime import datetime

router = Router()

USER_CART = {}

PHONE_REGEX = r"^0\d{9}$"
WORKING_HOURS = (8, 16)


@router.message(F.text == "/start")
async def start_command(message: Message, state: FSMContext):
    """Обробник команди /start."""
    current_time = datetime.now().hour
    current_day = datetime.now().weekday()
    if current_time < WORKING_HOURS[0] or current_time > WORKING_HOURS[1] or current_day in (5, 6):
        await message.answer("Вибачте, зараз замовлення недоступне. Графік роботи з 8 ранку до 16 години.")
        return

    await state.set_state(OrderState.waiting_for_coffee)
    await message.answer(
        "Ласкаво просимо!\nОберіть каву з меню нижче:\n"
        "Прошу звернути увагу, що безкоштовна доставка буде при замовленні від 150 грн. Дякую за розуміння.",
        reply_markup=main_menu()
    )
    # Ініціалізуємо кошик для користувача
    USER_CART[message.from_user.id] = {"items": {}, "total": 0}


@router.message(OrderState.waiting_for_coffee)
async def select_coffee(message: Message, state: FSMContext):
    """Обробник вибору кави."""
    user_id = message.from_user.id
    selected_item = message.text.strip()

    # Приводимо вибраний елемент до точного формату
    for item in PRICES.keys():
        if item.strip() == selected_item.split(" - ")[0].strip():
            selected_item = item
            break

    # Перевіряємо, що користувач обрав каву з меню
    if selected_item in PRICES:
        price = PRICES[selected_item]

        # Додаємо або оновлюємо елемент у кошику
        if selected_item in USER_CART[user_id]["items"]:
            USER_CART[user_id]["items"][selected_item]["quantity"] += 1
        else:
            USER_CART[user_id]["items"][selected_item] = {"price": price, "quantity": 1}

        USER_CART[user_id]["total"] += price

        await message.answer(
            f"Додано в кошик: {selected_item} ({USER_CART[user_id]['items'][selected_item]['quantity']} шт.)"
        )

    elif selected_item == "🛒 Кошик":
        # Показати вміст кошика
        cart = USER_CART.get(user_id, {"items": {}, "total": 0})
        if cart["items"]:
            cart_contents = "\n".join(
                [f"{name} - {details['price']}₴ x {details['quantity']}"
                 for name, details in cart["items"].items()]
            )
            total = cart["total"]
            await message.answer(
                f"Ваше замовлення:\n{cart_contents}\n\nРазом: {total}₴"
            )

            # Переходимо до вибору способу оплати
            await state.set_state(OrderState.waiting_for_payment)
            await message.answer(
                "Оберіть спосіб оплати:",
                reply_markup=payment_options_keyboard()  # Додаємо варіанти оплати
            )
        else:
            await message.answer("Ваш кошик порожній.")

    elif selected_item == "ℹ️ Допомога":
        await message.answer("Оберіть каву з меню або відкрийте кошик 🛒.")
    else:
        await message.answer("Будь ласка, оберіть доступний варіант із меню.")


@router.message(OrderState.waiting_for_payment)
async def process_payment(message: Message, state: FSMContext):
    """Обробник вибору способу оплати."""
    user_id = message.from_user.id
    payment_method = message.text.strip()

    if payment_method == "Оплата готівкою":
        # Підтвердження оплати готівкою
        await state.update_data(payment_method="Готівка")
        await message.answer(
            "Дякую! Ваше замовлення буде оброблено найближчим часом.",
            reply_markup=ReplyKeyboardRemove()  # Видаляємо меню
        )
        # Переходимо до наступного кроку
        await state.set_state(OrderState.waiting_for_address)
        await message.answer(
            "Напишіть номер телефону в форматі: 0ХХХХХХХХХ для підтвердження замовлення та умов доставки:"
        )

    elif payment_method == "Оплата через IBAN":
        # Відправка IBAN і інструкцій
        await state.update_data(payment_method="IBAN")
        iban_number = IBAN  # Замініть на свій реальний номер IBAN
        await message.answer(
            f"Ваш IBAN для оплати:\n`{iban_number}`\n\n"
            "Скопіюйте номер IBAN та здійсніть оплату. Після цього введіть номер телефону в форматі 0XXXXXXXXX для підтвердження замовлення.",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(OrderState.waiting_for_address)

    else:
        await message.answer("Будь ласка, оберіть доступний спосіб оплати.")


@router.message(OrderState.waiting_for_address)
async def process_address(message: Message, state: FSMContext):
    """Обробник отримання адреси доставки."""
    user_id = message.from_user.id
    phone = message.text.strip()

    # Регулярний вираз для перевірки телефонного номера (наприклад, 0XXXXXXXXX)


    # Перевіряємо, чи номер телефону відповідає формату
    if not re.match(PHONE_REGEX, phone):
        await message.answer(
            "Будь ласка, введіть правильний номер телефону у форматі: 0XXXXXXXXX"
        )
        return

    # Завершення замовлення
    await message.answer(
        "Дякую! Найближчим часом ми зателефонуємо Вам для підтвердження замовлення.",
        reply_markup=ReplyKeyboardRemove()
    )

    # Отримуємо кошик
    cart = USER_CART[user_id]
    cart_contents = "\n".join(
        [f"{name} - {details['price']} грн x {details['quantity']}"
         for name, details in cart["items"].items()]
    )
    total = cart["total"]

    data = await state.get_data()
    payment_method = data.get("payment_method", "Не вказано")

    admin_message = (
        f"Нове замовлення від клієнта @{message.from_user.username} (ID: {user_id}):\n\n"
        f"Метод оплати: {payment_method}\n\n"
        f"{cart_contents}\n\nРазом: {total} грн\n"
        f"Телефон для зв'язку: {phone}"
    )

    # Надсилаємо адміністратору замовлення
    await message.bot.send_message(chat_id=ADMIN_ID, text=admin_message)

    # Очищуємо стан та кошик
    await state.clear()
    USER_CART.pop(user_id, None)
