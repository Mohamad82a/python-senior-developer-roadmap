# Pydantic models for requests/responses body

from pydantic import BaseModel, EmailStr
from typing import Optional


# User creation input
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


# User read (response)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True


# Token schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
