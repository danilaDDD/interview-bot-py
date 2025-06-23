import asyncio

from aiogram import Bot, Dispatcher, F
from app.setting.logging import *
from aiogram.filters import Command

from app.setting.setting import load_settings

setting = load_settings()

bot = Bot(token=setting.BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message):
    await message.answer("Welcome to Interview48 Bot! How can I assist you today?")
    await message.answer("Your chat ID is: " + str(message.chat.id))

@dp.message(Command('echo'))
async def echo_command(message):
    await message.answer(f"You said: {message.text.replace('/echo', '').strip()}")

@dp.message(F.text)
async def text_message_handler(message):
    await message.answer("Unknown command or message. Please use /start or /echo.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, )

if __name__ == '__main__':
    asyncio.run(main())