from __future__ import annotations
from dotenv import load_dotenv
load_dotenv()

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from backend.app.core.settings import settings
from backend.app.database.base import Base

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
        # ✅ 인증만: 유저/롤/유저-롤만 임포트
        from backend.app.database.models.user import User  # noqa: F401
        from backend.app.database.models.roles import Role  # noqa: F401
        from backend.app.database.models.user_roles import UserRole  # noqa: F401

        # ✅ 생성할 테이블만 명시적으로 지정
        tables_to_create = [User.__table__, Role.__table__, UserRole.__table__]

        # 디버그: 실제 생성 시도할 테이블 목록 출력
        print("create_tables(tables):", [t.name for t in tables_to_create])

        Base.metadata.create_all(bind=sync_engine, tables=tables_to_create)
        print("데이터베이스 테이블 생성 (auth-only) 성공")
    except Exception as e:
        print(f"테이블 생성 실패: {e}")