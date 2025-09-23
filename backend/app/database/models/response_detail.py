from backend.app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column

class ResponseDetail(Base):
    __tablename__ = "response_details" # 개별 응답 선택지

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    response_id: Mapped[int] = mapped_column(nullable=False)
    question_id: Mapped[int] = mapped_column(nullable=False)
    selected_option_id: Mapped[int] = mapped_column(nullable=False)