from backend.app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timedelta
from sqlalchemy import String, TIMESTAMP, func, ForeignKey
from typing import Optional

class Surveys(Base):
    __tablename__ = "surveys"

    servey_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(40), nullable=False)
    description: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)
    expire_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, default=(lambda: datetime.utcnow() + timedelta(days=14)), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="posts")