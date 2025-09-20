from backend.app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Table

# 연결 테이블 (M:N)
survey_tags = Table(
    "survey_tags",
    Base.metadata,
    mapped_column("survey_id", Integer, primary_key=True),
    mapped_column("tag_id", Integer, primary_key=True)
    # ForeignKey("surveys.survey_id", ondelete="CASCADE"),
    # ForeignKey("tags.id", ondelete="CASCADE")
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    surveys = relationship("Survey", secondary=survey_tags, back_populates="tags")


# Survey 모델 안에 추가
class Survey(Base):
    __tablename__ = "surveys"
    # ... 기존 컬럼들 ...

    tags = relationship("Tag", secondary=survey_tags, back_populates="surveys")
