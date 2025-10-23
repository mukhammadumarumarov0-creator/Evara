from aiogram import Bot
from decouple import config

BOT_TOKEN=config('BOT_TOKEN')
ADMIN_ID=config('ADMIN_ID')


async def send_message(text):
    bot=Bot(token=BOT_TOKEN)
    await bot.send_message(ADMIN_ID,text,parse_mode="html")
    bot.close()