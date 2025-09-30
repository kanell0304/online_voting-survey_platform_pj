from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TIMESTAMP, Boolean
from datetime import datetime
from typing import Optional

# 유저 역할 ex) admin, manager, guest
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False) # 역할 이름
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # 역할에 대한 설명
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now) # 생성일
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now) # 수정일
