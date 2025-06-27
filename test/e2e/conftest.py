from unittest.mock import Mock, AsyncMock, PropertyMock

import pytest
from aiogram.types import Message


@pytest.fixture
def mock_message() -> Message:
    mock = Mock(spec=Message)
    mock.answer = AsyncMock()
    mock.text = PropertyMock(spec=str)

    return mock

