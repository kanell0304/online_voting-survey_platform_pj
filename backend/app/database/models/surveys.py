from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey, Boolean, DateTime, func, text, Text
from typing import Optional, List


# 설문지 테이블
class Surveys(Base):
    __tablename__ = "surveys"

    survey_id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text, nullable=False) # 설문지 주제
    description: Mapped[str] = mapped_column(Text, nullable=False) # 설문지에 대한 설명
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False) # 설문지 작성자 user_id
    

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False) # 생성일
    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=text("(NOW()+INTERVAL 14 DAY)"), nullable=True) # 마감일 default: 생성일 + 14일
    updated_at: Mapped[Optional[datetime]]=mapped_column(DateTime, onupdate=func.now(), nullable=True)
    is_public:Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    user: Mapped["User"] = relationship("User", back_populates="surveys")
    questions: Mapped[List["SurveyQuestion"]] = relationship("SurveyQuestion", back_populates="survey", cascade="all, delete-orphan", lazy="selectin")
    responses: Mapped[List["Response"]] = relationship("Response", cascade="all, delete-orphan", lazy="selectin")
    email_logs: Mapped[List["EmailLog"]] = relationship("EmailLog", back_populates="surveys", cascade="all, delete-orphan", lazy="selectin")