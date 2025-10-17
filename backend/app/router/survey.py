from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.auth import get_user_id
from backend.app.database.database import get_db
from backend.app.database.schemas.surveys import SurveyCreate, SurveyOut
from backend.app.service.survey_service import SurveyService


router=APIRouter(prefix="/surveys", tags=["Surveys"])


@router.post("", response_model=SurveyOut, status_code=status.HTTP_201_CREATED)
async def create_surveys(survey:SurveyCreate, user_id: int = Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    new_survey=await SurveyService.create_survey(db, user_id, survey)
    return new_survey

@router.get("", response_model=List[SurveyOut])
async def get_all_surveys(user_id:int, db:AsyncSession=Depends(get_db)):
    return await SurveyService.list_survey(db, user_id)

@router.get("/{survey_id}", response_model=SurveyOut)
async def get_my_survey(survey_id:int, user_id: int = Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    my_survey=await SurveyService.get_detailed(db, survey_id, user_id)
    if not my_survey:
        raise HTTPException(status_code=404, detail="Survey Not Found")
    return my_survey

@router.delete("/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_surveys(user_id:int, survey_id:int, db:AsyncSession=Depends(get_db)):
    deleted=await SurveyService.delete_survey(db, user_id, survey_id)
    if deleted==0:
        raise HTTPException(status_code=404, detail="Survey Not Found")
    await db.commit()
    return None


