from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List

from backend.app.database.models.survey_option import SurveyOption
from backend.app.database.schemas.survey_question import SurveyQuestionCreate
from backend.app.database.models.survey_question import SurveyQuestion
from backend.app.database.models.surveys import Surveys


class SurveyQuestionCrud:
    @staticmethod
    async def add_new_question(db:AsyncSession, survey_id:int, user_id:int, question:SurveyQuestionCreate) -> Optional[SurveyQuestion]:
        survey=await db.execute(select(Surveys).where(Surveys.survey_id==survey_id, Surveys.user_id==user_id))
        if survey.scalar_one_or_none() is None:
            return None
        
        q=SurveyQuestion(survey_id=survey_id, 
                         question_text=question.question_text, 
                         question_type=question.question_type)

        db.add(q)
        await db.flush()

        # 객관식 질문 생성을 위해 다음 코드를 추가했습니다. -이경준-
        # <
        if question.options: # 질문 타입이 객관식(선택지)일때 선택지에 관한 데이터가 있다면
            for opt_data in question.options: # 배열을 순환
                opt = SurveyOption( # option 생성
                    question_id=q.question_id,
                    option_text=opt_data.option_text # 선택지 텍스트 - ex) 사과
                )
                db.add(opt)

        await db.flush()
        await db.refresh(q)
        # >
        return q
    
    @staticmethod
    async def read_a_question(db:AsyncSession, survey_id:int, user_id:int, question_id:int)->Optional[SurveyQuestion]:
        check=await db.execute(select(Surveys.survey_id).where(Surveys.survey_id==survey_id, Surveys.user_id==user_id))
        if check.scalar_one_or_none() is None:
            return None
        
        stmt = (select(SurveyQuestion).where(
            SurveyQuestion.survey_id == survey_id, 
            SurveyQuestion.question_id == question_id).options(selectinload(SurveyQuestion.options)))
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def read_all_questions(db:AsyncSession, survey_id:int, user_id:int)->List[SurveyQuestion]:
        check=await db.execute(select(Surveys).where(Surveys.survey_id==survey_id, Surveys.user_id==user_id))
        if check.scalar_one_or_none() is None:
            return []
        
        stmt=(select(SurveyQuestion).where(SurveyQuestion.survey_id==survey_id).options(
            selectinload(SurveyQuestion.options)).order_by(SurveyQuestion.question_id.asc()))
        result=await db.execute(stmt)
        return list(result.scalars())
    
    @staticmethod
    async def delete_a_question(db:AsyncSession, survey_id:int, question_id:int, user_id:int) -> int:
        check=await db.execute(select(Surveys.survey_id).where(Surveys.survey_id==survey_id, Surveys.user_id==user_id))
        if check.scalar_one_or_none() is None:
            return 0
        
        result=await db.execute(delete(SurveyQuestion).where(
            SurveyQuestion.question_id==question_id,
            SurveyQuestion.survey_id==survey_id
        ))
        return result.rowcount or 0
