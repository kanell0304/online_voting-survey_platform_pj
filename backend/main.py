from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.database import create_tables
from app.service.api_routes import router as service_router
from app.database.base import Base
from app.router import image

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

# FastAPI 앱 생성
app = FastAPI(
    title="My FastAPI Application",
    description="API with separated service layer",
    version="1.0.0",
    lifespan=lifespan
)

# 서비스 라우터를 /api 프리픽스로 포함
app.include_router(
    service_router,
    prefix="/api",
    tags=["Service API"]
)

# 라우터 추가
app.include_router(image.router)