from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from sqlalchemy import Text
from typing import Optional, List
from backend.app.database.models.survey_question import QuestionType
from backend.app.database.schemas.survey_option import SurveyOptionCreate, SurveyOptionOut

class SurveyQuestionBase(BaseModel):
    question_text:str=Field(..., max_length=500)
    question_type:QuestionType
    is_required:bool=Field(default=False)

class SurveyQuestionCreate(SurveyQuestionBase):
    options:Optional[list[SurveyOptionCreate]]=Field(default_factory=list)

class SurveyQuestionOut(SurveyQuestionBase):
    question_id:int
    options:List[SurveyOptionOut]=Field(default_factory=list)
    created_at:Optional[datetime]
    updated_at:Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

