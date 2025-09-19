from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from backend.app.core.settings import settings
from sqlalchemy.orm import sessionmaker

# 비동기 db연결 생성하는 함수 (mysql+asyncmy url사용하여 비동기적으로 db와 연결한다)
async_engine=create_async_engine(settings.database_url, echo=False)

# 비동기 엔진과 연결된 세션사용하려고
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

# 동기 db연결 생성하는 함수 (동기적으로 db와 연결한다))
sync_engine=create_engine(settings.sync_database_url, pool_pre_ping=True)

# 기본 클래스 설정(Base)
Base=declarative_base()

# 비동기 세션 생성
# async def get_db():
#     session=None
#     try:
#         session=AsyncSessionLocal()
#         yield session
#     except:
#         pass
#     finally:
#         if session:
#             await session.close()
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session