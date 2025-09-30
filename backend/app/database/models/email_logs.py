from pydantic import EmailStr

from backend.app.database.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, TIMESTAMP, func, DateTime, String, JSON, ForeignKey
from datetime import datetime

class EmailLog(Base):
    __tablename__="email_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    received_email: Mapped[EmailStr] = mapped_column(String(50), nullable=False)
    created_at:Mapped[datetime]=mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)
    survey_id:Mapped[int]=mapped_column(ForeignKey("surveys.survey_id"), nullable=False)

    surveys: Mapped["Surveys"] = relationship("Surveys", back_populates="email_logs")