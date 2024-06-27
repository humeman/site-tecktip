import os
from typing import Any, List, Type, TypeVar
import sqlalchemy
from sqlalchemy import ColumnExpressionArgument, MetaData, Result
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine

class Base(DeclarativeBase):
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Tip(Base):
    __tablename__ = "tips"
    id = sqlalchemy.Column(sqlalchemy.String(40), primary_key = True)
    by = sqlalchemy.Column(sqlalchemy.String(32))
    created = sqlalchemy.Column(sqlalchemy.BigInteger)
    tip = sqlalchemy.Column(sqlalchemy.String(256))

class Image(Base):
    __tablename__ = "images"
    id = sqlalchemy.Column(sqlalchemy.String(40), primary_key = True)
    created = sqlalchemy.Column(sqlalchemy.BigInteger)
    file = sqlalchemy.Column(sqlalchemy.String(128))

class Submission(Base):
    __tablename__ = "submissions"
    id = sqlalchemy.Column(sqlalchemy.String(40), primary_key = True)
    by = sqlalchemy.Column(sqlalchemy.String(32))
    created = sqlalchemy.Column(sqlalchemy.BigInteger)
    tip = sqlalchemy.Column(sqlalchemy.String(256))
    ip = sqlalchemy.Column(sqlalchemy.String(128))

class LegacyKey(Base):
    __tablename__ = "legacy_keys"
    val = sqlalchemy.Column(sqlalchemy.String(64), primary_key = True)

class User(Base):
    __tablename__ = "users"
    val = sqlalchemy.Column(sqlalchemy.String(64), primary_key = True)
    id = sqlalchemy.Column(sqlalchemy.String(64), primary_key = True),
    name = sqlalchemy.Column(sqlalchemy.String(32)),
    email = sqlalchemy.Column(sqlalchemy.String(256)),
    password = sqlalchemy.Column(sqlalchemy.String(256)),
    admin = sqlalchemy.Column(sqlalchemy.Boolean)

T = TypeVar("T", bound = Base)

class Database:
    """
    Handles DB operations for the Teck API™. This is an async
    context manager.

    Before initialization, the following env vars must be set:
        MYSQL_HOST,
        MYSQL_PORT,
        MYSQL_USER,
        MYSQL_PASSWORD,
        MYSQL_DB
    """

    def __init__(self) -> None:
        self._host = os.getenv("MYSQL_HOST")
        self._port = int(os.getenv("MYSQL_PORT"))
        self._user = os.getenv("MYSQL_USER")
        self._password = os.getenv("MYSQL_PASSWORD")
        self._db = os.getenv("MYSQL_DB")

        self._connected = False
        self._ready = False

        self._table_tips = sqlalchemy.Table(
            "tips",
            sqlalchemy.MetaData(),
            sqlalchemy.Column("id", sqlalchemy.String(40), primary_key = True),
            sqlalchemy.Column("by", sqlalchemy.String(32)),
            sqlalchemy.Column("created", sqlalchemy.BigInteger),
            sqlalchemy.Column("tip", sqlalchemy.String(256))
        )
        self._table_images = sqlalchemy.Table(
            "images",
            sqlalchemy.MetaData(),
            sqlalchemy.Column("id", sqlalchemy.String(40), primary_key = True),
            sqlalchemy.Column("created", sqlalchemy.BigInteger),
            sqlalchemy.Column("file", sqlalchemy.String(128))
        )
        self._table_submissions = sqlalchemy.Table(
            "submissions",
            sqlalchemy.MetaData(),
            sqlalchemy.Column("id", sqlalchemy.String(40), primary_key = True),
            sqlalchemy.Column("by", sqlalchemy.String(32)),
            sqlalchemy.Column("created", sqlalchemy.BigInteger),
            sqlalchemy.Column("tip", sqlalchemy.String(256)),
            sqlalchemy.Column("ip", sqlalchemy.String(128))
        )
        self._table_legacy_keys = sqlalchemy.Table(
            "legacy_keys",
            sqlalchemy.MetaData(),
            sqlalchemy.Column("val", sqlalchemy.String(64), primary_key = True)
        )
        self._table_users = sqlalchemy.Table(
            "users",
            sqlalchemy.MetaData(),
            sqlalchemy.Column("id", sqlalchemy.String(64), primary_key = True),
            sqlalchemy.Column("name", sqlalchemy.String(32)),
            sqlalchemy.Column("email", sqlalchemy.String(256)),
            sqlalchemy.Column("password", sqlalchemy.String(256)),
            sqlalchemy.Column("admin", sqlalchemy.Boolean)
        )

    async def random(self, objtype: Type[T]) -> T:
        async with self._session_maker() as session:
            if type(session) != AsyncSession: return # Type hinting sucks
            result = await session.execute(
                sqlalchemy.select(objtype).order_by(sqlalchemy.func.random()).limit(1)
            )
            return result.scalars().first()
        
    async def get(self, objtype: Type[T], where: ColumnExpressionArgument) -> int:
        async with self._session_maker() as session:
            if type(session) != AsyncSession: return
            result = await session.execute(
                sqlalchemy.select(objtype).where(where)
            )
            return result.scalar()

    async def count(self, objtype: Type[T]) -> int:
        async with self._session_maker() as session:
            if type(session) != AsyncSession: return
            result = await session.execute(
                sqlalchemy.select(sqlalchemy.func.count()).select_from(objtype)
            )
            return result.scalar()
        
    async def list_paginated(self, objtype: Type[T], col: sqlalchemy.Column, page: int = 0) -> List[T]:
        async with self._session_maker() as session:
            if type(session) != AsyncSession: return
            result: Result[Any] = await session.execute(
                sqlalchemy.select(objtype).order_by(col).offset(page * 50).limit(50)
            )
            return result.all()
        
    async def list_all(self, objtype: Type[T]) -> List[T]:
        async with self._session_maker() as session:
            if type(session) != AsyncSession: return
            result: Result[Any] = await session.execute(
                sqlalchemy.select(objtype)
            )
            return result.all()
        
    async def upsert(self, obj: T) -> None:
        async with self._session_maker() as session:
            if type(session) != AsyncSession: return
            session.add(obj)
            await session.commit()
        
    async def delete(self, obj: T) -> None:
        async with self._session_maker() as session:
            if type(session) != AsyncSession: return
            await session.delete(obj)
            await session.commit()

    async def __aenter__(self) -> None:
        self._engine = create_async_engine(
            f"mysql+aiomysql://{self._user}:{self._password}@{self._host}:{self._port}/{self._db}"
        )
        self._session_maker = sessionmaker(
            self._engine,
            expire_on_commit = False,
            class_ = AsyncSession
        )
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        self._connected = True

    async def __aexit__(self, *args, **kwargs) -> None:
        self._pool.close()
        await self._pool.wait_closed()
        self._connected = False