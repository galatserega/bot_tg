import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config import TOKEN
from handlers.start import router  # Імпортуємо ваші хендлери

async def main():
    """Основна функція запуску бота."""
    # Створюємо екземпляр бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()

    # Реєструємо всі маршрути (хендлери)
    dp.include_router(router)

    print("Бот запущено!")  # Лог для підтвердження старту

    try:
        # Запускаємо polling
        await dp.start_polling(bot)
    finally:
        # Закриваємо бот при завершенні
        await bot.session.close()

# Перевірка, щоб виконати запуск лише при прямому виклику скрипта
if __name__ == "__main__":
    asyncio.run(main())
