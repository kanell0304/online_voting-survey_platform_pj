from backend.app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional


class Response(Base):
    __tablename__ = "responses" # 설문 응답

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,index=True)
    survey_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=True)
    submitted_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.utcnow)