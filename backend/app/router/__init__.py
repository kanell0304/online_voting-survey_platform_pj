# backend/app/router/__init__.py

# 각 라우터를 안전하게 로드하고, 없으면 None으로 둔다.
def _safe_import_router(module_path, attr="router"):
    try:
        module = __import__(module_path, fromlist=[attr])
        return getattr(module, attr, None)
    except Exception:
        return None

# === 팀 공용(설문 등) 라우터 ===
image_router = _safe_import_router("backend.app.router.image")
email_router = _safe_import_router("backend.app.router.email")
response_router = _safe_import_router("backend.app.router.response")
survey_router = _safe_import_router("backend.app.router.survey")
survey_question_router = _safe_import_router("backend.app.router.survey_question")
survey_option_router = _safe_import_router("backend.app.router.survey_option")

# === 유저 라우터(네가 담당한 최신 구현) ===
# routers/user.py 에 있던 걸 router/user.py 로 옮겼다고 가정
user_router = _safe_import_router("backend.app.router.user")

# (선택) 레거시를 남기고 싶다면, 아래처럼 별도 prefix로 노출할 수도 있음
# user_legacy_router = _safe_import_router("backend.app.router.user_legacy")
