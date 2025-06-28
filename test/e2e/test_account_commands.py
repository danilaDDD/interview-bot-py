
from unittest.mock import Mock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Chat
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.router.account import start_command, process_email
from .conftest import message, db, state

WAITED_EMAIL_STATE = "RegistrationState:waiting_for_email"

async def get_account_by_chat_id(session: AsyncSession, chat_id: int):
    result = await session.execute(
        select(Account).where(Account.chat_id == chat_id)
    )
    return result.scalar_one_or_none()

class TestStartCommand:
    EMAIL_INPUT_MSG = "Пожалуйста, введите ваш email:"
    ALREADY_REGISTERED_MSG = "Вы уже зарегистрированы!"

    @pytest.mark.asyncio
    async def test_with_not_exist_account(self, message: Message | Mock, state: FSMContext | Mock,
                                          db: AsyncSession):
        await start_command(message, state, db)

        state.set_state.assert_awaited_once_with(WAITED_EMAIL_STATE)
        message.answer.assert_awaited_once_with(self.EMAIL_INPUT_MSG)

    @pytest.mark.asyncio
    async def test_with_exist_account(self, message: Message, state: FSMContext,
                                      db: AsyncSession, current_chat: Chat):
        account = Account(chat_id=current_chat.id, email="test@test.ru",
                          first_name="test",
                          last_name="test")
        db.add(account)
        await db.commit()

        await start_command(message, state, db)

        message.answer.assert_awaited_once_with(self.ALREADY_REGISTERED_MSG)


class TestProcessEmailCommand:
    @pytest.fixture(autouse=True)
    def setup(self, state):
        state.state = WAITED_EMAIL_STATE
        yield

    @pytest.mark.asyncio
    async def test_input_valid_email(self, message, state,
                                     db: AsyncSession, current_chat, current_user):
        message.text = "test@test.com"

        await process_email(message, state, db)

        state.clear.assert_awaited_once()
        message.answer.assert_awaited_once_with("Регистрация успешно завершена!")

        account = await get_account_by_chat_id(db, current_chat.id)

        assert account is not None
        assert account.chat_id == current_chat.id
        assert account.first_name == current_user.first_name
        assert account.last_name == current_user.last_name
        assert account.email == message.text
        assert account.username == current_user.username







