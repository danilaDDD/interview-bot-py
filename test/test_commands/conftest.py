from unittest.mock import Mock, AsyncMock, PropertyMock

import pytest
import pytest_asyncio
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Chat, User
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.models.account import Account
from app.setting.initial import dp
from test.test_commands.mock import MockFSMContext


@pytest.fixture(scope="session")
def current_chat() -> Chat:
    return Chat(id=123456789, type="private", title="Test Chat", username="test_chat")

@pytest.fixture(scope="session")
def current_user() -> User:
    return User(id=987654321, is_bot=False, first_name="Test", last_name="User", username="test_user")

@pytest.fixture
def message(current_chat: Chat, current_user) -> Message:
    mock = Mock(spec=Message)
    mock.answer = AsyncMock()
    mock.text = PropertyMock(spec=str)
    mock.from_user = current_user
    mock.chat = current_chat

    return mock

async def clean_database(db: AsyncSession):
    await db.execute(delete(Account))
    await db.commit()


@pytest_asyncio.fixture
async def db(test_settings):
    engine = create_async_engine(test_settings.get_database_url(), echo=True)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False, )

    async with async_session_maker() as session:
        await clean_database(session)
        yield session


@pytest.fixture
def state() -> MockFSMContext:
    return MockFSMContext()

