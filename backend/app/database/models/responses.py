from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional, List

# 응답 테이블
class Response(Base):
    __tablename__ = "responses" # 설문 응답

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,index=True)
    survey_id: Mapped[int] = mapped_column(ForeignKey("surveys.survey_id"), nullable=False) # 설문지 번호
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True) # 설문 응답자 아이디정보, null가능 -> 값이 존재하지 않으면 익명
    submitted_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow) # 응답 제출 시간

    # Relationships
    details: Mapped[List["ResponseDetail"]] = relationship("ResponseDetail", back_populates="response", cascade="all, delete-orphan")
