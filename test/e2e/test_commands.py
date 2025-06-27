from unittest.mock import Mock, call

import pytest
from aiogram.types import Message
from .conftest import mock_message
from test.conftest import test_settings

from app.main import start_command, echo_command, text_message_handler


class TestCommands:
    @pytest.mark.asyncio
    async def test_start_command(self, mock_message: Mock):
        await start_command(mock_message)
        mock_message.answer.assert_awaited_with("Welcome to Interview48 Bot! How can I assist you today?")

    @pytest.mark.asyncio
    async def test_echo_command(self, mock_message: Mock):
        mock_message.text = "/echo Hello, World!"
        await echo_command(mock_message)
        mock_message.answer.assert_awaited_with("You said: Hello, World!")


