from backend.app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table, Column

# 연결 테이블 (M:N)
survey_tags = Table(
    "survey_tags",
    Base.metadata,
    Column("survey_id", Integer, ForeignKey("surveys.survey_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    surveys = relationship("Surveys", secondary=survey_tags, back_populates="tags")
