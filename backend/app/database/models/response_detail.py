from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class ResponseDetail(Base):
    __tablename__ = "response_details" # 개별 응답 선택지

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("responses.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("survey_questions.question_id"), nullable=False)
    selected_option_id: Mapped[int] = mapped_column(ForeignKey("survey_options.option_id"), nullable=False)

    # Relationships
    response: Mapped["Response"] = relationship("Response", back_populates="details")
