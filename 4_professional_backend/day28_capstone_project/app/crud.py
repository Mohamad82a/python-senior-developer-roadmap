# Database operations for User model

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_email(db: AsyncSession, email:str):
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id:int):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: schemas.UserCreate):
    hashed_password = get_password_hash(user_in.password)
    user = models.User(email=user_in.email, hashed_password=hashed_password, full_name=user_in.full_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(db: AsyncSession, email:str, password:str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def deactivate_user(db: AsyncSession, user_id:int):
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    user.is_active = False
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user