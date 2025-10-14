# backend/app/database/schemas/user.py
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# 공통 필드(요청/내부 공통)
class UserBase(BaseModel):
    email: str
    username: str


# 회원가입 요청
class UserCreate(UserBase):
    password: str


# 로그인 요청
class UserLogin(BaseModel):
    email: str
    password: str


# 부분 수정(패치) 요청
class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


# DB에서 가져오는 내부용 모델
class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy 객체 → Pydantic 변환 허용

    user_id: int
    # 내부적으로 비밀번호 해시를 다루고 싶다면 여기에 포함 가능(응답 모델과 구분!)
    # password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# 클라이언트 응답용(비밀번호 제외)
class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    created_at: datetime
