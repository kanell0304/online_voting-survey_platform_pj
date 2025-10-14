# backend/app/core/auth.py
from __future__ import annotations

from fastapi import Request, Response, HTTPException
from datetime import timedelta, datetime, timezone
from typing import Optional, Tuple, Any

from backend.app.core.settings import settings
from backend.app.core.jwt_context import verify_token

# 쿠키 키 이름
ACCESS_COOKIE_NAME = "access_token"
REFRESH_COOKIE_NAME = "refresh_token"

# 공통 쿠키 옵션 (HTTPS 환경이면 secure=True, samesite='none' 고려)
COOKIE_COMMON = {
    "httponly": True,
    "samesite": "lax",
    "secure": False,
    "path": "/",
}

def _expires_at(delta: timedelta) -> datetime:
    return datetime.now(timezone.utc) + delta

def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """액세스/리프레시 토큰을 HttpOnly 쿠키로 세팅"""
    response.set_cookie(
        key=ACCESS_COOKIE_NAME,
        value=access_token,
        expires=_expires_at(settings.access_token_expire),
        **COOKIE_COMMON,
    )
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        expires=_expires_at(settings.refresh_token_expire),
        **COOKIE_COMMON,
    )

def clear_auth_cookies(response: Response) -> None:
    """로그아웃용: 쿠키 삭제"""
    response.delete_cookie(ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/")

def get_tokens_from_request(request: Request) -> Tuple[Optional[str], Optional[str]]:
    """요청 쿠키에서 액세스/리프레시 토큰을 읽어온다"""
    access = request.cookies.get(ACCESS_COOKIE_NAME)
    refresh = request.cookies.get(REFRESH_COOKIE_NAME)
    return access, refresh

def _extract_user_id_from_verify_result(result: Any) -> Optional[int]:
    """
    verify_token() 반환값이 dict(payload) 또는 user_id(int/str)일 수 있으므로 안전하게 user_id 추출
    """
    # dict(payload) 케이스
    if isinstance(result, dict):
        val = result.get("sub") or result.get("user_id")
        if val is None:
            return None
        try:
            return int(val)
        except Exception:
            return None
    # int/str 케이스(학원 템플릿 일부는 user_id를 바로 반환하기도 함)
    if isinstance(result, (int, str)):
        try:
            return int(result)
        except Exception:
            return None
    return None

def get_user_id(request: Request) -> int:
    """
    FastAPI Depends 용.
    - access_token 쿠키를 읽어 JWT 검증
    - payload 또는 반환값에서 user_id를 추출
    """
    access, _ = get_tokens_from_request(request)
    if not access:
        raise HTTPException(status_code=401, detail="인증 정보가 없습니다.")

    try:
        verify_result = verify_token(access)
    except Exception:
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")

    user_id = _extract_user_id_from_verify_result(verify_result)
    if user_id is None:
        raise HTTPException(status_code=401, detail="토큰에 사용자 정보가 없습니다.")
    return user_id
