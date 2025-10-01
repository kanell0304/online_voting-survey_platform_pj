from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.dialects.mysql import LONGBLOB
from backend.app.database.base import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # autoincrement 추가
    filename = Column(String(255), nullable=False)
    data = Column(LONGBLOB, nullable=False)
