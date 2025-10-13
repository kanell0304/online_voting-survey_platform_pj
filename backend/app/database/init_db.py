from sqlalchemy import create_engine
from backend.app.core.load_env import load as load_env
load_env()  # .env 먼저 로드

from backend.app.core.settings import settings
from backend.app.database.base import Base

def create_tables():
    try:
        # 필요한 모델만 추가 import (등록만, 수정 없음)
        import backend.app.database.models.user            # noqa: F401
        import backend.app.database.models.survey_question # noqa: F401
        import backend.app.database.models.survey_option   # noqa: F401

        # 동기 엔진으로 테이블 생성
        sync_engine = create_engine(settings.sync_database_url, future=True)
        Base.metadata.create_all(bind=sync_engine)
        print("✅ 테이블 생성 완료")
    except Exception as e:
        print(f"❌ 테이블 생성 실패: {e}")
