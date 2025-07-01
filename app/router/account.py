from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.schema import EmailSchema
from app.service.account import AccountService

account_router = Router()

class RegistrationState(StatesGroup):
    waiting_for_email = State()

ALREADY_REGISTERED_MSG = "Вы уже зарегистрированы!"
WAITED_EMAIL_MSG = "Пожалуйста, введите ваш email:"

@account_router.message(Command("start"))
async def start_command(message: Message, state: FSMContext, db: AsyncSession):
    account = await AccountService.get_account_by_chat_id(db, message.chat.id)

    if account:
        await message.answer(ALREADY_REGISTERED_MSG)
        return

    await state.set_state(RegistrationState.waiting_for_email)
    await message.answer(WAITED_EMAIL_MSG)

SUCCESS_REGISTRATION_MSG = "Регистрация успешно завершена!"
INPUT_EMAIL_ERROR_MSG = "Ошибка, пожалуйста, введите корректный email."

@account_router.message(RegistrationState.waiting_for_email)
async def process_email(message: Message, state: FSMContext, db: AsyncSession):
    try:
        email = message.text.strip()
        EmailSchema(email=email)
        account_data = {
            "email": email,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }

        await AccountService.create_account(
            db,
            chat_id=message.chat.id,
            **account_data
        )

        await state.clear()
        await message.answer(SUCCESS_REGISTRATION_MSG)
    except ValueError as e:
        await message.answer(INPUT_EMAIL_ERROR_MSG)
