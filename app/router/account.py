from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

account_router = Router()

@account_router.message(Command('start'))
async def start_command(message: Message, db: AsyncSession):
    await message.answer("Welcome to Interview48 Bot! How can I assist you today?")