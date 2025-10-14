from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.schemas.survey_option import SurveyOptionCreate
from backend.app.database.crud.survey_option_crud import SurveyOptionCrud

class SurveyOptionService:
    @staticmethod
    async def add_option(db:AsyncSession, survey_id:int, question_id:int, user_id:int, option:SurveyOptionCreate):
        return await SurveyOptionCrud.add_an_option(db, survey_id, question_id, user_id, option)

    @staticmethod
    async def delete_option(db:AsyncSession, survey_id:int, question_id:int, option_id:int, user_id:int):
        return await SurveyOptionCrud.delete_an_option(db, survey_id, question_id, option_id, user_id)
