# Other dependencies for better separation

from fastapi import Depends, HTTPException, status
from .auth import get_current_user
from .database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db_session() -> AsyncSession:
    async for session in get_db():
        yield session


# For protected endpoints
async def current_active_user(user = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user
