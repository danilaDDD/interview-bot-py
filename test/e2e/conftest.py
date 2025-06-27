from unittest.mock import Mock, AsyncMock, PropertyMock

import pytest
import pytest_asyncio
from aiogram.types import Message
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.models.account import Account

@pytest.fixture
def mock_message() -> Message:
    mock = Mock(spec=Message)
    mock.answer = AsyncMock()
    mock.text = PropertyMock(spec=str)

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



