from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.database.models.user import User
from backend.app.database.schemas.user import UserCreate, UserUpdate

class UserCrud:
    """User 관련 CRUD"""

    @staticmethod
    async def get_id(db: AsyncSession, user_id: int) -> User | None:
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user: UserCreate) -> User:
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.flush()  # commit은 호출하는 쪽에서
        return db_user

    @staticmethod
    async def delete_by_id(db: AsyncSession, user_id: int):
        db_user = await db.get(User, user_id)
        if db_user:
            db.delete(db_user)  # AsyncSession.delete는 동기 메서드
            await db.flush()
            return db_user
        return None

    @staticmethod
    async def get_username(db: AsyncSession, username: str):
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_email(db: AsyncSession, email: str):
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_by_id(db: AsyncSession, user_id: int, user: UserUpdate):
        db_user = await db.get(User, user_id)
        if db_user:
            update_data = user.model_dump(exclude_unset=True)
            for k, v in update_data.items():
                setattr(db_user, k, v)
            await db.flush()
            return db_user
        return None

    @staticmethod
    async def update_refresh_token_id(db: AsyncSession, user_id: int, refresh_token: str):
        db_user = await db.get(User, user_id)
        if db_user:
            db_user.refresh_token = refresh_token
            await db.flush()
        return db_user

    @staticmethod
    async def delete_refresh_token(db: AsyncSession, refresh_token: str):
        result = await db.execute(select(User).where(User.refresh_token == refresh_token))
        db_user = result.scalar_one_or_none()
        if db_user:
            db_user.refresh_token = None
            await db.flush()
        return db_user
