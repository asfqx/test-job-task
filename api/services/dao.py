from api.db.database import async_session_maker
from sqlalchemy import select, insert, desc, update, func, delete
from sqlalchemy.exc import IntegrityError

from api.models.model import MethodNames


class MethodNamesDAO:
    model = MethodNames

    @classmethod
    async def get_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by).limit(1).order_by(desc(cls.model.id))
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**data).returning(cls.model.id)
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one()
            except IntegrityError as e:
                return False

    @classmethod
    async def update(cls, id, **parameters):
        async with async_session_maker() as session:
            try:
                query = update(cls.model).where(cls.model.id == id).values(**parameters).returning(cls.model.id)
                result = await session.execute(query)
                await session.commit()
                return result.mappings().one()
            except Exception as e:
                return False

    @classmethod
    async def get_all(cls, **filters):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters).order_by(desc(cls.model.id))
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def get_paged_all(cls, page, **filters):
        async with async_session_maker() as session:
            query = (select(cls.model)
                     .filter_by(**filters)
                     .limit(20)
                     .offset(
                         page - 1
                         if page == 1
                         else (page - 1) * 20)
                     .order_by(desc(cls.model.id)))
            query_count = select(func.count(cls.model.id)).filter_by(**filters)
            result = await session.execute(query)
            count = await session.execute(query_count)
            return result.mappings().all(), count.mappings().one()

    @classmethod
    async def delete(cls, **filters):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filters)
            await session.execute(query)
            await session.commit()
            return True
