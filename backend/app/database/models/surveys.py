from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from sqlalchemy import String, TIMESTAMP, func, ForeignKey, Boolean
from typing import Optional, List

# 설문지 테이블
class Surveys(Base):
    __tablename__ = "surveys"

    survey_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(40), nullable=False) # 설문지 주제
    description: Mapped[str] = mapped_column(String(100), nullable=False) # 설문지에 대한 설명
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False) # 설문지 작성자 user_id
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False) # 생성일
    expire_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, default=(lambda: datetime.utcnow() + timedelta(days=14)), nullable=True) # 마감일 default: 생성일 + 14일
    updated_at: Mapped[Optional[datetime]]=mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)
    is_public:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="surveys")
    questions: Mapped[List["SurveyQuestion"]] = relationship("SurveyQuestion", back_populates="survey", cascade="all, delete-orphan", lazy="selectin")
    responses: Mapped[List["Response"]] = relationship("Response", cascade="all, delete-orphan", lazy="selectin")
    email_logs: Mapped[List["EmailLog"]] = relationship("EmailLog", back_populates="surveys", cascade="all, delete-orphan", lazy="selectin")