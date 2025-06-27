import asyncio

from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message

from app.setting.logging import *
from aiogram.filters import Command

from app.setting.setting import load_settings

setting = load_settings()

bot = Bot(token=setting.BOT_TOKEN)
dp = Dispatcher()

router = Router()

@router.message(Command('start'))
async def start_command(message: Message):
    await message.answer("Welcome to Interview48 Bot! How can I assist you today?")

@router.message(Command('echo'))
async def echo_command(message: Message):
    await message.answer(f"You said: {message.text.replace('/echo', '').strip()}")

@router.message(F.text)
async def text_message_handler(message: Message):
    await message.answer("Unknown command or message. Please use /start or /echo.")

async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, )

if __name__ == '__main__':
    asyncio.run(main())