from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from typing import Optional, List

# 사용자 테이블
class User(Base):
    __tablename__="users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False) # 이름
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False) # 이메일(아이디)
    password: Mapped[str] = mapped_column(String(300), nullable=False) # 비밀번호
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False) # 전화번호
    refresh_token:Mapped[Optional[str]] = mapped_column(String(300), nullable=True) # 리프레쉬 토큰 정보
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True) # 생성일(회원가입일)

    #1:M관계
    survey:Mapped[List["Surveys"]]=relationship("Surveys", back_populates="user", cascade="all, delete-orphan")
    responses:Mapped[List["Response"]]=relationship("Response", cascade="all, delete-orphan")
