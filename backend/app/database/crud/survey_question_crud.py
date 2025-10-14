from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
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
        await db.refresh(q)
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
