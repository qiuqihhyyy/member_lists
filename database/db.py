from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import String,  Integer, Column,  DateTime
from sqlalchemy import func
from sqlalchemy import select, update, delete
import pandas as pd
import sqlite3



database_url = 'sqlite+aiosqlite:///db.sqlite3'
engine = create_async_engine(url=database_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


# базовый класс
class Base(AsyncAttrs, DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class Co_builder(Base):
    __tablename__ = "cobuilders"
    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    AVB_email = Column(String)
    gmail = Column(String)
    post = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'AVB_email': self.AVB_email,
            'gmail': self.gmail,
            'post': self.post,

        }


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **values):
        """
        Асинхронно создает новый экземпляр модели с указанными значениями.

        Аргументы:
            **values: Именованные параметры для создания нового экземпляра модели.

        Возвращает:
            Созданный экземпляр модели.
        """
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)

            return result.scalars().all()


    @classmethod
    async def delete(cls):
        """
                Асинхронно удаляет все экземпляры модели.

                """
        async with async_session_maker() as session:
            async with session.begin():
                stmt = delete(cls.model)
                await session.execute(stmt)
                await session.commit()


class Co_builderDAO(BaseDAO):
    model = Co_builder