import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.exc import SQLAlchemyError


class SessionMiddleware(BaseMiddleware):
    session_maker = None

    def __init__(self, session_maker):
        super().__init__()
        self.session_maker = session_maker

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        try:
            async with self.session_maker() as session:
                data['db'] = session
                return await handler(event, data)
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


logger = logging.getLogger('error_logger')

class LoggingMiddleware(BaseMiddleware):
    def __init__(self, ):
        super().__init__()

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"Error in command event {data}: {e}", exc_info=True)
            raise e