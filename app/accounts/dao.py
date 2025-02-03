from sqlalchemy import select

from app.database import async_session
from app.models import Account
from app.dao.base import BaseDAO


class AccountDAO(BaseDAO):
    model = Account

    @classmethod
    async def find_accounts_by_user_id(cls, user_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.scalars().all()
