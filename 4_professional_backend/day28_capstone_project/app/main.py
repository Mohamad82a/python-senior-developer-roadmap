from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import json


from . import models, schemas, crud, auth, cache, background
from .database import engine, Base, get_db


app = FastAPI(title='Capstone FastAPI Backend')

# Create database table at startup
@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



# --- Use OAuth2PasswordRequestForm to accept form data (username & password) ---
@app.post('/token', response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.authenticate_user(db, form_data.username, form_data.password)
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = auth.create_access_token(data={"sub": user.email})
    return {'access_token': access_token, 'token_type': 'bearer'}


# --- Register new user ---
@app.post('/user/register', response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: schemas.UserCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    existing_user = await crud.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = await crud.create_user(db, user_in)
    # schedule background welcome email (sync simulation)
    background_tasks.add_task(background.send_welcome_email, user.email)

    await cache.set_cached_user(user.id, json.dumps({'id': user.id, 'email': user.email, 'full_name': user.full_name}), expire=300) # expire in seconds (equals to 10 minutes)
    return user



# Displays current user
@app.get('/users/me', response_model=schemas.UserRead)
async def read_user(current_user = Depends(auth.get_current_user)):
    return current_user


# List users
@app.get('/users', response_model=List[schemas.UserRead])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


# Get user by id with cache check
@app.get('/users/{user_id}', response_model=schemas.UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    # check cache first
    cached = await cache.get_cached_user(user_id)
    if cached:
        data = json.loads(cached)
        return data

    user = await crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # set cache user
    await cache.set_cached_user(user_id, json.dumps({'id': user.id, 'email': user.email, 'full_name': user.full_name}), expire=300)
    return user