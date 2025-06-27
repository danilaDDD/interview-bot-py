from unittest.mock import Mock, call

import pytest
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.router.account import start_command
from .conftest import mock_message, db


class TestCommands:
    HELLO_MESSAGE = "Welcome to Interview48 Bot! How can I assist you today?"

    @pytest.mark.asyncio
    async def test_start_command(self, mock_message: Mock, db: AsyncSession):
        await start_command(mock_message, db)
        mock_message.answer.assert_awaited_with(self.HELLO_MESSAGE)


