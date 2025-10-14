from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.schemas.survey_question import SurveyQuestionCreate
from backend.app.database.crud.survey_question_crud import SurveyQuestionCrud


class SurveyQuestionService:
    @staticmethod
    async def add_question(db:AsyncSession, survey_id:int, user_id:int, question:SurveyQuestionCreate):
        return await SurveyQuestionCrud.add_new_question(db, survey_id, user_id, question)
    
    @staticmethod
    async def read_question(db:AsyncSession, survey_id:int, user_id:int, question_id:int):
        return await SurveyQuestionCrud.read_a_question(db, survey_id, user_id, question_id)
    
    @staticmethod
    async def read_question_list(db:AsyncSession, survey_id:int, user_id:int):
        return await SurveyQuestionCrud.read_all_questions(db, survey_id, user_id)
    
    @staticmethod
    async def delete_question(db:AsyncSession, survey_id:int, user_id:int, question_id:int):
        return await SurveyQuestionCrud.delete_a_question(db, survey_id, question_id, user_id)
    
