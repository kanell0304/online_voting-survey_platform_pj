from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.schemas.surveys import SurveyCreate, SurveyUpdate
from backend.app.database.crud.surveys_crud import SurveyCrud

class SurveyService:

    @staticmethod
    async def create_survey(db:AsyncSession, user_id:int, survey:SurveyCreate):
        return await SurveyCrud.create_new_survey(db, user_id, survey)
    
    @staticmethod
    async def get_detailed(db:AsyncSession, survey_id:int):
        return await SurveyCrud.get_my_detailed_survey(db, survey_id)

    @staticmethod
    async def get_all_surveys(db: AsyncSession):
        return await SurveyCrud.list_all_surveys_is_public_is_true(db)
    
    @staticmethod
    async def list_survey(db:AsyncSession, user_id:int):
        return await SurveyCrud.list_my_surveys(db, user_id)
    
    @staticmethod
    async def delete_survey(db:AsyncSession, survey_id:int, user_id:int):
        return await SurveyCrud.delete_my_survey(db, survey_id, user_id)
    
    @staticmethod
    async def modify_survey(db:AsyncSession, survey_id:int, user_id:int, survey:SurveyUpdate):
        return await SurveyCrud.modify_my_survey(db, survey_id, user_id, survey)

