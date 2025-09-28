from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, func
from typing import Optional, List

class User(Base):
    __tablename__="users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(300), nullable=False)
    refresh_token:Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=True)

    #1:M관계
    survey:Mapped[List["Surveys"]]=relationship("Surveys", back_populates="user", cascade="all, delete-orphan")
    responses:Mapped[List["Response"]]=relationship("Response", cascade="all, delete-orphan")
