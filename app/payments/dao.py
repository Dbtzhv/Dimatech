from sqlalchemy import select

from app.database import async_session
from app.models import Payment, Account
from app.dao.base import BaseDAO


class PaymentDAO(BaseDAO):
    model = Payment

    @classmethod
    async def find_payments_by_user_id(cls, user_id: int):
        async with async_session() as session:
            user_accounts = select(Account.id).filter_by(user_id=user_id)
            result = await session.execute(user_accounts)
            account_ids = result.scalars().all()

            if not account_ids:
                return []

            query = select(cls.model).filter(cls.model.account_id.in_(account_ids))
            result = await session.execute(query)
            return result.scalars().all()
