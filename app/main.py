import asyncio

from app.router.account import account_router
from app.setting.initial import dp, bot
from app.setting.logging import *

async def on_startup():
    dp.include_router(account_router)
    await dp.start_polling(bot)

async def main():
    await on_startup()

if __name__ == "__main__":
    asyncio.run(main())


