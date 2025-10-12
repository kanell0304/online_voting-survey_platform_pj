from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.database import get_db
from backend.app.database.schemas.survey import SurveyCreate, SurveyOut
from backend.app.service.survey_service import SurveyService

router=APIRouter(prefix="/survey", tags=["surveys"])

@router.post("", response_model=SurveyOut)
async def create_survey(new_survey:SurveyCreate, user:int, db:AsyncSession=Depends(get_db)):
    return await SurveyService(db).create_new_survey(user_id=user, new_survey=new_survey)

@router.get("", response_model=List[SurveyOut])
async def list_surveys(user:int, db:AsyncSession=Depends(get_db)):
    return await SurveyService(db).list_my_surveys(user_id=user)

@router.get("/{survey_id}", response_model=SurveyOut)
async def get_my_survey(survey_id:int, user:int, db:AsyncSession=Depends(get_db)):
    return await SurveyService(db).get_my_detailed_survey(survey_id, user_id=user)

# current_user...
# 설문 삭제

