from backend.app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import TIMESTAMP
from datetime import datetime

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(primary_key=True)
    assigned_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
