from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.schemas.surveys import SurveyCreate
from backend.app.database.crud.surveys_crud import SurveyCrud

class SurveyService:

    @staticmethod
    async def create_survey(db:AsyncSession, user_id:int, survey:SurveyCreate):
        return await SurveyCrud.create_new_survey(db, user_id, survey)
    
    @staticmethod
    async def get_detailed(db:AsyncSession, survey_id:int):
        return await SurveyCrud.get_my_detailed_survey(db, survey_id)
    
    @staticmethod
    async def list_survey(db:AsyncSession, user_id:int):
        return await SurveyCrud.list_my_surveys(db, user_id)
    
    @staticmethod
    async def delete_survey(db:AsyncSession, user_id:int, survey_id:int):
        return await SurveyCrud.delete_my_survey(db, survey_id, user_id)

