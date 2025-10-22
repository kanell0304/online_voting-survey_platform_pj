from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.database import create_tables
from backend.app.middleware.token_refresh import TokenRefreshMiddleware
from fastapi.middleware.cors import CORSMiddleware
from backend.app.router.api_routes_preset import router as service_router
from app.router import image
from app.router import email
from app.router import response
from app.router import user
from app.router import survey, survey_question, survey_option


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# 서비스 라우터를 /api 프리픽스로 포함
app.include_router(
    service_router,
    prefix="/api",
    tags=["Service API"]
)

# 라우터 추가
app.include_router(image.router)
app.include_router(email.router)
app.include_router(response.router)
app.include_router(user.router)
app.include_router(survey.router)
app.include_router(survey_question.router)
app.include_router(survey_option.router)

@app.get("/health")
def health():
    return {"status": "ok"}