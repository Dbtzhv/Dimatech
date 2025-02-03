from sqlalchemy import select, insert, delete, update

from app.database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_by_id(cls, model_id: int):
        async with async_session() as session:
            query = delete(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            await session.commit()
            return f"{cls.model.__name__} with id {model_id} has been deleted"

    @classmethod
    async def update_by_id(cls, model_id: int, **data):
        data = {k: v for k, v in data.items() if v is not None}
        async with async_session() as session:
            query = update(cls.model).filter_by(id=model_id).values(**data)
            result = await session.execute(query)
            await session.commit()
            return f"{cls.model.__name__} with id {model_id} has been updated"
