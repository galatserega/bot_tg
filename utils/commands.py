from aiogram import Bot
from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    """Устанавливаем команды для меню бота."""
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)


