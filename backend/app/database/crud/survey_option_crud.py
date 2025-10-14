from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional
from backend.app.database.schemas.survey_option import SurveyOptionCreate
from backend.app.database.models.survey_option import SurveyOption
from backend.app.database.models.survey_question import SurveyQuestion
from backend.app.database.models.surveys import Surveys

class SurveyOptionCrud:
    @staticmethod
    async def add_an_option(db:AsyncSession, survey_id:int, question_id:int, user_id:int, o:SurveyOptionCreate)->Optional[SurveyOption]:
        result=await db.execute(select(SurveyQuestion.question_id).join(
            Surveys, Surveys.survey_id==SurveyQuestion.survey_id).where(
                SurveyQuestion.question_id==question_id,
                SurveyQuestion.survey_id==survey_id,
                Surveys.user_id==user_id))
        
        if result.scalar_one_or_none() is None:
            return None

        option=SurveyOption(question_id=question_id, option_text=o.option_text)
        db.add(option)
        await db.flush()
        await db.refresh(option)
        return option
    
    @staticmethod
    async def delete_an_option(db:AsyncSession, survey_id:int, question_id:int, option_id:int, user_id:int) -> int:
        check=await db.execute(select(SurveyOption.option_id).join(
            SurveyQuestion, SurveyQuestion.question_id==SurveyOption.question_id).join(
                Surveys, Surveys.survey_id==SurveyQuestion.survey_id).where(
                    Surveys.user_id==user_id,
                    Surveys.survey_id==survey_id,
                    SurveyQuestion.question_id==question_id,
                    SurveyOption.option_id==option_id))
        
        if check.scalar_one_or_none() is None:
            return 0
        
        result=await db.execute(delete(SurveyOption).where(
            SurveyOption.option_id==option_id,
            SurveyOption.question_id==question_id
        ))
        return result.rowcount or 0