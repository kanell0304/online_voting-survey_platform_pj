# backend/app/service/user.py
from typing import Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.database.schemas.user import UserCreate, UserLogin, UserUpdate, UserRead
from app.database.crud.user import UserCrud
from app.core.jwt_context import (
    get_pwd_hash,
    verify_pwd,
    create_access_token,
    create_refresh_token,
)

class UserService:
    """User 도메인 서비스 (CRUD + 인증 토큰 발급)"""

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        db_user = await UserCrud.get_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return db_user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int):
        return await UserService.get_user(db, user_id)

    @staticmethod
    async def list_users(db: AsyncSession, skip: int = 0, limit: int = 50) -> List[UserRead]:
        users = await UserCrud.list(db, skip=skip, limit=limit)
        return users

    @staticmethod
    async def register(db: AsyncSession, user: UserCreate):
        if await UserCrud.get_username(db, user.username):
            raise HTTPException(status_code=400, detail="이미 존재하는 사용자명입니다.")
        hashed_pw = await get_pwd_hash(user.password)
        user_create = UserCreate(username=user.username, password=hashed_pw, email=user.email)
        try:
            db_user = await UserCrud.create(db, user_create)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="회원가입 처리 중 오류가 발생했습니다.")

    @staticmethod
    async def login(db: AsyncSession, user: UserLogin) -> Tuple[object, str, str]:
        db_user = await UserCrud.get_email(db, user.email)
        if not db_user or not await verify_pwd(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
        refresh_token = create_refresh_token(db_user.user_id)
        access_token = create_access_token(db_user.user_id)
        try:
            updated_user = await UserCrud.update_refresh_token_id(db, db_user.user_id, refresh_token)
            await db.commit()
            await db.refresh(updated_user)
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="로그인 처리 중 오류가 발생했습니다.")
        return updated_user, access_token, refresh_token

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, payload: UserUpdate):
        # password가 오면 해시로 교체
        data = payload.model_dump(exclude_unset=True)
        if "password" in data and data["password"]:
            data["password"] = await get_pwd_hash(data["password"])
        updated = await UserCrud.update_by_id(db, user_id, data)
        if not updated:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        await db.commit()
        await db.refresh(updated)
        return updated

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        deleted = await UserCrud.delete_by_id(db, user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        await db.commit()
        return True
