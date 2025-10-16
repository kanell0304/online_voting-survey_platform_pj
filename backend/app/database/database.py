from __future__ import annotations
from dotenv import load_dotenv
load_dotenv()

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from ..core.settings import settings
from .base import Base

# 엔진 설정
async_engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
    echo=False
)

sync_engine = create_engine(
    settings.sync_database_url,
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        yield db


def create_tables():
    try:
        # 모든 모델 import (Base에 등록)
        from .models import user
        from .models import roles
        from .models import user_roles
        from .models import surveys
        from .models import survey_question
        from .models import survey_option
        from .models import responses
        from .models import response_detail
        from .models import surveystats
        from .models import email_logs
        from .models import image

        Base.metadata.create_all(bind=sync_engine)
        print("데이터베이스 테이블 생성")
        
    except Exception as e:
        print(f"테이블 생성 실패: {e}")
