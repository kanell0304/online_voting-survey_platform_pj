# backend/min_main.py
from fastapi import FastAPI
from backend.app.middleware.token_refresh import TokenRefreshMiddleware
from backend.app.routers.user import router as user_router

app = FastAPI(title="Minimal App", version="0.1.0")

app.add_middleware(TokenRefreshMiddleware)
app.include_router(user_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}
