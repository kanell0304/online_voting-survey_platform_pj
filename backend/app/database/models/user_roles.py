from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP, ForeignKey
from datetime import datetime

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    assigned_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
