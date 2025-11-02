# backend/app/service/user.py
from pydoc import describe
from typing import Tuple, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile, Depends
from sqlalchemy import select

from .image_service import ImageService
from ..core.auth import get_user_id
from ..database.models import Roles, UserRoles
from ..database.models.roles import RoleEnum
from ..database.schemas.user import UserCreate, UserLogin, UserUpdate, UserRead, UserReadWithProfile
from ..database.crud.user import UserCrud
from ..database.models import User
from ..core.jwt_context import (get_pwd_hash, verify_pwd, create_access_token, create_refresh_token)
from ..service.email_service import email_service
from ..database.models import Image

class UserService:
    """User 도메인 서비스 (CRUD + 인증 토큰 발급)"""

    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        db_user = await UserCrud.get_id(db, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return db_user

    @staticmethod
    async def get_user_with_user_roles(db: AsyncSession, user_id: int):
        db_user = await UserCrud.get_user_with_role(db, user_id)
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
    async def register(db: AsyncSession, user: UserCreate, role_name: str = RoleEnum.USER):
        if await UserCrud.get_email(db, user.email):
            raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

        hashed_pw = await get_pwd_hash(user.password)
        # user_create = UserCreate(username=user.username, phone_number=user.phone_number, password=hashed_pw, email=user.email, role=user.role)

        try:

            db_user = User(username=user.username, phone_number=user.phone_number, password=hashed_pw, email=user.email)
            db.add(db_user)
            await db.flush()

            # user_role 로직 추가 - 이경준
            result = await db.execute(select(Roles).where(Roles.role_name == role_name))
            role = result.scalar_one_or_none()

            if not role:
                role_description = "일반 사용자"
                if role_name == "ADMIN":
                    role_description = "Admin 관리자"
                role = Roles(role_name=role_name, description=role_description)
                db.add(role)
                await db.flush()

            user_role = UserRoles(user_id = db_user.user_id, role_id=role.id)
            db.add(user_role)

            await db.commit()
            await db.refresh(db_user)
            return db_user
        except Exception as e:
            await db.rollback()
            print(f"회원가입 에러: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
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

    # 비밀번호 찾기 (인증코드 발송)
    @staticmethod
    async def forgot_password(db: AsyncSession, email: str, username: str, phone_number: str):
        # 사용자 확인
        user = await UserCrud.get_user_by_credentials(db, email, username, phone_number)
        if not user: # 없으면 exception 발생
            raise HTTPException(status_code=404, detail="User Not Found")

        # 6자리 인증코드 생성
        reset_code = UserCrud.generate_reset_code()

        # DB에 코드 저장 (유효기간 15분)
        await UserCrud.save_reset_code(db, user.user_id, reset_code, expires_minutes=15)
        await db.commit()

        # 이메일 발송
        success, message = await email_service.send_reset_code_email(recipient_email=user.email, username=user.username, reset_code=reset_code)

        if not success:
            raise HTTPException(status_code=500, detail=message)

        return {
            "message": "인증코드가 이메일로 발송되었습니다.",
            "expires_in_minutes": 15
        }

    # 인증코드로 비밀번호 재설정
    @staticmethod
    async def reset_password_with_code(db: AsyncSession, email: str, reset_code: str, new_password: str):
        # 인증코드 검증
        user = await UserCrud.verify_reset_code(db, email, reset_code)

        if not user:
            raise HTTPException(status_code=400, detail="인증코드가 유효하지 않거나 만료되었습니다.")

        try:
            # 비밀번호 해시화 및 업데이트
            hashed_password = await get_pwd_hash(new_password)
            await UserCrud.update_by_id(db, user.user_id, {"password": hashed_password})

            # 인증코드 초기화
            await UserCrud.clear_reset_code(db, user.user_id)

            await db.commit()

            return {"message": "비밀번호가 성공적으로 변경되었습니다."}

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail="비밀번호 변경 중 오류가 발생했습니다.")

    @staticmethod
    async def update_profile_image(file: UploadFile, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).filter(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # 기존 프로필 이미지 삭제
        if user.profile_image_id:
            old_image_result = await db.execute(select(Image).filter(Image.id == user.profile_image_id))
            old_image = old_image_result.scalar_one_or_none()

            if old_image:
                await db.delete(old_image)

        # 새 이미지 업로드
        db_image = await ImageService.image_upload(file, db)

        # 유저에 이미지 연결
        user.profile_image_id = db_image.id
        await db.commit()
        await db.refresh(user)

        return user

    @staticmethod
    async def get_user_with_profile(db: AsyncSession, user_id: int) -> UserReadWithProfile:
        result = await db.execute(select(User).filter(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # UserReadWithProfile로 변환
        return UserReadWithProfile.from_user(user)

    @staticmethod
    async def delete_profile_image(db: AsyncSession, user_id: int):
        result = await db.execute(select(User).filter(User.user_id == user_id))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if not user.profile_image_id:
            raise HTTPException(status_code=404, detail="No profile image found")

        # 이미지 삭제
        image_result = await db.execute(select(Image).filter(Image.id == user.profile_image_id))
        image = image_result.scalar_one_or_none()

        if image:
            await db.delete(image)

        user.profile_image_id = None

        await db.commit()
        await db.refresh(user)

        return user
