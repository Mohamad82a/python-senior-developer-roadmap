# 🏗️ Capstone Project — FastAPI Production Backend

This README walks you **step-by-step** through building, running, and testing the Capstone FastAPI backend.  
It explains **which file to create first**, why each file exists, and how to run the app both locally and with Docker.  

> 🚀 This project demonstrates a production-ready backend with **JWT authentication**, **async SQLAlchemy**, **Redis caching**, **background tasks**, **pytest testing**, and **Docker Compose orchestration**.

---

## 📚 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Step-by-Step File Creation](#step-by-step)
4. [Local Development Setup](#local-dev)
5. [Run with Docker Compose](#docker)
6. [Testing](#tests)
7. [Environment Variables](#env)
8. [Troubleshooting](#notes)
9. [Next Steps](#next-steps)

---

## 🧰 Prerequisites <a name="prerequisites"></a>

- Python **3.10+** (3.11 recommended)  
- `pip` and `venv`  
- (Optional) Docker & Docker Compose  
- (Optional) Redis and PostgreSQL if running outside Docker  

---

## 🗂️ Project Structure <a name="project-structure"></a>
```text
capstone-backend/
│
├── app/
│ ├── init.py
│ ├── main.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ ├── auth.py
│ ├── cache.py
│ ├── background.py
│ └── deps.py
│
├── tests/
│ ├── conftest.py
│ ├── test_auth.py
│ └── test_users.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## 🪜 Step-by-Step File Creation <a name="step-by-step"></a>
---
## 1️⃣ Create and activate your virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate    # Windows
```
---

## 2️⃣ Create requirements.txt

```text
fastapi
uvicorn[standard]
SQLAlchemy==2.0.20
asyncpg
aiosqlite
python-dotenv
python-jose
passlib[bcrypt]
redis
httpx
aiofiles
pytest
pytest-asyncio
```

Install with:

```bash
pip install -r requirements.txt
```
---

## 3️⃣ Create .env

```ini
DATABASE_URL=sqlite+aiosqlite:///./dev.db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_DEBUG=true
```

---
Copy to .env and modify before running.

---

## 4️⃣ Create database connection — app/database.py

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./dev.db")

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

---

## 5️⃣ Define ORM models — app/models.py

```python
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner = relationship("User", back_populates="posts")
```

---

## 6️⃣ Define schemas — app/schemas.py

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

---

## 7️⃣ CRUD operations — app/crud.py

```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from . import models, schemas

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd.hash(password)

def verify_password(plain: str, hashed: str):
    return pwd.verify(plain, hashed)

async def get_user_by_email(db: AsyncSession, email: str):
    q = select(models.User).where(models.User.email == email)
    res = await db.execute(q)
    return res.scalars().first()

async def create_user(db: AsyncSession, u: schemas.UserCreate):
    hashed = get_password_hash(u.password)
    user = models.User(email=u.email, hashed_password=hashed, full_name=u.full_name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
```

---

## 8️⃣ Authentication — app/auth.py

```python
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db
from .crud import get_user_by_email
from dotenv import load_dotenv

load_dotenv()
SECRET = os.getenv("JWT_SECRET", "change-this")
ALGO = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=EXPIRE_MIN))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGO)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    cred_exc = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        email: str = payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc
    user = await get_user_by_email(db, email)
    if not user:
        raise cred_exc
    return user
```

---

## 9️⃣ Create the main app — app/main.py

```python
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from . import database, models, schemas, crud, auth, background
from .database import engine

app = FastAPI(title="Capstone FastAPI Backend")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    user = await crud.get_user_by_email(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = auth.create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.UserRead)
async def create_user(user_in: schemas.UserCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(database.get_db)):
    user = await crud.create_user(db, user_in)
    background_tasks.add_task(background.send_welcome_email, user.email)
    return user
```

---

## 🧑‍💻 Local Development <a name="local-dev"></a>
1.Create .env from .env.example.

2.Install dependencies:
```bash
pip install -r requirements.txt
```

3.Run Redis (optional):
```bash
redis-server
```

4.Run the app:
```bash
uvicorn app.main:app --reload
```

5.Visit Swagger UI:
👉 http://127.0.0.1:8000/docs

---

## 🐳 Run with Docker Compose <a name="docker"></a>
```bash
docker-compose up --build
```

API → http://localhost:8000

Swagger → http://localhost:8000/docs

Postgres + Redis run automatically.

---

## 🧪 Run Tests <a name="tests"></a>
```bash
pytest -v
```

Use pytest-asyncio for async tests, and httpx.AsyncClient for integration testing.

---

## ⚙️ Environment Variables <a name="env"></a>
Example .env:

```ini
DATABASE_URL=sqlite+aiosqlite:///./dev.db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=mysecretkey
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
APP_DEBUG=true
```

---
## 🧩 Troubleshooting <a name="notes"></a>
Issue	Possible Fix
DB tables not created	Check @app.on_event("startup") in main.py
JWT decode error	Ensure same secret & algorithm used
Redis connection refused	Run Redis or comment out cache imports
Slow responses	Avoid blocking I/O (use async properly)
422 validation errors	Check schema types and request body format

---

## 🚀 Next Steps <a name="next-steps"></a>
Add Alembic for migrations

Use Celery or RQ for async tasks

Add role-based auth

Setup GitHub Actions CI

Integrate logging, CORS, and rate limiting

---

## Author: 🧑‍💻 Senior Python Developer Roadmap — Capstone Project
## Tech stack: FastAPI · SQLAlchemy · PostgreSQL · Redis · JWT · Docker · Pytest

