from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import async_session
from app.models import User
from app.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def find_users_with_accounts(cls):
        async with async_session() as session:
            query = select(cls.model).options(selectinload(cls.model.accounts))
            result = await session.execute(query)
            return result.scalars().all()

