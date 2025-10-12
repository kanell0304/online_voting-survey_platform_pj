from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.schemas.survey import SurveyCreate
from backend.app.database.crud.survey_crud import SurveyCrud

class SurveyService:
    def __init__(self, db:AsyncSession):
        self.db=db

    async def create_new_survey(self, user_id:int, survey:SurveyCreate):
        return await SurveyCrud.create_new_survey(self.db, user_id, survey)
    
    async def list_my_surveys(self, user_id:int):
        return await SurveyCrud.list_my_surveys(self.db, user_id)
    
    async def get_my_detailed_survey(self, survey_id:int, user_id:int):
        my_survey=await SurveyCrud.get_my_detailed_survey(self.db, survey_id, user_id)

        if not my_survey:
            raise HTTPException(status_code=404, detail="Survey Not Found")
        return my_survey
    
    # 설문 삭제 서비스

