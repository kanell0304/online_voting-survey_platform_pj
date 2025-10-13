# backend/min_main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.app.database.database import create_tables
from backend.app.routers.auth import router as auth_router


def _strip_non_auth_relationships() -> None:
    """
    팀 코드(모델 파일) 수정 없이, 미니앱에서만 User의 비-인증 도메인 관계들을 제거한다.
    - class 속성(delattr)
    - mapper 관계(dict) 및 attrs/_props에서도 제거
    """
    try:
        from backend.app.database.models.user import User  # type: ignore
        # 프로젝트 상황에 맞게 필요 시 아래 목록에 이름을 추가
        candidates = [
            "surveys",          # User -> Surveys
            "responses",        # User -> Response
            "email_logs",       # User -> EmailLog
            "comments",         # User -> Comment
            "tags",             # User -> Tag
            "survey_stats",     # User -> SurveyStats
        ]

        # 1) 클래스 속성 제거
        for name in candidates:
            if hasattr(User, name):
                try:
                    delattr(User, name)
                    print(f"[auth-min] delattr User.{name}")
                except Exception as e:
                    print(f"[auth-min] delattr User.{name} skip: {e}")

        # 2) 매퍼 레벨에서 제거
        try:
            m = User.__mapper__  # Mapper 객체
            # relationships / attrs / _props 세 군데를 신중히 제거
            for name in list(getattr(m, "relationships", {})):
                if name in candidates:
                    try:
                        m.relationships.pop(name, None)
                        print(f"[auth-min] mapper.relationships pop: {name}")
                    except Exception as e:
                        print(f"[auth-min] mapper.relationships pop {name} skip: {e}")

            for name in list(getattr(m, "attrs", {})):
                if name in candidates:
                    try:
                        m.attrs.pop(name, None)
                        print(f"[auth-min] mapper.attrs pop: {name}")
                    except Exception as e:
                        print(f"[auth-min] mapper.attrs pop {name} skip: {e}")

            # _props는 내부 속성이지만, 관계가 남아 있으면 여기에도 있을 수 있음
            if hasattr(m, "_props"):
                for name in list(getattr(m, "_props", {})):
                    if name in candidates:
                        try:
                            m._props.pop(name, None)  # type: ignore[attr-defined]
                            print(f"[auth-min] mapper._props pop: {name}")
                        except Exception as e:
                            print(f"[auth-min] mapper._props pop {name} skip: {e}")
        except Exception as e:
            print(f"[auth-min] mapper strip failed: {e}")

    except Exception as e:
        print(f"[auth-min] strip relationships failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1) 인증 도메인 테이블만 생성 (users / roles / user_roles)
    create_tables()
    # 2) User에 붙은 비-인증 관계 제거 (매퍼 초기화 전에 수행)
    _strip_non_auth_relationships()
    yield


app = FastAPI(
    title="Auth-only FastAPI",
    description="User & token endpoints only",
    version="1.0.0",
    lifespan=lifespan,
)

# 인증 라우터만 마운트
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
