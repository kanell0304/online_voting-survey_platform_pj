from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
from typing import Optional, List


class Response(Base):
    __tablename__ = "responses" # 설문 응답

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,index=True)
    survey_id: Mapped[int] = mapped_column(ForeignKey("surveys.survey_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow)

    # Relationships
    details: Mapped[List["ResponseDetail"]] = relationship("ResponseDetail", back_populates="response", cascade="all, delete-orphan")
