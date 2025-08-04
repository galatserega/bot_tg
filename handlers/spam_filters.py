import os
from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Ключевые слова спама
BAD_WORDS = ['http', 'https', 'freeether',
             'airdrop', 'wallet', 'click', 'connect', 'Jetacash', 'jetacash', 'bonus', 'deposit']


ADMIN_ID = int(os.getenv('ADMIN_ID'))


@router.message(F.text)
async def filter_spam(message: Message):
    text = message.text.lower()
    if any(bad_word in text for bad_word in BAD_WORDS):
        await message.delete()
        return
