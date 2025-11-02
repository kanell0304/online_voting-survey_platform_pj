# backend/app/database/schemas/user.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict


# 공통 필드(요청/내부 공통)
class UserBase(BaseModel):
    email: str
    username: str
    phone_number: str


# 회원가입 요청
class UserCreate(UserBase):
    password: str
    role: Optional[str] = "USER"  # 기본값 USER => 'ADMIN' 으로 생성하려면 ADMIN 값 입력 필요

# 로그인 요청
class UserLogin(BaseModel):
    email: str
    password: str


# 부분 수정(패치) 요청
class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserProfileImageUpdate(BaseModel):
    pass


# DB에서 가져오는 내부용 모델
class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy 객체 → Pydantic 변환 허용

    user_id: int
    profile_image_id: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class RoleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role_name: str
    description: Optional[str] = None

# 클라이언트 응답용(비밀번호 제외)
class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    profile_image_id: Optional[int] = None
    created_at: datetime


class UserReadWithProfile(UserRead):
    profile_image_url: Optional[str] = None

    @classmethod
    def from_user(cls, user, base_url: str = ""):
        profile_url = None
        if user.profile_image_id:
            profile_url = f"{base_url}/image/raw/{user.profile_image_id}"

        return cls(
            email=user.email,
            username=user.username,
            phone_number=user.phone_number,
            user_id=user.user_id,
            profile_image_id=user.profile_image_id,
            created_at=user.created_at,
            profile_image_url=profile_url
        )


class UserReadWithRoles(UserRead):
    roles: List[RoleRead] = []


# 비밀번호 찾기 요청 - 이메일, 이름, 전화번호 입력
class ForgotPasswordRequest(UserBase):
    pass

# 인증코드로 비밀번호 재설정 -
class ResetPasswordWithCode(BaseModel):
    email: str
    reset_code: str = Field(..., min_length=6, max_length=6)
    new_password: str


class UserReadWithRolesAndProfile(UserReadWithProfile):
    roles: List[RoleRead] = []