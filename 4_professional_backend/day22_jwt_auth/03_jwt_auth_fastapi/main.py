from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import os

from watchfiles import awatch

from . import models, database

app = FastAPI()

SECRET_KEY ='super-secret'
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@app.on_event("startup")
async def on_startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.post('/users/create')
async def create_user(username: str, password: str, db: AsyncSession = Depends(database.get_db)):
    user = models.User(username=username, password=password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'message': 'User created successfully!', 'user': user}


def create_access_token(data:dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta is None:
        expires_delta = timedelta(minutes=10)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(models.User).where(models.User.username == username))
    return result.scalar_one_or_none()

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    user = await get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token(data={"sub": user.username })
    return {'access_token': token, 'token_type': 'bearer'}

@app.get('/users/me')
def read_me(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {'user': payload.get('sub')}
    except JWTError:
        raise HTTPException(status_code=401, detail="Incorrect token")

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



