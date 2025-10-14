# backend/app/middleware/token_refresh.py
from __future__ import annotations

from typing import Optional
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

from jwt import ExpiredSignatureError, InvalidTokenError

from backend.app.database.database import get_db
from backend.app.database.crud.user import UserCrud
from backend.app.core.jwt_context import (
    verify_token,
    create_access_token,
    create_refresh_token,
)
from backend.app.core.auth import set_auth_cookies


class TokenRefreshMiddleware(BaseHTTPMiddleware):
    """
    동작 요약
    1) 요청 쿠키에서 access_token, refresh_token 읽기
    2) access_token 유효 → 그대로 통과
       access_token 무효 → refresh_token 검사
    3) refresh_token 유효 → 새 access/refresh 토큰 발급 + DB에 refresh 토큰 업데이트 + 쿠키 교체
       refresh_token 만료 → 401 with {"detail": "refresh_token_expired"}
       refresh_token 무효 → 아무 것도 하지 않고 통과 (로그인 필요 상태 유지)
    """

    async def dispatch(self, request: Request, call_next):
        # 먼저 downstream 실행 (응답 객체를 만든 후 쿠키만 교체)
        response = await call_next(request)

        access_token: Optional[str] = request.cookies.get("access_token")
        refresh_token: Optional[str] = request.cookies.get("refresh_token")

        # 1) access_token이 있고, 유효하면 그대로 통과
        if access_token:
            try:
                verify_token(access_token)
                return response
            except (ExpiredSignatureError, InvalidTokenError):
                # 무효/만료면 아래에서 refresh_token으로 갱신 시도
                pass

        # 2) refresh_token 없으면 그대로 통과(로그인 필요 상태 유지)
        if not refresh_token:
            return response

        # 3) refresh_token 검증
        try:
            payload = verify_token(refresh_token)  # 학원 템플릿 기준: payload(dict) 반환
        except ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "refresh_token_expired"})
        except InvalidTokenError:
            # 무효 토큰이면 그대로 통과 (다음 요청에서 로그인하도록)
            return response

        # payload에서 사용자 식별 추출
        user_id = payload.get("sub") or payload.get("user_id")
        if user_id is None:
            return response

        try:
            user_id = int(user_id)
        except Exception:
            return response

        # 새 토큰 발급
        new_access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id)

        # DB에 refresh 토큰 갱신 (미들웨어는 DI를 못 쓰므로 의존성 제너레이터 직접 사용)
        try:
            async for db in get_db():
                await UserCrud.update_refresh_token_id(db, user_id, new_refresh_token)
                await db.commit()
                break
        except Exception:
            # DB 갱신 실패 시 쿠키를 바꾸지 않고 그대로 반환
            return response

        # 쿠키 교체
        set_auth_cookies(response, new_access_token, new_refresh_token)
        return response
