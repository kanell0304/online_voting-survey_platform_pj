from backend.app.database.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Text, TIMESTAMP, func, DateTime, String, JSON, ForeignKey
from datetime import datetime

class Comment(Base):
    __tablename__="comments"

    id:Mapped[int]=mapped_column(BigInteger, primary_key=True, index=True, autoincrement=True)
    survey_id:Mapped[int]=mapped_column(ForeignKey("surveys.survey_id"), index=True, nullable=False)
    question_id:Mapped[Optional[int]]=mapped_column(ForeignKey("survey_questions.question_id"), index=True, nullable=True)
    option_id:Mapped[Optional[int]]=mapped_column(ForeignKey("survey_options.option_id"), index=True, nullable=True)
    response_id:Mapped[Optional[int]]=mapped_column(ForeignKey("responses.id"), index=True, nullable=True)
    user_id:Mapped[int]=mapped_column(ForeignKey("users.user_id"), index=True, nullable=False)
    content:Mapped[str]=mapped_column(Text, nullable=False)
    created_at:Mapped[datetime]=mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

