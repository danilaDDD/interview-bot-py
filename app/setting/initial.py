from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from app.setting.middleware import SessionMiddleware, LoggingMiddleware
from app.setting.setting import load_settings

settings = load_settings()

engine = create_async_engine(settings.get_database_url(), echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, )

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()

dp.update.middleware(SessionMiddleware(async_session_maker))
dp.update.middleware(LoggingMiddleware())