from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
from backend.app.database.schemas.surveys import SurveyCreate
from backend.app.database.models.surveys import Surveys
from backend.app.database.models.survey_question import SurveyQuestion
from backend.app.database.models.survey_option import SurveyOption


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

        for q in surveyCreate.questions:
            questions=SurveyQuestion(
                survey_id=new_survey.survey_id,
                question_text=q.question_text,
                question_type=q.question_type
            )
            db.add(questions)
            await db.flush()

            for o in q.options:
                option=SurveyOption(
                    question_id=questions.question_id,
                    option_text=o.option_text
                )
                db.add(option)
                await db.flush()

        await db.commit()

        stmt=(select(Surveys).where(Surveys.survey_id==new_survey.survey_id).options(
            selectinload(Surveys.questions).selectinload(SurveyQuestion.options)))
        result=await db.execute(stmt)
        return result.scalar_one()
    
    # 설문 상세보기
    @staticmethod
    async def get_my_detailed_survey(db:AsyncSession, survey_id: int) -> Optional[Surveys]:
        stmt=(select(Surveys).where(
            Surveys.survey_id==survey_id).options(
                selectinload(Surveys.questions).selectinload(SurveyQuestion.options)))
        
        result=await db.execute(stmt)
        return result.scalar_one_or_none()

    # 설문 목록 조회
    @staticmethod
    async def list_my_surveys(db:AsyncSession, user_id:int) -> List[Surveys]:
        stmt=select(Surveys).where(Surveys.user_id==user_id).order_by(Surveys.survey_id.desc())
        result=await db.execute(stmt)
        return list(result.scalars())
    
    # 설문 삭제
    @staticmethod
    async def delete_my_survey(db:AsyncSession, survey_id:int, user_id:int):
        stmt=delete(Surveys).where(Surveys.survey_id==survey_id, Surveys.user_id==user_id)
        result=await db.execute(stmt)
        return result.rowcount or 0
   