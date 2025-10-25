# backend/app/database/crud/user.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.user import User  # 모델 경로 통일
from ..schemas.user import UserCreate
from datetime import datetime, timedelta
import random
import string

class UserCrud:

    @staticmethod
    async def get_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    # 회원 roles와 함께 회원 조회
    @staticmethod
    async def get_user_with_role(db: AsyncSession, user_id: int)-> Optional[User]:
        from sqlalchemy.orm import selectinload
        result = await db.execute(select(User).options(selectinload(User.roles)).where(User.user_id == user_id))
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

    # 입력 받은 이메일, 이름, 전화번호가 모두 동일한 유저 조회
    @staticmethod
    async def get_user_by_credentials(db: AsyncSession, email: str, username: str, phone_number: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email, User.username == username, User.phone_number == phone_number)) # 이메일, 이름, 전화번호가 모두 일치하는 유저 조회
        return result.scalar_one_or_none()

    # 6자리 인증코드 생성
    @staticmethod
    def generate_reset_code() -> str:
        return ''.join(random.choices(string.digits, k=6))

    # 인증코드 저장 (User 모델에 필드 추가한 경우)
    @staticmethod
    async def save_reset_code(db: AsyncSession, user_id: int, code: str, expires_minutes: int = 15): # expires_minutes = 15 => 임시 인증 코드의 유효 기간이 15분 이다~
        user = await db.get(User, user_id) # user_id로 유저 조회 후
        if user: # 유저가 존재하면
            user.reset_code = code # 인증코드 저장
            user.reset_code_expires_at = datetime.now() + timedelta(minutes=expires_minutes) # 인증코드 유효 기간 저장
            await db.flush()
        return user

    # 인증코드 검증(유효 기간이 지났는지)
    @staticmethod
    async def verify_reset_code(db: AsyncSession, email: str, code: str) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email, User.reset_code == code, User.reset_code_expires_at > datetime.now()))  # 인증코드 만료 확인(15분이 지났는지)
        return result.scalar_one_or_none()

    # 인증코드 초기화 - 작업이 완료되면 임시로 부여한 인증 코드 값 초기화 => null
    @staticmethod
    async def clear_reset_code(db: AsyncSession, user_id: int):
        user = await db.get(User, user_id) # 해당 유저 정보를 조회
        if user:
            user.reset_code = None # null로 변경
            user.reset_code_expires_at = None # null로 변경
            await db.flush()
        return user