import os

import pytest

from app.setting.setting import load_settings
from test.telegramapi import TelegramRequests


@pytest.fixture(scope='session')
def test_settings() -> 'Settings':
    os.environ['ENV'] = 'test'
    return load_settings()

@pytest.fixture(scope='session')
def telegram_api_client(test_settings):
    return TelegramRequests(test_settings.BOT_TOKEN, 861230357)