import os

import pytest

from app.setting.setting import load_settings


@pytest.fixture(scope='session')
def test_settings() -> 'Settings':
    os.environ['ENV'] = 'test'
    return load_settings()