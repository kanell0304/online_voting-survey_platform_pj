from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.database import get_db
from backend.app.database.schemas.survey_option import SurveyOptionCreate, SurveyOptionOut
from backend.app.service.survey_option_service import SurveyOptionService

router=APIRouter(prefix="/surveys/{survey_id}/survey_questions/{question_id}/survey_options", tags=["Survey Options"])

@router.post("", response_model=SurveyOptionOut, status_code=status.HTTP_201_CREATED)
async def create_options(user_id:int, survey_id:int, option:SurveyOptionCreate, db:AsyncSession=Depends(get_db)):
    new_option=await SurveyOptionService.add_option(db, user_id, survey_id, option)
    if new_option is None:
        raise HTTPException(status_code=404, detail="Survey Not Found or Not Owned")
    await db.commit()
    return new_option

@router.delete("/{option_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_options(user_id:int, survey_id:int, question_id:int, db:AsyncSession=Depends(get_db)):
    deleted=await SurveyOptionService.delete_option(db, user_id, survey_id, question_id)
    if deleted==0:
        raise HTTPException(status_code=404, detail="Option Not Found or Survey Not Owned")
    await db.commit()
    return None