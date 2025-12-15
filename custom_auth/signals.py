import asyncio
from telegram import Bot
from django.conf import settings

bot = Bot(settings.BOT_TOKEN)

async def send_code_async(telegram_id, code):
    await bot.send_message(
        chat_id=telegram_id,
        text=f"🔐 Aktivatsiya kodingiz: <code>{code}</code>",
        parse_mode="HTML"
    )

def send_code(telegram_id, code):
    asyncio.run(send_code_async(telegram_id, code))
