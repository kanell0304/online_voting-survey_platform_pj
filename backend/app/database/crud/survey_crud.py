from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from backend.app.database.schemas.survey import SurveyCreate
from backend.app.database.models.surveys import Surveys


class SurveyCrud:
    
    # 설문 생성
    @staticmethod
    async def create_new_survey(db:AsyncSession, user_id:int, surveyCreate:SurveyCreate) -> Surveys:
        new_survey=Surveys(
            user_id=user_id, 
            title=surveyCreate.title,
            description=surveyCreate.description,
            expire_at=surveyCreate.expire_at,
        )

        db.add(new_survey)
        await db.flush()
        await db.refresh(new_survey)
        return new_survey
    
    # 설문 상세보기
    @staticmethod
    async def get_my_detailed_survey(db:AsyncSession, survey_id:int, user_id:int) -> Optional[Surveys]:
        stmt=select(Surveys).where(
            Surveys.survey_id==survey_id,
            Surveys.user_id==user_id
        )
        result=await db.execute(stmt)
        return result.scalar_one_or_none()

    # 나의 설문 목록 조회
    @staticmethod
    async def list_my_surveys(db:AsyncSession, user_id:int) -> List[Surveys]:
        stmt=select(Surveys).where(Surveys.user_id==user_id)
        result=await db.execute(stmt)
        return list(result.scalars())
    
    # 설문 삭제 : is_delete or deleted_at