from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account


class AccountService:
    @staticmethod
    async def get_account_by_chat_id(session: AsyncSession, chat_id: int):
        result = await session.execute(
            select(Account).where(Account.chat_id == chat_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_account(session: AsyncSession, chat_id: int, **kwargs):
        account = Account(chat_id=str(chat_id), **kwargs)
        session.add(account)
        await session.commit()
        return account