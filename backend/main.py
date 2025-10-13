from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.app.core.load_env import load as load_env
load_env()  # .env를 UTF-8로 로드 (Settings가 바로 읽을 수 있게)

from backend.app.service.api_routes import router as service_router

# 테이블 생성 유틸
from backend.app.database.init_db import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


# ✅ FastAPI 앱 생성
app = FastAPI(
    title="My FastAPI Application",
    description="API with separated service layer",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ 서비스 라우터 /api 프리픽스로 포함
app.include_router(
    service_router,
    prefix="/api",
    tags=["Service API"]
)
