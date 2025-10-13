from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine('sqlite+aiosqlite:///async.db')
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

