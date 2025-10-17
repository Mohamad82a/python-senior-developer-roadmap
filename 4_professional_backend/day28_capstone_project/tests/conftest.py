import asyncio
import os
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from app.main import app
from app.database import Base, get_db
from app import models

DATABASE_URL = os.getenv("DATABASE_URL")

# create separate engine for tests
engine_test = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocalTest = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

# override the get_db dependency to use test DB
async def override_get_db():
    async with SessionLocalTest() as session:
        yield session


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
async def client(monkeypatch):
    monkeypatch.setattr('app.database.SessionLocal', SessionLocalTest)
    monkeypatch.setattr('app.database.engine', engine_test)
    monkeypatch.setattr('app.database.get_db', override_get_db)

    async with AsyncClient(app=app, base_url='http://testserver') as async_connection:
        yield async_connection