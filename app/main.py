import asyncio

from app.setting.setting import load_settings

setting = load_settings()

async def main():
    print(setting.get_database_url())

if __name__ == '__main__':
    asyncio.run(main())