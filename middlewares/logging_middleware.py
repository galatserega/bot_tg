from aiogram.types import TelegramObject

class LoggingMiddleware:
    async def __call__(self, handler, event: TelegramObject, data: dict):
        print(f"Отримано подію: {event}")
        return await handler(event, data)
