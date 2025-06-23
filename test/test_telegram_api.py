import asyncio
import time
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from app.setting.setting import Settings
from .conftest import *

BOT_NAME = "@Interview2015Bot"
USER_ID = 861230357
PHONE = "+79113874810"
CALLBACK_CODE = 34450

class TestTelegramClient:
    @pytest_asyncio.fixture
    async def client(self, test_settings):
        client = TelegramClient('user',
                                int(test_settings.TEST_API_ID),
                                test_settings.TEST_API_HASH)
        client.session.set_dc(2, '149.154.167.40', 443)
        await asyncio.sleep(1)
        try:
            await client.start(phone=PHONE)
            yield client
        finally:
            if client.is_connected():
                await client.disconnect()


    def test_connection_client(self, client: TelegramClient):
        assert client.is_connected()

    @pytest.mark.asyncio
    async def test_start_command(self, client: TelegramClient):
        await client.send_message(BOT_NAME, "hellow")
        resp = await client.get_response()

        assert resp.text == "Unknown command or message. Please use /start or /echo."











