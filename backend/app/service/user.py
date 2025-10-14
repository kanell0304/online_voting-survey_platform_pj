# backend/app/service/user.py
from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from backend.app.database.schemas.user import UserCreate, UserLogin
from backend.app.database.crud.user import UserCrud
from backend.app.core.jwt_context import (
    get_pwd_hash,
    verify_pwd,
    create_access_token,
    create_refresh_token,
)

class UserService:
    """User 도메인 서비스 (CRUD + 인증 토큰 발급)"""

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        """user_id로 사용자 조회. 없으면 404"""
        db_user = await UserCrud.get_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return db_user

    @staticmethod
    async def register(db: AsyncSession, user: UserCreate):
        """
        회원가입:
        - username 중복 검사
        - 비밀번호 해시 후 저장
        """
        # username 중복 검사
        if await UserCrud.get_username(db, user.username):
            raise HTTPException(status_code=400, detail="이미 존재하는 사용자명입니다.")

        # 비밀번호 해시
        hashed_pw = await get_pwd_hash(user.password)
        user_create = UserCreate(username=user.username, password=hashed_pw, email=user.email)

        try:
            db_user = await UserCrud.create(db, user_create)
            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception:
            # 트랜잭션 롤백 후 에러 응답
            await db.rollback()
            raise HTTPException(status_code=500, detail="회원가입 처리 중 오류가 발생했습니다.")

    @staticmethod
    async def login(db: AsyncSession, user: UserLogin) -> Tuple[object, str, str]:
        """
        로그인:
        - 이메일 조회 및 비밀번호 검증
        - 리프레시/액세스 토큰 생성
        - 리프레시 토큰 DB에 저장
        - (updated_user, access_token, refresh_token) 반환
        """
        db_user = await UserCrud.get_email(db, user.email)
        # 사용자 없음 또는 비밀번호 불일치
        if not db_user or not await verify_pwd(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

        # 토큰 생성
        refresh_token = create_refresh_token(db_user.user_id)
        access_token = create_access_token(db_user.user_id)

        # 리프레시 토큰 저장
        try:
            updated_user = await UserCrud.update_refresh_token_id(db, db_user.user_id, refresh_token)
            await db.commit()
            await db.refresh(updated_user)
        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="로그인 처리 중 오류가 발생했습니다.")

        return updated_user, access_token, refresh_token
