from __future__ import annotations

from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Enum, DateTime, func, ForeignKey, Boolean
from datetime import datetime
from typing import List, Optional
import enum

# 설문지 타입 정의
# Enum -> 고정 값
class QuestionType(str, enum.Enum):
    single_choice = "single_choice"
    multiple_choice = "multiple_choice"
    short_text     = "short_text"
    long_text      = "long_text"
    # rating         = "rating"
    # yes_no         = "yes_no"

# 설문지 질문 테이블 ex) 1. 이 설문을 하기까지의 경로가 어떻게 됩니까?
class SurveyQuestion(Base):
    __tablename__ = "survey_questions"

    question_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    survey_id: Mapped[int] = mapped_column(ForeignKey("surveys.survey_id", ondelete="CASCADE"), nullable=False, index=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now(), nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


    # 질문 1 : N 옵션
    options: Mapped[List["SurveyOption"]] = relationship(
        "SurveyOption",
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="SurveyOption.option_id",
        lazy="selectin"
    )
    
    # 질문 N : 1 설문
    survey: Mapped["Surveys"] = relationship("Surveys", back_populates="questions", lazy="selectin")

    def __repr__(self) -> str:
        return f"<SurveyQuestion id={self.question_id} survey_id={self.survey_id} type={self.question_type}>"
