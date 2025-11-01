from __future__ import annotations

from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey
from datetime import datetime

# 설문 질문 옵션 ex) 텍스트, 4지선다, 예/아니오
class SurveyOption(Base):
    __tablename__ = "survey_options"

    option_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,index=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("survey_questions.question_id", ondelete="CASCADE"), nullable=False, index=True)
    option_text: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    
    # 옵션 N : 1 질문
    question: Mapped["SurveyQuestion"] = relationship(
        "SurveyQuestion",
        back_populates="options",
        lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<SurveyOption id={self.option_id} q={self.question_id}>"
