from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database.database import get_db
from backend.app.database.schemas.survey_question import SurveyQuestionCreate, SurveyQuestionOut
from backend.app.service.survey_question_service import SurveyQuestionService


router=APIRouter(prefix="/surveys/{survey_id}/survey_questions", tags=["Survey Questions"])


@router.post("", response_model=SurveyQuestionOut, status_code=status.HTTP_201_CREATED)
async def create_questions(survey_id:int, question:SurveyQuestionCreate, user_id:int, db:AsyncSession=Depends(get_db)):
    new_question=await SurveyQuestionService.add_question(db, survey_id, user_id, question)
    if new_question is None:
        raise HTTPException(status_code=404, detail="Survey Not Found or Not Owned")
    await db.commit()
    return new_question

@router.get("", response_model=List[SurveyQuestionOut])
async def get_all_questions(survey_id:int, user_id:int, db:AsyncSession=Depends(get_db)):
    return await SurveyQuestionService.read_question_list(db, survey_id, user_id)

@router.get("/{question_id}", response_model=SurveyQuestionOut)
async def get_a_question(survey_id:int, question_id:int, user_id:int, db:AsyncSession=Depends(get_db)):
    question=await SurveyQuestionService.read_question(db, survey_id, user_id, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question Not Found")
    return question

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_questions(user_id:int, survey_id:int, question_id: int, db:AsyncSession=Depends(get_db)):
    deleted=await SurveyQuestionService.delete_question(db, survey_id, user_id, question_id)
    if deleted==0:
        raise HTTPException(status_code=404, detail="Question Not Found or Survey Not Owned")
    await db.commit()
    return None