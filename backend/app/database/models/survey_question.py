from __future__ import annotations

from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, Enum, TIMESTAMP, func, ForeignKey
from datetime import datetime
from typing import List, Optional
import enum

class QuestionType(str, enum.Enum):
    single_choice = "single_choice"
    multiple_choice = "multiple_choice"
    short_text     = "short_text"
    long_text      = "long_text"
    rating         = "rating"
    yes_no         = "yes_no"

class SurveyQuestion(Base):
    __tablename__ = "survey_questions"

    question_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    survey_id: Mapped[int] = mapped_column(ForeignKey("surveys.survey_id"), nullable=False, index=True)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    question_type: Mapped[QuestionType] = mapped_column(Enum(QuestionType), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)

    # 질문 1 : N 옵션
    options: Mapped[List["SurveyOption"]] = relationship(
        "SurveyOption",
        back_populates="question",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="SurveyOption.option_id"
    )
    
    # 질문 N : 1 설문
    survey: Mapped["Surveys"] = relationship("Surveys", back_populates="questions")

    def __repr__(self) -> str:
        return f"<SurveyQuestion id={self.question_id} survey_id={self.survey_id} type={self.question_type}>"
