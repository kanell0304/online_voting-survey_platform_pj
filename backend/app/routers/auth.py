from __future__ import annotations

from datetime import datetime
from typing import Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import jwt

# 프로젝트 내부 의존성
from backend.app.database.database import get_db
from backend.app.core.settings import settings
from backend.app.database.models.user import User  # 팀원의 User 모델 사용

router = APIRouter()
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── Swagger에서 Bearer 토큰 붙여넣기 사용 ─────────────────────────────
#  - /docs 의 Authorize 팝업에 'Bearer' 입력칸이 생김
bearer_scheme = HTTPBearer(auto_error=True)

# ---- 유틸: User 모델 필드명 동적 매핑 (팀원 스키마와 충돌 방지) ----
def pick_attr_name(model, candidates) -> Optional[str]:
    for c in candidates:
        if hasattr(model, c):
            return c
    return None

EMAIL_FIELD = pick_attr_name(User, ["email", "user_email", "email_id", "username", "login"])
PWD_FIELD   = pick_attr_name(User, ["password_hash", "hashed_password", "password"])
NAME_FIELD  = pick_attr_name(User, ["name", "username", "nickname", "display_name"])

if EMAIL_FIELD is None or PWD_FIELD is None:
    raise RuntimeError(
        "User 모델에서 이메일/패스워드 필드를 찾지 못했습니다. "
        "candidates(email): email/user_email/email_id/username/login, "
        "candidates(password): password_hash/hashed_password/password"
    )

# ---- 스키마 (이 파일 내부에서만 사용) ----
class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# ---- JWT ----
def create_access_token(sub: str) -> Tuple[str, int]:
    expire = datetime.utcnow() + settings.access_token_expire
    payload = {"sub": sub, "exp": expire}
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algo)
    return token, int(settings.access_token_expire.total_seconds())

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_ctx.verify(plain, hashed)

def hash_password(plain: str) -> str:
    return pwd_ctx.hash(plain)

# ---- 공통 인증 의존성: Bearer 토큰으로 현재 사용자 로드 ----
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algo])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    email: Optional[str] = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    result = await db.execute(select(User).where(getattr(User, EMAIL_FIELD) == email))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# ---- 엔드포인트 ----
@router.post("/register", response_model=TokenOut, summary="회원가입")
async def register(data: RegisterIn, db: AsyncSession = Depends(get_db)):
    # 중복 체크
    stmt = select(User).where(getattr(User, EMAIL_FIELD) == data.email)
    existed = (await db.execute(stmt)).scalars().first()
    if existed:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    # 유저 생성
    user = User()
    setattr(user, EMAIL_FIELD, data.email)
    setattr(user, PWD_FIELD, hash_password(data.password))
    if NAME_FIELD and data.name:
        setattr(user, NAME_FIELD, data.name)

    db.add(user)
    await db.commit()

    token, exp = create_access_token(sub=data.email)
    return TokenOut(access_token=token, expires_in=exp)

@router.post("/login", response_model=TokenOut, summary="로그인")
async def login(data: LoginIn, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(getattr(User, EMAIL_FIELD) == data.email)
    user = (await db.execute(stmt)).scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="잘못된 인증 정보입니다.")

    stored_hash = getattr(user, PWD_FIELD, None)
    if not stored_hash or not verify_password(data.password, stored_hash):
        raise HTTPException(status_code=401, detail="잘못된 인증 정보입니다.")

    token, exp = create_access_token(sub=data.email)
    return TokenOut(access_token=token, expires_in=exp)

@router.get("/me", summary="내 정보(토큰 필요)")
async def me(current_user: User = Depends(get_current_user)):
    return {
        "user_id": getattr(current_user, "user_id", None),
        "email": getattr(current_user, EMAIL_FIELD, None),
        "username": getattr(current_user, NAME_FIELD, None),
        "roles": [r.name for r in getattr(current_user, "roles", [])] if hasattr(current_user, "roles") else [],
    }
