from __future__ import annotations

from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from datetime import datetime
from typing import Optional

# 설문 질문 옵션 ex) 텍스트, 4지선다, 예/아니오
class SurveyOption(Base):
    __tablename__ = "survey_options"

    option_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("survey_questions.question_id"), nullable=False, index=True)
    option_text: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=True)

    # 옵션 N : 1 질문
    question: Mapped["SurveyQuestion"] = relationship(
        "SurveyQuestion",
        back_populates="options"
    )

    def __repr__(self) -> str:
        return f"<SurveyOption id={self.option_id} q={self.question_id}>"
