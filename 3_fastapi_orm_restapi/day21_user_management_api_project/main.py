from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from . import models, database

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post('/users/create')
async def create_user(name: str, age: int, db: AsyncSession = Depends(database.get_db)):
    user = models.User(name=name, age=age)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'message': 'User created successfully!', 'user': user}

@app.get('/users')
async def get_users(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


@app.get('/users/{user_id}')
async def get_user(user_id: int, db:AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete('/users/{user_id}')
async def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {'message': 'User deleted successfully!'}
