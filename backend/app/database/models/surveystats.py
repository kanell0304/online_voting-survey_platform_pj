from backend.app.database.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, TIMESTAMP, func, DateTime, String, JSON, ForeignKey
from datetime import datetime

class SurveyStats(Base):
    __tablename__="survey_stats"

    id:Mapped[int]=mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    survey_id:Mapped[int]=mapped_column(ForeignKey("surveys.survey_id"), index=True, nullable=False)
    question_id:Mapped[Optional[int]]=mapped_column(ForeignKey("survey_questions.question_id"), index=True, nullable=True)
    period_start:Mapped[Optional[datetime]]=mapped_column(DateTime, index=True, nullable=True)
    period_end:Mapped[Optional[datetime]]=mapped_column(DateTime, index=True, nullable=True)

    stat_kind:Mapped[str]=mapped_column(String(30), index=True, nullable=False)
    stat_data:Mapped[dict]=mapped_column(JSON, nullable=False)
    computed_at:Mapped[datetime]=mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)