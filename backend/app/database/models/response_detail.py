from typing import Optional
from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text

# 응답 정보
class ResponseDetail(Base):
    __tablename__ = "response_details" # 개별 응답 선택지

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("responses.id"), nullable=False) # 설문응답 번호
    question_id: Mapped[int] = mapped_column(ForeignKey("survey_questions.question_id"), nullable=False) # 질문 번호
    selected_option_id: Mapped[Optional[int]] = mapped_column(ForeignKey("survey_options.option_id"),nullable=True) # 선택지의 대한 정보 응답형식이 주관식일 때는 None
    text_response: Mapped[Optional[str]] = mapped_column(Text,nullable=True) # 응답 형식이 객관식일 때는 None

    # Relationships
    response: Mapped["Response"] = relationship("Response", back_populates="details")
