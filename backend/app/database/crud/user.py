# backend/app/database/crud/user.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.models.user import User  # 모델 경로 통일
from app.database.schemas.user import UserCreate

class UserCrud:

    @staticmethod
    async def get_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.flush()
        return db_user

    @staticmethod
    async def delete_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        db_user = await db.get(User, user_id)
        if db_user:
            await db.delete(db_user)
            await db.flush()
            return db_user
        return None

    @staticmethod
    async def get_username(db: AsyncSession, username: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_by_id(db: AsyncSession, user_id: int, data: dict) -> Optional[User]:
        db_user = await db.get(User, user_id)
        if db_user:
            for k, v in data.items():
                setattr(db_user, k, v)
            await db.flush()
            return db_user
        return None

    @staticmethod
    async def update_refresh_token_id(db: AsyncSession, user_id: int, refresh_token: str) -> Optional[User]:
        db_user = await db.get(User, user_id)
        if db_user:
            db_user.refresh_token = refresh_token
            await db.flush()
        return db_user

    @staticmethod
    async def delete_refresh_token(db: AsyncSession, refresh_token: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.refresh_token == refresh_token))
        db_user = result.scalar_one_or_none()
        if db_user:
            db_user.refresh_token = None
            await db.flush()
        return db_user

    @staticmethod
    async def list(db: AsyncSession, skip: int = 0, limit: int = 50) -> List[User]:
        result = await db.execute(select(User).offset(skip).limit(limit))
        return list(result.scalars().all())
