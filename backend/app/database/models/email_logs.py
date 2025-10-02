from pydantic import EmailStr

from backend.app.database.base import Base
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Text, TIMESTAMP, func, DateTime, String, JSON, ForeignKey
from datetime import datetime

# 설문지 배포 정보
class EmailLog(Base):
    __tablename__="email_logs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    recipient_email: Mapped[EmailStr] = mapped_column(String(50), nullable=False) # 받는사람 이메일
    title: Mapped[str] = mapped_column(String(100), nullable=False) # 제목
    content: Mapped[str] = mapped_column(String(500), nullable=False) # 내용
    created_at:Mapped[datetime]=mapped_column(TIMESTAMP, server_default=func.now(), nullable=False) # 생성 일
    survey_id:Mapped[int]=mapped_column(ForeignKey("surveys.survey_id"), nullable=False) # 설문지 번호

    surveys: Mapped["Surveys"] = relationship("Surveys", back_populates="email_logs")