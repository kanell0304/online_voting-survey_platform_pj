import enum

from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, TIMESTAMP, Enum
from datetime import datetime
from typing import Optional, List


# 계정 권한 - ADMIN, USER
class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"

# 유저 역할 ex) admin, manager, guest
class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    role_name: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), unique=True, nullable=False) # 역할 이름
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True) # 역할에 대한 설명
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now) # 생성일
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now, onupdate=datetime.now) # 수정일

    users: Mapped[List["User"]] = relationship("User", secondary="user_roles", back_populates="roles")