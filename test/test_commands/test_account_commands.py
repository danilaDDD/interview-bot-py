import pytest
import pytest_asyncio
from aiogram.types import Message, Chat
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.router.account import (RegistrationState, start_command, process_email,
                                ALREADY_REGISTERED_MSG, WAITED_EMAIL_MSG,
                                SUCCESS_REGISTRATION_MSG, INPUT_EMAIL_ERROR_MSG)
from .conftest import message, db, state
from .mock import MockFSMContext

async def get_account_by_chat_id(session: AsyncSession, chat_id: int):
    result = await session.execute(
        select(Account).where(Account.chat_id == chat_id)
    )
    return result.scalar_one_or_none()

class TestStartCommand:

    @pytest.mark.asyncio
    async def test_with_not_exist_account(self, message: Message, state: MockFSMContext,
                                          db: AsyncSession):
        await start_command(message, state, db)

        assert state.state == RegistrationState.waiting_for_email
        message.answer.assert_awaited_once_with(WAITED_EMAIL_MSG)

    @pytest.mark.asyncio
    async def test_with_exist_account(self, message: Message, state: MockFSMContext,
                                      db: AsyncSession, current_chat: Chat):
        account = Account(chat_id=current_chat.id, email="test@test.ru",
                          first_name="test",
                          last_name="test")
        db.add(account)
        await db.commit()

        await start_command(message, state, db)

        message.answer.assert_awaited_once_with(ALREADY_REGISTERED_MSG)
        assert state.is_clear_state()


class TestProcessEmailCommand:
    @pytest_asyncio.fixture
    async def state(self, state: MockFSMContext) -> MockFSMContext:
        state = MockFSMContext()
        await state.set_state(RegistrationState.waiting_for_email)
        return state

    async def wrap_process_email(self, message: Message, state: MockFSMContext, db: AsyncSession):
        if state.state == RegistrationState.waiting_for_email:
            await process_email(message, state, db)

    @pytest.mark.asyncio
    async def test_input_valid_email(self, message, state,
                                     db: AsyncSession, current_chat, current_user):
        message.text = "test@test.com"

        await self.wrap_process_email(message, state, db)

        assert state.is_clear_state()
        message.answer.assert_awaited_once_with(SUCCESS_REGISTRATION_MSG)

        account = await get_account_by_chat_id(db, current_chat.id)

        assert account is not None
        assert account.chat_id == current_chat.id
        assert account.first_name == current_user.first_name
        assert account.last_name == current_user.last_name
        assert account.email == message.text
        assert account.username == current_user.username


    @pytest.mark.asyncio
    async def test_input_invalid_email(self, message, state,
                                       db: AsyncSession):
        message.text = "invalid-email"

        await self.wrap_process_email(message, state, db)

        assert state.state == RegistrationState.waiting_for_email
        message.answer.assert_awaited_once_with(INPUT_EMAIL_ERROR_MSG)


    @pytest.mark.asyncio
    async def test_repeated_input_invalid_email(self, message, state,
                                       db: AsyncSession):
        invalid_emails = ["invalid-email", "another-invalid-email", "test@.com", "1123@com", ""]

        for email in invalid_emails:
            message.text = email
            await self.wrap_process_email(message, state, db)

        assert state.state == RegistrationState.waiting_for_email
        assert message.answer.call_count == len(invalid_emails)
        for call_args in message.answer.await_args_list:
            assert call_args[0][0] == INPUT_EMAIL_ERROR_MSG


    @pytest.mark.asyncio
    async def test_different_input(self, message, state,
                                       db: AsyncSession, current_chat, current_user):
        inputs = ["invalid", "invalid2", "test@test.ru", ]

        for input_text in inputs:
            message.text = input_text
            await self.wrap_process_email(message, state, db)

        assert state.is_clear_state()

        expected_msgs = [INPUT_EMAIL_ERROR_MSG, INPUT_EMAIL_ERROR_MSG, SUCCESS_REGISTRATION_MSG]
        assert message.answer.call_count == len(inputs)
        for call_args, expected in zip(message.answer.await_args_list, expected_msgs):
            assert call_args[0][0] == expected

        account = await get_account_by_chat_id(db, current_chat.id)
        assert account is not None
        assert account.chat_id == current_chat.id







