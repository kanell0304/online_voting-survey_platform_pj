from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.auth import get_user_id
from backend.app.database.database import get_db
from backend.app.database.schemas.surveys import SurveyCreate, SurveyOut, SurveyUpdate
from backend.app.service.survey_service import SurveyService


router=APIRouter(prefix="/surveys", tags=["Surveys"])


@router.post("", response_model=SurveyOut, status_code=status.HTTP_201_CREATED)
async def create_surveys(survey:SurveyCreate, user_id: int = Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    new_survey=await SurveyService.create_survey(db, user_id, survey)
    return new_survey

@router.get("", response_model=List[SurveyOut])
async def get_all_surveys(user_id:int = Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    return await SurveyService.list_survey(db, user_id)

@router.get("/get_all_public_surveys", response_model=List[SurveyOut])
async def get_all_surveys_by_is_public_is_true(db: AsyncSession=Depends(get_db)):
    return await SurveyService.get_all_surveys(db)

@router.get("/{survey_id}", response_model=SurveyOut)
async def get_my_survey(survey_id:int, db:AsyncSession=Depends(get_db)):
    my_survey=await SurveyService.get_detailed(db, survey_id)
    if not my_survey:
        raise HTTPException(status_code=404, detail="Survey Not Found")
    return my_survey

@router.delete("/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_surveys(survey_id:int, user_id:int = Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    deleted=await SurveyService.delete_survey(db, survey_id, user_id)
    if deleted==0:
        raise HTTPException(status_code=404, detail="Survey Not Found")
    await db.commit()
    return None

@router.patch("/{survey_id}", response_model=SurveyOut, status_code=status.HTTP_200_OK)
async def patch_surveys(survey:SurveyUpdate, survey_id:int, user_id:int=Depends(get_user_id), db:AsyncSession=Depends(get_db)):
    updated=await SurveyService.modify_survey(db, survey_id, user_id, survey)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Survey Not Found")
    
    await db.commit()
    return updated
